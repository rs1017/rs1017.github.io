---
title: CLion에서 Windows DLL을 Linux .so로 크로스 빌드하는 방법
author: naksupapa
date: 2026-01-13 15:00:00 +0900
categories: [Tech]
tags: [clion, rider, cmake, cross-compile, dll, so, linux, windows, wsl2]
---

# CLion에서 Windows DLL을 Linux .so로 크로스 빌드하기

Windows에서 개발한 C/C++ 라이브러리(.dll)를 Linux 서버에서 사용해야 할 때가 있습니다. JetBrains의 **CLion** (또는 Rider의 C++ 지원)을 사용하면 Windows 환경에서도 Linux용 `.so` 파일을 쉽게 빌드할 수 있습니다.

## 크로스 빌드가 필요한 이유

- 개발 환경은 Windows지만 배포 환경이 Linux 서버인 경우
- 게임 서버, 백엔드 서버 등 Linux 환경에서 네이티브 라이브러리가 필요한 경우
- CI/CD 파이프라인에서 멀티 플랫폼 빌드가 필요한 경우

## 방법 1: WSL2 툴체인 사용 (권장)

가장 간단하고 권장되는 방법입니다.

### 1.1 WSL2 설치 및 설정

```powershell
# PowerShell 관리자 권한으로 실행
wsl --install -d Ubuntu-22.04
```

WSL2 Ubuntu에서 필수 패키지를 설치합니다:

```bash
sudo apt update
sudo apt install -y build-essential cmake gdb
```

### 1.2 CLion에서 WSL2 툴체인 추가

1. **File → Settings → Build, Execution, Deployment → Toolchains**
2. **+** 버튼 클릭 → **WSL** 선택
3. WSL 배포판 선택 (Ubuntu-22.04)
4. CMake, C Compiler, C++ Compiler가 자동 감지되는지 확인

<!-- 이미지: WSL Toolchain 설정 화면 -->

### 1.3 CMake 프로파일 설정

1. **File → Settings → Build, Execution, Deployment → CMake**
2. **+** 버튼으로 새 프로파일 추가
3. **Name**: `Release-Linux-WSL`
4. **Build type**: `Release`
5. **Toolchain**: 위에서 만든 WSL 툴체인 선택

## 방법 2: Docker 컨테이너 사용

Docker를 통해 더 깔끔한 Linux 빌드 환경을 구성할 수 있습니다.

### 2.1 Dockerfile 작성

프로젝트 루트에 `Dockerfile.build`를 생성합니다:

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gdb \
    gdbserver \
    rsync \
    ssh \
    && rm -rf /var/lib/apt/lists/*

# SSH 서버 설정 (CLion 연결용)
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22 7777

CMD ["/usr/sbin/sshd", "-D"]
```

### 2.2 Docker 컨테이너 실행

```bash
docker build -t clion-linux-build -f Dockerfile.build .
docker run -d -p 2222:22 -p 7777:7777 --name linux-builder clion-linux-build
```

### 2.3 CLion에서 Remote Host 툴체인 추가

1. **Settings → Toolchains → +** 버튼 → **Remote Host**
2. **Credentials** 설정:
   - Host: `localhost`
   - Port: `2222`
   - User: `root`
   - Password: `password`

## 방법 3: Remote SSH 서버 연결

실제 Linux 서버나 VM에 직접 연결하여 빌드할 수 있습니다.

### 3.1 Linux 서버 준비

```bash
# 빌드 서버에서 실행
sudo apt install -y build-essential cmake gdb gdbserver rsync
```

### 3.2 CLion Remote Host 설정

1. **Settings → Toolchains → +** → **Remote Host**
2. SSH 접속 정보 입력
3. CMake, GCC/G++ 경로 자동 감지 확인

## CMakeLists.txt 설정

공유 라이브러리를 빌드하기 위한 `CMakeLists.txt` 예제입니다:

```cmake
cmake_minimum_required(VERSION 3.20)
project(MySharedLib VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 공유 라이브러리 생성
add_library(mylib SHARED
    src/mylib.cpp
    src/utils.cpp
)

# 플랫폼별 설정
if(WIN32)
    # Windows DLL 설정
    target_compile_definitions(mylib PRIVATE MYLIB_EXPORTS)
    set_target_properties(mylib PROPERTIES
        WINDOWS_EXPORT_ALL_SYMBOLS ON
        OUTPUT_NAME "mylib"
        PREFIX ""
    )
elseif(UNIX AND NOT APPLE)
    # Linux .so 설정
    set_target_properties(mylib PROPERTIES
        OUTPUT_NAME "mylib"
        VERSION ${PROJECT_VERSION}
        SOVERSION 1
        POSITION_INDEPENDENT_CODE ON
    )
endif()

# 헤더 파일 공개
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
```

## 플랫폼별 Export 매크로

헤더 파일에서 사용할 export 매크로를 정의합니다:

```cpp
// include/mylib_export.h
#pragma once

#ifdef _WIN32
    #ifdef MYLIB_EXPORTS
        #define MYLIB_API __declspec(dllexport)
    #else
        #define MYLIB_API __declspec(dllimport)
    #endif
#else
    #define MYLIB_API __attribute__((visibility("default")))
#endif
```

사용 예시:

```cpp
// include/mylib.h
#pragma once
#include "mylib_export.h"

extern "C" {
    MYLIB_API int add(int a, int b);
    MYLIB_API const char* get_version();
}
```

## 빌드 및 배포

### Windows에서 Linux용 빌드 실행

1. CLion 우측 상단 **CMake 프로파일** 드롭다운 클릭
2. `Release-Linux-WSL` 선택
3. **Build → Build Project** (Ctrl+F9)

빌드 결과물 위치:
- WSL: `\\wsl$\Ubuntu-22.04\home\user\project\cmake-build-release-linux-wsl\`
- Docker/SSH: 원격 서버의 지정된 경로

### 빌드된 .so 파일 확인

```bash
# Linux에서 확인
file libmylib.so
# 출력: libmylib.so: ELF 64-bit LSB shared object, x86-64, ...

# 심볼 확인
nm -D libmylib.so | grep " T "

# 의존성 확인
ldd libmylib.so
```

## 디버깅

WSL이나 Remote 환경에서 디버깅도 가능합니다:

1. **Run → Edit Configurations**
2. CMake Application 선택
3. **Target**: `mylib`
4. **Before launch**에 빌드 추가
5. 중단점 설정 후 **Debug** 실행

GDB Server를 사용한 원격 디버깅:

```bash
# 원격 서버에서
gdbserver :7777 ./test_app

# CLion에서 GDB Remote Debug 설정
```

## 자주 발생하는 문제

### 1. undefined reference 에러

```
CMake Error: undefined reference to `__imp_xxx'
```

**해결**: Windows 전용 함수나 라이브러리 호출 부분을 `#ifdef _WIN32`로 분기 처리

### 2. GLIBC 버전 호환성

```
./libmylib.so: version `GLIBC_2.34' not found
```

**해결**: 배포 대상 서버와 동일한 GLIBC 버전의 Ubuntu를 사용하여 빌드

### 3. Position Independent Code 에러

```
relocation R_X86_64_PC32 against symbol can not be used
```

**해결**: CMakeLists.txt에 `POSITION_INDEPENDENT_CODE ON` 추가

## 정리

| 방법 | 장점 | 단점 |
|------|------|------|
| **WSL2** | 설정 간단, 빠른 빌드 | Windows 10/11 필요 |
| **Docker** | 환경 일관성, 재현성 | 초기 설정 복잡 |
| **Remote SSH** | 실제 환경과 동일 | 네트워크 필요 |

개인 개발 환경에서는 **WSL2**를, CI/CD나 팀 환경에서는 **Docker**를 추천합니다.

## 참고 자료

- [JetBrains CLion WSL Documentation](https://www.jetbrains.com/help/clion/how-to-use-wsl-development-environment-in-clion.html)
- [CMake Shared Library Tutorial](https://cmake.org/cmake/help/latest/command/add_library.html)
- [GCC Visibility](https://gcc.gnu.org/wiki/Visibility)
