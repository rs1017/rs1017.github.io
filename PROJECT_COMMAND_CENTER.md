# Project Command Center Blueprint

## 1. 목적

본 문서는 이 저장소를 "프로젝트 커맨드 센터"로 운영하기 위한 기준 구조를 정의합니다.

- 다중 프로젝트 모니터링
- 룰/에이전트 스킬 제공
- 게임 기획부터 WAS/배포까지 라이프사이클 관리
- 단일 명령 채널 운영

## 2. 운영 도메인

### Monitoring
- 프로젝트 상태 수집
- 리스크 탐지
- 진행률 시각화

### Governance (Rule/Policy)
- 운영 정책 작성 및 개정
- 위반 케이스 기록
- 개선 액션 추적

### Agent Skills
- 반복 작업의 스킬화
- 스킬 버전/적용 범위 관리
- 실행 로그 누적

### Game Lifecycle
- Vision/Design
- Development (WAS 포함)
- QA
- Deployment

## 3. 권장 저장소 운영 방식

1. 명령 요청은 이슈/문서/커밋으로 남긴다.
2. 정책 변경은 이유와 적용 범위를 함께 기록한다.
3. 배포는 검증 결과와 함께 기록한다.
4. 모니터링 결과는 정기 요약 포스트로 발행한다.

## 4. 문서 매핑

- 정책: `*_POLICY.md`
- 로드맵: `*_ROADMAP.md`
- 룰: `assets/downloads/rules/`
- 운영 기록: `_posts/`
- 소개/원칙: `_tabs/about.md`, `README.md`

## 5. KPI 예시

- 배포 성공률
- 정책 위반 건수
- 자동화 전환율
- 명령 처리 리드타임
