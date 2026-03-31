# ComfyUI Preschool Activity Workflow

## Target

One post = one activity type = 10 images minimum

Allowed output style:

- clean silhouette
- low clutter
- preschool-friendly shapes
- easy printable conversion later
- line art, black-and-white, or minimal color for most worksheet types

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

## Activity List Rule

Lock the 10-page activity list before generation.

Example for one theme:

1. page purpose
2. target object or letter
3. difficulty note
4. line-art requirement
5. whitespace requirement
6. assembly note if needed
7. print check
8. variation note
9. short title
10. export target

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

- `Image Scale / Upscale` for source cleanup
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

The goal is not one beautiful finished painting.
The goal is one strong 10-page printable activity set.

## Prompt Formula

Use one prompt skeleton for the whole post.

### Positive Prompt

`[activity type], [main subject], preschool printable worksheet source art, clean silhouette, simple shapes, black and white line art or minimal color, white background or low clutter, no text`

### Negative Prompt

`text, watermark, logo, cluttered background, photorealistic skin, extra fingers, distorted face, extra limbs, muddy colors, dark horror mood, busy frame, gradients, painterly shading`

## Activity Lock Layer

Before batching the 10 pages, lock these four:

- activity goal
- subject family
- background treatment
- line/detail density

Example:

- activity goal: spring coloring pages
- subject family: rabbit, flowers, trees
- background treatment: white background or single shallow scene layer
- detail density: bold outlines, no tiny micro-details

## Batch Method

### Pass 1. Look Development

- generate 8 to 12 images
- pick 2 strongest
- write down what worked

### Pass 2. Activity Batch

- keep prompt skeleton fixed
- swap only worksheet nouns and subject wording
- generate 24 to 40 candidates

### Pass 3. Cleanup Batch

- run selected images through image-to-image lightly
- remove noise
- simplify weak edges
- unify line weight and contrast
- strip extra color from non-coloring pages

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
- have one immediate task
- leave enough white space for printing

## Web Export Rules

For post use:

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
- do not insert long intro text above the image set

## Example Title Set

### Spring Coloring

- 꽃 토끼
- 튤립 집
- 나비 나무
- 꽃 바구니
- 봄 들판
- 구름 그네
- 새싹 집
- 꽃비 길
- 봄 연못
- 숲 낮잠

### Garden Hidden Picture

- 정원 문
- 새집 길
- 꽃 울타리
- 물뿌리개
- 나비 자리
- 열매 잎
- 둥근 화분
- 정원 길
- 벤치 찾기
- 꽃 그늘

### Ocean Cut And Paste Source

- 고래
- 물고기
- 조개
- 문어
- 산호
- 돌고래
- 해마
- 불가사리
- 잠수함
- 파도
