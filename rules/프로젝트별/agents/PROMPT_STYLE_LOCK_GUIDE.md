# ComfyUI Prompt Style Lock Guide

## 목적
- 게임 그래픽과 15초 영상에서 캐릭터/배경/색감이 컷마다 흔들리지 않도록 고정 규칙을 제공한다.

## 공통 원칙
1. `Base Prompt`(불변)와 `Shot Prompt`(가변)를 분리한다.
2. 모델, VAE, LoRA, sampler, cfg, steps, 해상도, seed 정책을 프로젝트 단위로 고정한다.
3. 무작위 요소는 한 번에 하나만 변경한다.

## Base Prompt 템플릿
```text
[PROJECT_STYLE_LOCK]
game cinematic, stylized fantasy card battle, clean silhouette, readable UI-safe composition,
consistent character outfit and emblem, consistent color palette, controlled lighting, high detail

[CHARACTER_LOCK]
<character_name>, <hair>, <armor/material>, <main_color>, <weapon_type>, same face identity

[SCENE_LOCK]
battle arena, same architectural motifs, same time-of-day lighting, coherent atmosphere
```

## Shot Prompt 템플릿
```text
[SHOT_ACTION]
camera angle: <wide|medium|close>, action: <attack|summon|reaction>, motion intensity: <low|mid|high>
duration target: <seconds>, framing: <rule>
```

## Negative Prompt 기본
```text
extra limbs, deformed hands, inconsistent face, wrong costume, text artifacts, watermark, blurry, low contrast
```

## Seed/파라미터 고정 규칙
- 캐릭터 고정 샷: 동일 seed 유지
- 액션 변형 샷: `seed + 1~5` 범위만 사용
- 핵심 파라미터 권장 고정:
  - FLUX: model + text encoder + vae 고정, cfg/steps 고정
  - SDXL: base/refiner 쌍 고정, LoRA 가중치 고정
  - 비디오(Wan): keyframe seed 고정 + 프레임 보간만 변경

## 15초 영상 연속성 규칙
1. 0초/7초/14초 키프레임을 먼저 생성한다.
2. 중간 프레임은 동일 스타일 잠금값으로 생성한다.
3. 컷 전환은 조명/팔레트가 갑자기 바뀌지 않도록 한 단계씩만 변화시킨다.
4. 최종 검수는 `캐릭터 일치`, `의상 일치`, `색감 일치`, `배경 일치` 4항목으로 수행한다.

## 권장 모델 세트 (D:/ComfyUI-Easy-Install-Windows/ComfyUI-Easy-Install/ComfyUI/models 기준)
- 이미지 고품질: `diffusion_models/flux1-dev-fp8.safetensors`
- 이미지 고속: `diffusion_models/flux1-schnell-fp8.safetensors`
- SDXL 베이스: `checkpoints/sd_xl_base_1.0.safetensors`
- SDXL 리파이너: `checkpoints/sd_xl_refiner_1.0.safetensors`
- LoRA 가속: `loras/Hyper-FLUX.1-dev-8steps-lora.safetensors`, `loras/lcm_lora_sdxl.safetensors`
- 15초 영상: `diffusion_models/wan2.1_t2v_1.3B_fp16.safetensors`
