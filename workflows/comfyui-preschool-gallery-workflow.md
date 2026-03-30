# ComfyUI Preschool Gallery Workflow

## Target

One post = one theme = 10 images minimum

Allowed output style:

- bright illustration
- clean silhouette
- low clutter
- preschool-friendly shapes
- easy printable conversion later

## Folder Convention

For each new post, create:

- `assets/img/playroom/<theme>/01.svg` or `01.png`
- `assets/img/playroom/<theme>/02.svg` or `02.png`
- ...
- `assets/img/playroom/<theme>/10.svg` or `10.png`

Theme examples:

- `spring`
- `garden`
- `ocean`
- `tracing`
- `counting`

## Shot List Rule

Lock the 10-shot list before generation.

Example for one theme:

1. hero scene
2. close subject
3. wide scene
4. motion scene
5. object focus
6. alternate angle
7. alternate mood
8. simpler composition
9. decorative pattern scene
10. closing scene

## Core ComfyUI Graph

Use this graph as the base:

1. `Load Checkpoint`
2. `CLIP Text Encode (Positive)`
3. `CLIP Text Encode (Negative)`
4. `Empty Latent Image`
5. `KSampler`
6. `VAE Decode`
7. `Save Image`

Add these branches only when needed:

- `Image Scale / Upscale` for web export refinement
- `Image-to-Image` for consistency and cleanup
- `ControlNet` if composition is drifting too much
- `LoRA Loader` if one child-friendly house style is needed

## Base Generation Settings

Start here and only move if the set is weak:

- aspect ratio: landscape first
- batch size: 4
- total candidate count per theme: 24 to 40
- denoise: moderate
- guidance: moderate
- seed: fixed for variations, changed for expansion

The goal is not one perfect image.
The goal is one strong 10-image set.

## Prompt Formula

Use one prompt skeleton for the whole post.

### Positive Prompt

`[main subject], [environment], preschool-friendly illustration, clean silhouette, simple shapes, bright paper-friendly palette, soft texture, charming composition, no text`

### Negative Prompt

`text, watermark, logo, cluttered background, photorealistic skin, extra fingers, distorted face, extra limbs, muddy colors, dark horror mood, busy frame`

## Theme Lock Layer

Before batching the 10 shots, lock these four:

- palette
- subject family
- background treatment
- line/detail density

Example:

- palette: warm spring pastel
- subject family: rabbit, flowers, trees
- background treatment: 2 depth layers only
- detail density: medium, no tiny micro-details

## Batch Method

### Pass 1. Look Development

- generate 8 to 12 images
- pick 2 strongest
- write down what worked

### Pass 2. Theme Batch

- keep prompt skeleton fixed
- swap only scene nouns and camera wording
- generate 24 to 40 candidates

### Pass 3. Cleanup Batch

- run selected images through image-to-image lightly
- remove noise
- simplify weak edges
- unify saturation and contrast

## Selection Rules

Reject any image that has:

- unclear silhouette
- dead center empty composition
- over-detailed background
- malformed faces or limbs
- accidental text-like artifacts
- muddy lighting

Keep images that:

- read well at thumbnail size
- still look clear when printed smaller
- have one immediate subject

## Web Export Rules

For gallery use:

- one title only
- one image only
- no caption paragraphs

Export target:

- web preview: optimized png/webp
- source archive: larger master file

## Post Assembly Rules

When assembling the page:

- place 10 images minimum
- keep caption to 2 to 4 Korean syllables or one short noun phrase
- do not insert explanation paragraphs between images
- do not insert long intro text above the gallery

## Example Title Set

### Spring

- 토끼 산책
- 튤립 언덕
- 나비 나무
- 꽃 바구니
- 햇살 들판
- 구름 그네
- 새싹 집
- 꽃비 길
- 봄 연못
- 숲속 낮잠

### Garden

- 숨은 정원
- 새집 길
- 꽃 울타리
- 물뿌리개
- 나비 구석
- 열매 잎
- 둥근 화분
- 정원 문
- 초록 미로
- 꽃 그늘

### Ocean

- 바다 친구
- 산호 길
- 고래 숨결
- 조개 모래
- 별 바위
- 파도 터널
- 해마 숲
- 거북 산책
- 노랑 물고기
- 바다 낮잠
