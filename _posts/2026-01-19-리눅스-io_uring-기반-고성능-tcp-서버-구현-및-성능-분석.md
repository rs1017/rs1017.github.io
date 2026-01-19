---
layout: post
title: "리눅스 io_uring 기반 고성능 TCP 서버 구현 및 성능 분석"
date: 2026-01-19 19:28:22 +0900
categories: [Tech]
tags: [io_uring, 네트워크, Linux, 성능최적화]
image:
  path: /assets/img/posts/2026-01-19-리눅스-io_uring-기반-고성능-tcp-서버-구현-및-성능-분석/main.jpg
  alt: 리눅스 io_uring 기반 고성능 TCP 서버 구현 및 성능 분석
---

# 시스템 콜을 0회로: io_uring이 epoll을 압도하는 리눅스 고성능 서버의 비밀

고성능 네트워크 프로그래밍의 역사는 **시스템 콜(System Call)** 오버헤드를 줄이는 과정이었습니다. C10K 문제를 해결하며 리눅스 서버의 표준으로 자리 잡은 `epoll` 역시 비동기(Asynchronous) I/O의 혁명을 가져왔지만, 대규모 동시 접속 환경에서는 여전히 `read()`와 `write()` 호출이 성능 병목을 유발하는 근본적인 한계에 부딪힙니다.

이 글은 리눅스 커널 5.1 버전 이후 등장한 **`io_uring`**이 기존 `epoll` 기반 서버의 성능 천장을 어떻게 뚫어내는지 심층적으로 분석하고, 특히 TCP 서버 구현에서 필수적으로 적용해야 할 핵심 최적화 전략들을 제시합니다.

---

## I. I/O 병목의 벽: 우리가 `epoll`에 만족할 수 없는 이유

수십만 이상의 동시 연결을 처리하는 고성능 서버 환경에서, CPU 리소스의 상당 부분이 실제 데이터 처리 대신 **문맥 전환(Context Switching)**에 낭비됩니다.

`epoll`은 파일 디스크립터의 상태 변화를 효율적으로 감지하여 I/O 준비가 완료되었을 때만 애플리케이션에 알리는 훌륭한 메커니즘을 제공합니다. 그러나 알림을 받은 후 실제 I/O 작업, 즉 `recvmsg()`나 `sendmsg()`를 수행할 때마다 **사용자 공간(User Space)**에서 **커널 공간(Kernel Space)**으로의 시스템 콜 전환이 발생합니다.

이는 마치 고속도로(네트워크)를 빠르게 달리다가도 톨게이트(시스템 콜)마다 속도를 줄이고 비용을 지불해야 하는 것과 같습니다. 트랜잭션 빈도가 높아질수록 이 톨게이트 비용은 전체 성능을 지배하게 됩니다.

> **핵심 문제:** `epoll`은 이벤트를 효율적으로 기다리게 해주지만, **실제 I/O 연산 자체의 시스템 콜 오버헤드**는 해결하지 못합니다.

**`io_uring`**은 이 근본적인 시스템 콜 오버헤드를 극복하기 위해 설계된 리눅스 비동기 I/O 인터페이스의 혁신적인 재설계 결과물입니다.

## II. io_uring, 시스템 콜을 삭제하는 마법: SQ와 CQ의 비밀

`io_uring`의 핵심 아이디어는 I/O 요청과 완료를 위한 **공유 링 버퍼(Shared Ring Buffer)**를 커널 공간과 사용자 공간이 함께 매핑하여 사용하는 것입니다.

이 링 버퍼는 두 개의 핵심 컴포넌트로 구성됩니다.

1.  **Submission Queue (SQ, 제출 큐):** 사용자 애플리케이션이 수행하고자 하는 I/O 요청을 기록합니다. 각 요청은 **Submission Queue Entry (SQE)** 형태입니다.
2.  **Completion Queue (CQ, 완료 큐):** 커널이 I/O 작업을 완료한 후 그 결과를 애플리케이션에 보고합니다. 각 결과는 **Completion Queue Entry (CQE)** 형태입니다.

### 링 버퍼 작동 원리

1.  **요청 배치 (Batching):** 애플리케이션은 하나 이상의 SQE를 SQ에 기록합니다. 이때, 실제 커널 호출은 아직 발생하지 않습니다.
2.  **단 한 번의 커널 진입:** 애플리케이션은 `io_uring_enter()` 시스템 콜을 단 한 번 호출하여, SQ에 쌓아둔 모든 요청을 한 번에 커널에 전달합니다.
3.  **비동기 처리:** 커널은 전달받은 요청들을 비동기적으로 처리합니다.
4.  **결과 회수:** 커널은 작업 완료 시 CQ에 CQE를 기록합니다. 애플리케이션은 CQ를 직접 폴링(Polling)하여 결과를 확인할 수 있습니다.

이 메커니즘을 통해 수많은 I/O 요청이 단 하나의 `io_uring_enter()` 호출로 처리됩니다. 이는 기존의 `O_NONBLOCK` + `epoll` 방식에서 **요청 하나당 시스템 콜이 필요했던 구조**를 근본적으로 뒤집어, **시스템 콜 횟수를 극한으로 줄이는(Zero-copy for requests)** 결과를 낳습니다.

---

## III. 고성능 TCP 서버를 위한 필승 전략: Multishot과 SQ Polling

`io_uring`은 일반적인 파일 I/O뿐만 아니라 네트워크 프로그래밍에 특화된 고급 기능들을 제공합니다. 고성능 TCP 서버를 구현한다면 반드시 다음 두 가지 핵심 기능을 활용해야 합니다.

### 1. IORING_SETUP_SQPOLL: 시스템 콜 오버헤드의 최소화

기본 `io_uring` 모드에서도 시스템 콜 횟수는 줄어들지만, 애플리케이션이 요청을 제출하기 위해 여전히 `io_uring_enter()`를 호출해야 합니다.

**SQ Polling** 모드(링 생성 시 `IORING_SETUP_SQPOLL` 플래그 사용)를 활성화하면, 커널은 별도의 전용 커널 스레드(`kworker`)를 생성하여 SQ를 지속적으로 폴링합니다.

| 모드 | 요청 제출 방식 | 시스템 콜 부하 |
| :--- | :--- | :--- |
| **기본 모드** | 사용자 공간에서 `io_uring_enter()` 호출 | 요청 배치 시 한 번 발생 |
| **SQPOLL** | 커널 스레드(`kworker`)가 SQ를 확인하고 즉시 처리 | **0회 (커널 스레드가 대신 처리)** |

SQPOLL을 사용하면, 사용자 공간 스레드는 데이터를 SQ에 넣는 작업만 수행하면 됩니다. 커널 스레드가 이를 즉시 감지하고 처리하므로, 레이턴시가 결정적인 환경에서 시스템 콜 부하를 사실상 0에 가깝게 만들 수 있습니다.

### 2. Multishot I/O: 재등록 오버헤드의 제거

전통적인 비동기 I/O 모델(예: `epoll`)에서는 클라이언트 연결을 수락하거나 데이터를 수신할 때마다 해당 I/O 요청을 이벤트 루프에 **재등록**해야 하는 오버헤드가 발생했습니다.

`io_uring`의 **Multishot** 기능은 이 재등록 과정을 완전히 생략합니다.

#### Multishot `accept` (`IORING_OP_ACCEPT_MULTISHOT`)
일반적인 `accept`는 클라이언트 연결이 들어오면 해당 요청이 완료되고, 서버는 다음 연결을 기다리기 위해 `accept` 요청을 다시 등록해야 합니다.

Multishot `accept`를 사용하면, **단 하나의 SQE 등록**으로 커널이 지속적으로 들어오는 모든 연결을 수락하고, 완료 정보를 CQ에 쌓아줍니다. 서버는 CQ만 처리하면 되며, `accept` 요청을 다시 등록할 필요가 없습니다.

#### Multishot `recv` (`IORING_OP_RECV_MULTISHOT`)
데이터 수신(read) 역시 마찬가지입니다. 단일 `recv` 요청이 처리되면 다음 데이터를 받기 위해 다시 등록해야 했지만, Multishot `recv`는 한 번의 등록으로 해당 소켓에서 발생하는 모든 데이터 수신 이벤트를 처리합니다.

이 두 가지 Multishot 기능은 고도로 동시성이 높은 TCP 서버의 **루프 오버헤드(Loop Overhead)**를 극적으로 줄여, 극한의 성능을 달성하게 합니다.

### 3. Registered Buffers: 메모리 비용 절감

네트워크 I/O가 발생할 때마다 커널은 유저 공간이 제공한 버퍼의 유효성을 검사하고, 해당 페이지를 고정(Pinning)하는 작업을 수행해야 합니다. 이는 상당한 오버헤드입니다.

`io_uring`은 서버가 사용할 버퍼들을 **미리 커널에 등록(Registered)**하는 기능을 제공합니다. 요청 시 버퍼의 ID만 전달하면 되므로, 커널은 매번 버퍼 유효성 검사 및 고정 작업을 생략할 수 있습니다. 이는 특히 대량의 작은 패킷을 처리할 때 레이턴시를 획기적으로 줄여줍니다.

---

## IV. 성능 최적화의 양날의 검: io_uring 구현의 복잡성과 코드 예시

`io_uring`을 직접 사용하기 위해서는 C 언어 기반의 공식 라이브러리인 `liburing`을 사용하는 것이 일반적입니다.

### 핵심 구현 패턴: Multishot Accept

`io_uring` 서버의 I/O 루프는 `epoll` 서버와는 완전히 다른 방식으로 설계됩니다. 다음은 `liburing` 기반 Multishot Accept를 등록하는 핵심 코드 패턴입니다.

```c
#include <liburing.h>
#include <arpa/inet.h>
#include <sys/socket.h>

// io_uring 인스턴스 초기화 (링 크기, SQPOLL 플래그 등 설정)
struct io_uring ring;
// ENTRIES는 링 버퍼의 크기를 지정하는 상수입니다.
io_uring_queue_init(ENTRIES, &ring, IORING_SETUP_SQPOLL);

// SQ에 Multishot Accept 요청 등록
void setup_accept(struct io_uring *ring, int listen_fd, struct sockaddr_in *addr) {
    // 1. 제출 큐 엔트리(SQE) 확보
    struct io_uring_sqe *sqe = io_uring_get_sqe(ring);
    
    // addr_len 초기화 필요 (예: socklen_t addr_len = sizeof(*addr);)
    // 2. Multishot Accept 요청 준비
    io_uring_prep_accept_multishot(sqe, listen_fd, (struct sockaddr*)addr, 
                                   &addr_len, 0);

    // 3. 사용자 데이터(user_data) 설정: CQE가 돌아올 때 식별자로 사용
    sqe->user_data = ACCEPT_ID; 
}

// CQE 처리 루프 (서버 메인 루프)
void handle_completions(struct io_uring *ring) {
    struct io_uring_cqe *cqe;
    unsigned int head;
    unsigned int count = 0;
    
    // CQ에서 완료된 요청들을 기다림
    io_uring_submit_and_wait(ring, 1); 

    // 완료된 요청들을 처리
    io_uring_for_each_cqe(&ring, cqe) {
        if (cqe->user_data == ACCEPT_ID) {
            // 새 연결 처리: Multishot Accept의 경우 cqe->res에 새 연결 FD가 담겨 있음
            int client_fd = cqe->res;
            
            // 새 연결 FD에 대한 Multishot Recv 요청을 추가로 등록
            setup_multishot_recv(ring, client_fd); 
        }
        // ... 다른 I/O 처리 (Recv, Send 완료 등)
        count++;
    }
    
    // 사용한 CQE 정리
    io_uring_cq_advance(ring, count); 
}
```

### Trade-off 분석: 복잡성과 의존성

`io_uring`은 압도적인 성능을 제공하지만, 개발 및 운영 측면에서 다음과 같은 트레이드오프가 존재합니다.

1.  **개발 복잡성 증가:** `epoll` 대비 `io_uring`의 API는 훨씬 저수준(Low-level)이며, 링 버퍼의 상태 관리, SQE/CQE의 정확한 매핑, Multishot의 생명주기 관리 등이 까다롭습니다. 버퍼 관리 오류는 커널 메모리 유출로 이어질 수 있습니다.
2.  **커널 버전 의존성:** `io_uring`의 주요 성능 최적화 기능(특히 Multishot, SQPOLL)은 비교적 최신 커널 버전(주로 5.6 이후, 안정화는 5.10 이상)을 요구합니다. 오래된 리눅스 배포판에서는 활용이 어렵습니다.
3.  **디버깅의 어려움:** 비동기 I/O 자체도 디버깅이 어렵지만, 커널 공간에서 요청이 처리되는 `io_uring` 환경은 GDB 등 표준 도구로 추적하기 어려운 경우가 많습니다.

이러한 복잡성을 해소하기 위해 Rust의 `tokio-uring`이나 C++의 `liburing` 래퍼 라이브러리 등, `io_uring`을 고수준으로 추상화한 런타임들이 등장하고 있습니다. 성능이 절대적으로 중요한 코어 로직이 아니라면, 이러한 추상화된 런타임을 사용하는 것이 생산성 측면에서 유리할 수 있습니다.

---

## V. io_uring이 정의하는 미래의 네트워크 I/O: 지금 시작해야 하는 이유

`io_uring`은 단순한 `epoll`의 개선판이 아니라, 리눅스 I/O 스택 전체를 재정의하는 기술 혁명입니다. 이는 네트워크 I/O 성능에 목마른 모든 개발자에게 필수적인 기술이 되고 있습니다.

**`io_uring`의 영향 범위:**

1.  **네트워크 서버:** 이미 Nginx의 일부 기능이나 고성능 데이터베이스(Redis 등)의 대안으로 `io_uring` 기반 솔루션들이 연구되고 있습니다.
2.  **스토리지 I/O:** `io_uring`은 NVMe 드라이브와 같은 초고속 스토리지를 비동기적으로 다루는 데 최적화되어, 데이터베이스나 파일 시스템 성능 향상에 직접적인 기여를 합니다.
3.  **데이터 처리:** 대규모 파일 처리, 로깅 시스템 등 모든 I/O 집약적 애플리케이션에서 `io_uring`은 시스템 콜 오버헤드를 제거하여 처리량을 극대화합니다.

만약 당신의 서비스가 C10K를 넘어 C1M(100만 동시 접속)을 목표로 하거나, 극도로 낮은 레이턴시를 요구한다면, 기존 `epoll` 방식의 성능 한계에 갇혀 있지 말고 `io_uring` 기반 아키텍처로의 전환을 준비해야 합니다.

`io_uring`은 개발 초기 단계에 있지만, 그 잠재력은 이미 입증되었습니다. 고성능 컴퓨팅(HPC)의 미래는 시스템 콜 오버헤드가 없는 제로-카피 I/O에 달려 있으며, `io_uring`이 그 중심에 있습니다.

*(This post was automatically generated by AI Agent Pipeline)*
