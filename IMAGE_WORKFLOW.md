# Preschool Activity Workflow

## Goal

Each post ships with:

- 1 activity purpose
- 10 printable pages minimum
- 1 short title per image

No long explanations inside the page itself.

## Production Order

1. Pick one activity type
2. Write a 10-page activity list
3. Decide what must be AI-generated and what must be layout-built
4. Generate only the needed source assets
5. Assemble printable pages
6. Insert them into one Markdown post

## Activity Rules

- One post should stay on one worksheet goal
- Hidden picture, maze, tracing, matching, English, and cut-and-paste should not default to full-color art
- Coloring pages can carry color only as preview material; printable output should still favor line clarity
- Background noise should stay low enough for preschool readability

## 10-Page List Template

Use a fixed structure so every post is fast to assemble.

1. page goal
2. target age / difficulty
3. required objects or letters
4. line-art vs minimal-color decision
5. page-specific prompt or layout note
6. print-readability check

## ComfyUI Workflow Direction

### Stage 1. Activity Lock

- choose one activity type for the whole post
- decide whether ComfyUI is generating final line art or only source objects
- lock print-friendly line weight and whitespace first
- create 2 to 4 reference assets first

### Stage 2. Batch Generation

- generate only the assets needed for the worksheet
- keep silhouettes simple and printable
- reject images with cluttered edges or weak object separation

### Stage 3. Cleanup

- simplify noisy backgrounds
- keep subject silhouette readable
- remove tiny distracting details
- unify line weight and contrast
- reduce unnecessary color for non-coloring pages

### Stage 4. Export

- one web image for the post
- one higher-resolution source for later printable conversion
- one layout-ready asset set if the activity needs assembly

## Recommended ComfyUI Node Flow

Use a reusable graph with these stages:

1. checkpoint load
2. positive prompt encode
3. negative prompt encode
4. latent image setup
5. sampler
6. decode
7. optional upscale
8. optional cleanup pass
9. save image

If you need stronger consistency across the 10 images, add:

- style reference conditioning
- pose/composition control
- image-to-image refinement pass

## Prompt Structure

Keep prompts short and controlled.

### Base Prompt

- activity type
- main object set
- black and white line art or minimal-color printable style
- clean silhouette
- white background or low-clutter scene

### Negative Prompt

- tiny text
- watermark
- clutter
- heavy paint texture
- dense gradients
- extra limbs
- deformed hands
- muddy background
- photorealistic noise

## Approval Gate

Do not publish a post until:

- 10 images exist
- titles are short
- activity purpose is obvious
- non-coloring pages are printable without heavy color dependence
- no paragraph explanation is needed for the post to work
