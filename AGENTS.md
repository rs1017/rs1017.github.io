# Project Instructions

This repository is an activity-first preschool printable project.

## Project Purpose

- The goal is not to publish finished appreciation artwork.
- The goal is to publish preschool printable activities with a clear task.
- Every post must give the child something to do: hidden picture, coloring, maze, tracing, cut-and-paste, matching, counting, English study, or similar worksheet play.
- If a page is only "pretty pictures", it is off-direction and should be reworked or removed.

## Content Direction

- Keep the standard Jekyll blog structure working.
- Do not turn the site into a text-heavy blog.
- Images are the main content.
- Each image should have one short title.
- Each post page must contain at least 10 inserted images.
- Do not add explanatory paragraphs to gallery pages or artwork pages unless the user explicitly asks for them.
- If a page feels text-heavy, remove text before adding anything else.
- Each post should stay on one worksheet purpose only.
- Keep instructions short and functional only when the activity requires them.

## Visual Rules

- Prefer large visuals over lists, summaries, or article-style layouts.
- Keep the Chirpy blog home, categories, tags, and archives available unless the user explicitly asks to remove them.
- The homepage can be a blog feed, but preview images should stay prominent.
- One post preview should still favor one image + one short title.
- Post pages should feel like image collections, not articles.
- Keep supporting UI minimal: home link, print/download link, short labels only when necessary.
- Except for coloring pages, images should usually be line art, black-and-white, or minimal-color printable layouts.
- Do not use fully rendered colorful illustration sets for hidden-picture, maze, tracing, matching, or English worksheets.
- For printable pages, prefer white backgrounds over dark or filled backgrounds.
- Avoid heavy black fill areas or overly thick dark masses that waste printer ink.
- Coloring pages should keep wide open spaces for coloring, not dense black regions.

## Preschool Focus

- Content should feel friendly, bright, simple, and suitable for preschool or early elementary children.
- Favor themes like animals, seasons, shapes, tracing, mazes, hidden pictures, counting, and cut-and-paste activities.
- Use compositions that can later map cleanly to printable worksheets.

## Activity Types

- Hidden picture
- Coloring page
- Maze
- Tracing
- Cut-and-paste
- Matching
- Counting
- Alphabet / number worksheet
- English word study
- Spot the difference
- Connect the dots
- Shadow match

## Topic Bank

Use these as preferred post candidates before inventing new directions.

1. Spring flower coloring
2. Farm animal coloring
3. Dinosaur coloring
4. Vehicle coloring
5. Fruit coloring
6. Insect coloring
7. Weather coloring
8. Alphabet coloring
9. Number coloring
10. Shape coloring
11. Garden dense search scene
12. Zoo dense search scene
13. Ocean dense search scene
14. Kitchen dense search scene
15. Classroom dense search scene
16. Playground dense search scene
17. Forest dense search scene
18. Rainy day dense search scene
19. Dinosaur dense search scene
20. Space dense search scene
21. Rainbow maze
22. Rabbit maze
23. Ocean maze
24. Dinosaur maze
25. Farm maze
26. Space maze
27. Candy maze
28. Train maze
29. Flower maze
30. Weather maze
31. Line tracing basics
32. Curve tracing
33. Zigzag tracing
34. Shape tracing
35. Alphabet tracing
36. Number tracing
37. Name tracing blanks
38. Straight-line scissors practice
39. Curved-line scissors practice
40. Cut-and-paste animals
41. Cut-and-paste sea creatures
42. Cut-and-paste shapes
43. Shadow matching
44. Same and different
45. Count, trace, and color review
46. Number matching and ten-frame review
47. Alphabet picture match worksheet
48. English word trace and match worksheet
49. Connect the dots
50. Spot the difference

## Image Workflow

- Absolute rule: never create final illustration assets by arbitrary code drawing or SVG generation.
- Absolute rule: final characters, objects, scenes, and decorative artwork must come from ComfyUI generation or ComfyUI-generated source images.
- If an illustration was not made through ComfyUI, do not publish it. Remove it or replace it with a ComfyUI-made version.
- Layout assembly is allowed.
- Code or non-ComfyUI steps may add worksheet text, tracing guides, answer boxes, cut lines, labels, and layout framing.
- Code or non-ComfyUI steps must not invent the main illustration itself.
- Before starting any new content or code work, check whether the latest build or deploy failed.
- If the latest build failed, treat fixing or accounting for that failure as the first step before doing more content work.
- Do not use bulk generation just to save time.
- Work one image at a time, validate it, then move to the next image.
- If duplicate-looking images appear, stop and replace them before continuing.
- Define an activity list of at least 10 images before building a post.
- Keep one theme per post and one short title per image.
- Prefer reusable generation workflows and asset pipelines over manual one-by-one image making.
- Do not create final worksheet assets as SVG.
- Final published worksheet images must be raster files such as PNG.
- Use ComfyUI for final illustration generation and for source generation.
- For hidden picture and coloring, generated art still needs printable cleanup and should not default to fully painted scenes.
- When prompting or cleaning worksheet images, bias toward white paper backgrounds, thin-to-medium clean outlines, and printer-friendly line density.
- For coloring pages, prefer prompt words such as `drawing`, `line drawing`, `outline drawing`, `ink drawing`, and `monochrome drawing`.
- Do not rely on `coloring page` alone; pair it with explicit line-art wording.
- Avoid prompt words such as `render`, `cinematic`, `glossy`, `shaded`, `colored`, `panel`, and `character sheet` for printable coloring pages.
- If text-to-image keeps drifting into grids, sheets, collages, or repeated objects, stop and switch workflow instead of retrying the same prompt family.
- For high-quality coloring pages, prefer `high-quality original character image -> line cleanup / monochrome conversion -> printable page` over unstable text-only generation.

## Worksheet Quality Rules

### Counting

- Never publish counting pages that only show 1 to 10 copies of the same object.
- A counting worksheet must combine at least 3 learning actions on one A4 page.
- Valid counting actions: count the scene, trace the numeral, trace the number word, circle the correct answer, fill a ten-frame, count and color, compare more/less, draw more to make N, or match group to number.
- Counting pages should use a small scene or grouped context, not isolated repeated icons only.

### English

- Never publish an English worksheet that uses an entire A4 page for one word only.
- An English worksheet must combine at least 3 learning actions on one A4 page.
- Valid English actions: large picture + word tracing, uppercase/lowercase box, picture-word matching, beginning-sound task, cut-and-paste letters, or short sentence frame.
- English pages need a strong hero image plus supporting exercises; do not use a tiny icon alone.

### Tracing

- Never publish a tracing page that spends a full A4 page on a single line.
- A tracing worksheet should include 6 to 12 trace actions on the page.
- Mix warm-up strokes, shape tracing, path tracing, and a small finish-the-picture trace block.

### Mazes

- Maze difficulty must be much higher than the current simple repository mazes.
- A single A4 maze should target at least 35 decision points, 12 dead-end clusters, and 3 false-route groups.
- Avoid single-corridor or nearly linear mazes.

### Cut-and-Paste

- Prefer paper doll, puppet, dress-up, or build-a-character worksheets over loose object cut-and-paste pages.
- A cut-and-paste set should include a base body or puppet, 4 to 8 cut pieces, and clear placement guides.
- Two-page sets are preferred when the activity is character assembly.

### Hidden Picture

- Do not publish the old low-density hidden-picture format.
- Future hidden-picture pages must follow a Where's Wally style dense-scene search format.
- A hidden-picture page must include a crowded main scene, target thumbnail strip, strong distractors, and real search difficulty.

