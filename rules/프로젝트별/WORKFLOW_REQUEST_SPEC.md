# 블로그 기반 워크플로우 요청 사양

## 목적
- 이 블로그(Command Center)에서 요청하면, 고정 지침으로 `그래픽/전투씬/영상/사운드` 산출물을 생성하고 게시한다.

## 요청 포맷
다음 항목을 한 줄 또는 목록으로 전달:

1. 프로젝트: `godot-001-card-battle` 또는 `godot-002-card-3d-battle-kaykit`
2. 산출물: `그래픽컨셉`, `전투씬`, `게임영상`, `사운드` 중 선택
3. 길이/형식: 예) `영상 15초`, `gif`, `wav`
4. 스타일 키워드: 예) `dark fantasy`, `ui-safe`, `high readability`
5. 게시 여부: 예) `블로그 게시`, `초안만`

예시:
- `godot-002, 그래픽+영상(15초)+사운드, dark fantasy, 블로그 게시`

## 기본 실행 규칙
1. 작업 대상은 기본적으로 **블로그 저장소(`rs1017.github.io`)**이다.
2. 프로젝트 저장소 변경은 사용자가 명시적으로 요청한 경우에만 수행한다.
3. 생성 결과는 `assets/media/<project-id>/` 하위에 저장한다.
4. 게시 시 `_posts/`에 프로젝트별 미디어 포스트를 생성한다.
5. 태그는 반드시 `프로젝트명`, `방향성`을 포함한다.

## 산출물 표준 경로
- 그래픽 컨셉 보드: `assets/media/<project>/graphics_concept_board.png`
- 전투 씬: `assets/media/<project>/battle_scene.png`
- 영상: `assets/media/<project>/gameplay_video.gif` (또는 mp4)
- 사운드: `assets/media/<project>/audio/battle_theme_preview_15s.wav`

## ComfyUI 표준
- 루트: `D:/ComfyUI-Easy-Install-Windows/ComfyUI-Easy-Install/ComfyUI`
- 모델 경로: `D:/ComfyUI-Easy-Install-Windows/ComfyUI-Easy-Install/ComfyUI/models`
- API: `http://127.0.0.1:8188`

## 실패 시 처리
1. ComfyUI API 실패 시 원인(노드 불일치/모델 누락)을 먼저 기록
2. 즉시 대체안(기존 프레임 기반 패키징) 수행
3. 복구 필요 항목을 같은 게시글 하단에 명시
