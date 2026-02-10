-
---
layout: post
title: "Performance Profiler: 애플리케이션 성능 병목 분석 스킬"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [performance, profiling, optimization, bottleneck, cpu, memory, debugging, analysis]
---

## 개요

애플리케이션이 느려지는 원인을 정확히 파악하고 싶으신가요? Performance Profiler 스킬은 코드 실행 시간, 메모리 사용량, CPU 활용률을 분석하여 성능 병목을 찾아내고 최적화 방안을 제시합니다.

프로덕션 배포 전 성능 검증, 느린 API 엔드포인트 개선, 메모리 누수 탐지 등 다양한 성능 문제 해결에 활용할 수 있습니다.

## 주요 기능

### 1. 실행 시간 프로파일링
- 함수별 실행 시간 측정
- 호출 스택 분석
- 핫 패스(병목 경로) 식별
- 실행 흐름 시각화

### 2. 메모리 프로파일링
- 힙 메모리 분석
- 메모리 누수 탐지
- 객체 할당 추적
- 가비지 컬렉션 메트릭

### 3. CPU 프로파일링
- CPU 사용률 추적
- 스레드 분석
- 컨텍스트 스위칭 측정
- CPU 바운드 작업 탐지

### 4. I/O 프로파일링
- 파일 I/O 작업 분석
- 네트워크 요청 타이밍
- 데이터베이스 쿼리 성능
- 외부 API 호출 지연

## 사용 방법

### 기본 프로파일링 (Python)

```bash
# CPU 프로파일링
python -m cProfile -o output.prof script.py

# 라인별 상세 분석
kernprof -l -v script.py

# 메모리 프로파일링
python -m memory_profiler script.py
```

### 고급 분석 예제

```python
import cProfile
import pstats
from pstats import SortKey

# 프로파일러 시작
profiler = cProfile.Profile()
profiler.enable()

# 분석할 코드
result = your_function()

profiler.disable()

# 리포트 생성 (누적 시간 기준 정렬)
stats = pstats.Stats(profiler)
stats.sort_stats(SortKey.CUMULATIVE)
stats.print_stats(20)  # 상위 20개 함수
```

### 메모리 프로파일링

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    data = [i for i in range(1000000)]
    return data
```

### Node.js 프로파일링

```bash
# CPU 프로파일링
node --prof app.js
node --prof-process isolate-*.log > report.txt

# 힙 스냅샷
node --inspect app.js
# Chrome DevTools로 접속하여 분석
```

## 프로파일링 워크플로우

```
1. 기준선 측정 (Baseline)
   ↓
2. 프로파일러 실행
   ↓
3. 결과 분석
   ↓
4. 병목 지점 식별
   ↓
5. 최적화 적용
   ↓
6. 재측정 및 비교
   ↓
7. 리포트 생성
```

## 출력 리포트 예시

```markdown
# Performance Profiling Report

## 요약
- 총 실행 시간: 5.234초
- 최대 메모리 사용량: 245MB
- CPU 사용률: 78%
- I/O 대기 시간: 1.2초

## 주요 병목 지점
1. database_query() - 2.1초 (40%)
2. process_data() - 1.5초 (29%)
3. render_template() - 0.8초 (15%)

## 최적화 권장사항
1. 데이터베이스 결과 캐싱 적용
2. process_data()의 중첩 루프 최적화
3. 템플릿 지연 로딩(lazy loading) 사용
```

## 일반적인 병목 패턴과 해결책

### N+1 쿼리 문제

```python
# 비효율적 (각 유저마다 쿼리 발생)
for user in users:
    posts = user.posts

# 효율적 (한 번의 쿼리로 처리)
users = User.objects.prefetch_related('posts')
```

### 비효율적인 반복문

```python
# O(n²) 복잡도
for i in range(len(items)):
    for j in range(len(items)):
        # 처리

# O(n) 복잡도
from collections import Counter
counts = Counter(items)
```

### 메모리 누수

```python
# 나쁜 예 (전역 캐시가 계속 증가)
global_cache = {}

# 좋은 예 (자동으로 오래된 항목 제거)
from functools import lru_cache
@lru_cache(maxsize=128)
def cached_function(arg):
    pass
```

## 언어별 프로파일링 도구

| 언어 | CPU 프로파일러 | 메모리 프로파일러 | 시각화 도구 |
|------|---------------|------------------|-------------|
| Python | cProfile | memory_profiler | SnakeViz |
| JavaScript | V8 Profiler | Heap Snapshot | Chrome DevTools |
| Java | JProfiler | VisualVM | JConsole |
| Go | pprof | pprof (heap) | go tool pprof |
| C++ | gprof | Valgrind | KCachegrind |

## CI/CD 통합

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on: [pull_request]

jobs:
  profile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Profiler
        run: |
          python -m cProfile -o profile.stats app.py
          python -m pstats profile.stats
      - name: Compare with Baseline
        run: python compare_profiles.py
```

## 베스트 프랙티스

### 프로파일링 전
- 프로덕션과 유사한 데이터 볼륨 사용
- 디버그 모드 비활성화
- 불필요한 애플리케이션 종료
- 정확성을 위해 여러 번 실행

### 프로파일링 중
- 실제 워크로드 프로파일링
- 초기화 코드는 제외
- 핫 패스에 집중 (80/20 법칙)
- CPU와 메모리 모두 측정

### 프로파일링 후
- 기준선과 비교
- 최적화 검증
- 결과 문서화
- 변경 후 재측정

## 파일 위치

| 구분 | 경로 |
|------|------|
| 정의 파일 | `/assets/downloads/skills/performance-profiler/SKILL.md` |
| 설치 위치 | `~/.claude/skills/performance-profiler/` |