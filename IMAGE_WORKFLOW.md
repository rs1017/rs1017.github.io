# Preschool Image Workflow

## Goal

Each gallery post ships with:

- 1 theme
- 10 images minimum
- 1 short title per image

No long explanations inside the gallery itself.

## Production Order

1. Pick one theme
2. Write a 10-shot list
3. Generate a base image set
4. Select the strongest 10
5. Export web images
6. Insert them into one gallery page

## Theme Rules

- One post should stay visually consistent
- Color palette should stay within one family
- Character shape language should stay consistent
- Background noise should stay low enough for preschool readability

## 10-Shot List Template

Use a fixed structure so every post is fast to assemble.

1. hero image
2. close subject
3. wide scene
4. object focus
5. action scene
6. alternate mood
7. alternate composition
8. simplified scene
9. pattern scene
10. closing scene

## ComfyUI Workflow Direction

### Stage 1. Style Lock

- choose one model for the whole post
- fix one palette direction
- fix one subject direction
- create 2 to 4 reference images first

### Stage 2. Batch Generation

- generate 20 to 40 candidates
- keep camera angle and composition variety
- reject images with cluttered edges or weak silhouettes

### Stage 3. Cleanup

- simplify noisy backgrounds
- keep subject silhouette readable
- remove tiny distracting details
- unify line weight and contrast

### Stage 4. Export

- one web image for gallery use
- one higher-resolution source for later printable conversion

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

- subject
- environment
- preschool-friendly illustration
- clean silhouette
- bright paper-friendly palette

### Negative Prompt

- tiny text
- watermark
- clutter
- extra limbs
- deformed hands
- muddy background
- photorealistic noise

## Approval Gate

Do not publish a post until:

- 10 images exist
- titles are short
- theme is visually consistent
- no paragraph explanation is needed for the gallery to work
