# ComfyUI 이미지/영상 워크플로우 템플릿

## 1) 이미지(컨셉/전투씬) 기본
- 모델: `flux1-schnell-fp8.safetensors` 또는 `flux1-dev-fp8.safetensors`
- 텍스트 인코더: `clip_l.safetensors`, `t5xxl_fp8_e4m3fn.safetensors`
- VAE: `ae.safetensors`
- 해상도: `1344x768` (기본)
- 스타일 잠금: `rules/프로젝트별/agents/PROMPT_STYLE_LOCK_GUIDE.md`

권장 프롬프트 구조:
1. `PROJECT_STYLE_LOCK`
2. `CHARACTER_LOCK`
3. `SCENE_LOCK`
4. `SHOT_ACTION`

## 2) 15초 영상 기본
- 모델: `wan2.1_t2v_1.3B_fp16.safetensors`
- text encoder: `umt5_xxl_fp8_e4m3fn_scaled.safetensors`
- clip vision: `clip_vision_h.safetensors`
- vae: `wan_2.1_vae.safetensors`
- 길이: 15초
- 구조: `0~3초 훅`, `3~10초 전개`, `10~13초 임팩트`, `13~15초 엔드카드`

## 3) 결과 패키징
- 이미지 4장 이상일 때 `graphics_concept_board.png` 생성
- 전투 프레임 시퀀스는 `gameplay_video.gif` 우선 생성
- 사운드는 `battle_theme_preview_15s.wav` 기본
