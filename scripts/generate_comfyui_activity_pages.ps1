param(
  [string]$ComfyApi = 'http://127.0.0.1:8188',
  [string]$Checkpoint = 'sd_xl_base_1.0.safetensors',
  [int]$Steps = 18,
  [double]$Cfg = 7.0,
  [int]$Width = 1024,
  [int]$Height = 768,
  [string[]]$Themes = @(),
  [int]$ItemLimit = 0
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$assetRoot = Join-Path $repoRoot 'assets\img\playroom'
$comfyOutput = 'D:\ComfyUI-Easy-Install-Windows\ComfyUI-Easy-Install\ComfyUI\output'
$globalNegative = 'color, colored, pastel, watercolor, painted fill, gray shading, gradient fill, shadow, photorealistic, blurry, low contrast, messy composition, cluttered background, unreadable letters, broken maze, broken anatomy, text watermark, logo, frame, border'

$sets = @(
  @{
    Theme = 'coloring-spring'
    Style = 'preschool coloring worksheet page, black and white line art, bold clean outlines, wide coloring spaces, white background, printable activity page, no watermark'
    Items = @(
      @{ Name = '01'; Prompt = 'spring coloring worksheet page with cute rabbit, two tulips, small flowers, simple clouds and sun' }
      @{ Name = '02'; Prompt = 'spring coloring worksheet page with simple house, tulips, butterfly, open white background' }
      @{ Name = '03'; Prompt = 'spring coloring worksheet page with blossom tree, butterflies, grass line, big empty coloring areas' }
      @{ Name = '04'; Prompt = 'spring coloring worksheet page with flower basket and tulips, centered composition, black and white outline' }
      @{ Name = '05'; Prompt = 'spring coloring worksheet page with flower field and one large butterfly, simple black outlines' }
      @{ Name = '06'; Prompt = 'spring coloring worksheet page with rabbit on swing between clouds, bold outlines, white background' }
      @{ Name = '07'; Prompt = 'spring coloring worksheet page with tiny sprout cottage, flowers, simple sky, black and white' }
      @{ Name = '08'; Prompt = 'spring coloring worksheet page with petal path, tree, butterflies, open spaces for coloring' }
      @{ Name = '09'; Prompt = 'spring coloring worksheet page with pond, frog, flowers, black and white line art' }
      @{ Name = '10'; Prompt = 'spring coloring worksheet page with sleeping rabbit under two trees, simple grass line' }
    )
  }
  @{
    Theme = 'hidden-garden'
    Style = 'preschool hidden picture worksheet page, black and white line art, seek and find activity, clear scene, four target icons in bottom strip, bold outlines, white background, printable activity page, no watermark'
    Items = @(
      @{ Name = '01'; Prompt = 'garden hidden picture worksheet page with small house, tree, flowers, hidden flower, hidden apple, hidden bee, hidden shell, bottom strip showing target icons' }
      @{ Name = '02'; Prompt = 'garden hidden picture worksheet page with path, birdhouse, flowers, hidden butterfly, hidden flower, hidden fish, hidden apple, bottom strip target icons' }
      @{ Name = '03'; Prompt = 'garden hidden picture worksheet page with pots and tree, hidden flower, hidden shell, hidden fish, hidden apple, bottom icon strip' }
      @{ Name = '04'; Prompt = 'garden hidden picture worksheet page with fence and tree, hidden butterfly, hidden flower, hidden apple, hidden fish, bottom icon strip' }
      @{ Name = '05'; Prompt = 'garden hidden picture worksheet page with seed box scene, hidden apple, hidden flower, hidden shell, hidden fish, bottom icon strip' }
      @{ Name = '06'; Prompt = 'garden hidden picture worksheet page with apple tree scene, hidden apple, hidden butterfly, hidden flower, hidden shell, bottom icon strip' }
      @{ Name = '07'; Prompt = 'garden hidden picture worksheet page with pond corner scene, hidden flower, hidden fish, hidden shell, hidden apple, bottom icon strip' }
      @{ Name = '08'; Prompt = 'garden hidden picture worksheet page with bench scene, hidden apple, hidden flower, hidden fish, hidden butterfly, bottom icon strip' }
      @{ Name = '09'; Prompt = 'garden hidden picture worksheet page with flower path scene, hidden flower, hidden butterfly, hidden fish, hidden shell, bottom icon strip' }
      @{ Name = '10'; Prompt = 'garden hidden picture worksheet page with tree shade scene, hidden apple, hidden flower, hidden shell, hidden butterfly, bottom icon strip' }
    )
  }
  @{
    Theme = 'maze-rainy'
    Style = 'preschool maze worksheet page, black and white line art, bold rectangular maze, clear start and finish, simple theme icon, white background, printable activity page, no watermark'
    Items = @(
      @{ Name = '01'; Prompt = 'rainbow maze worksheet page, one large maze, black and white' }
      @{ Name = '02'; Prompt = 'rabbit maze worksheet page, one large maze, black and white' }
      @{ Name = '03'; Prompt = 'shell maze worksheet page, one large maze, black and white' }
      @{ Name = '04'; Prompt = 'balloon maze worksheet page, one large maze, black and white' }
      @{ Name = '05'; Prompt = 'fruit maze worksheet page, one large maze, black and white' }
      @{ Name = '06'; Prompt = 'star maze worksheet page, one large maze, black and white' }
      @{ Name = '07'; Prompt = 'dinosaur maze worksheet page, one large maze, black and white' }
      @{ Name = '08'; Prompt = 'kite maze worksheet page, one large maze, black and white' }
      @{ Name = '09'; Prompt = 'train maze worksheet page, one large maze, black and white' }
      @{ Name = '10'; Prompt = 'candy maze worksheet page, one large maze, black and white' }
    )
  }
  @{
    Theme = 'cut-paste-ocean'
    Style = 'preschool cut and paste worksheet page, black and white line art, top placement boxes and bottom dashed cut boxes, ocean theme, bold outlines, white background, printable activity page, no watermark'
    Items = @(
      @{ Name = '01'; Prompt = 'ocean cut and paste worksheet page with whale fish shell, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '02'; Prompt = 'ocean cut and paste worksheet page with fish coral starfish, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '03'; Prompt = 'ocean cut and paste worksheet page with octopus fish shell, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '04'; Prompt = 'ocean cut and paste worksheet page with turtle shell whale, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '05'; Prompt = 'ocean cut and paste worksheet page with starfish fish shell, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '06'; Prompt = 'ocean cut and paste worksheet page with submarine fish shell, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '07'; Prompt = 'ocean cut and paste worksheet page with shell starfish fish, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '08'; Prompt = 'ocean cut and paste worksheet page with coral fish shell, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '09'; Prompt = 'ocean cut and paste worksheet page with wave fish starfish, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
      @{ Name = '10'; Prompt = 'ocean cut and paste worksheet page with whale octopus fish, three placement boxes on top, three dashed cut boxes on bottom, black and white' }
    )
  }
  @{
    Theme = 'english-words'
    Style = 'preschool English worksheet page, black and white line art, very clear readable large letters, three handwriting trace rows, one simple object outline, white background, printable activity page, no watermark'
    Items = @(
      @{ Name = '01'; Prompt = 'English worksheet page with very clear readable capital A lowercase a and APPLE trace rows, one apple outline, black and white' }
      @{ Name = '02'; Prompt = 'English worksheet page with very clear readable capital B lowercase b and BALLOON trace rows, one balloon outline, black and white' }
      @{ Name = '03'; Prompt = 'English worksheet page with very clear readable capital C lowercase c and CAT trace rows, one cat outline, black and white' }
      @{ Name = '04'; Prompt = 'English worksheet page with very clear readable capital D lowercase d and DUCK trace rows, one duck outline, black and white' }
      @{ Name = '05'; Prompt = 'English worksheet page with very clear readable capital E lowercase e and EGG trace rows, one egg outline, black and white' }
      @{ Name = '06'; Prompt = 'English worksheet page with very clear readable capital F lowercase f and FISH trace rows, one fish outline, black and white' }
      @{ Name = '07'; Prompt = 'English worksheet page with very clear readable capital G lowercase g and GRAPES trace rows, one grapes outline, black and white' }
      @{ Name = '08'; Prompt = 'English worksheet page with very clear readable capital H lowercase h and HAT trace rows, one hat outline, black and white' }
      @{ Name = '09'; Prompt = 'English worksheet page with very clear readable capital I lowercase i and ICE CREAM trace rows, one ice cream outline, black and white' }
      @{ Name = '10'; Prompt = 'English worksheet page with very clear readable capital J lowercase j and JAM trace rows, one jam jar outline, black and white' }
    )
  }
  @{
    Theme = 'line-tracing'
    Style = 'preschool line tracing worksheet page, black and white line art, one large dotted path from left to right, clear start circle and finish circle, simple icon at each end, white background, printable activity page, no watermark'
    Items = @(
      @{ Name = '01'; Prompt = 'line tracing worksheet page, dotted curved path from flower to flower, start and finish circles, black and white' }
      @{ Name = '02'; Prompt = 'line tracing worksheet page, dotted curved path from cloud to sun, start and finish circles, black and white' }
      @{ Name = '03'; Prompt = 'line tracing worksheet page, dotted curved path from rabbit to tulip, start and finish circles, black and white' }
      @{ Name = '04'; Prompt = 'line tracing worksheet page, dotted curved path from star to balloon, start and finish circles, black and white' }
      @{ Name = '05'; Prompt = 'line tracing worksheet page, dotted curved path from butterfly to flower, start and finish circles, black and white' }
      @{ Name = '06'; Prompt = 'line tracing worksheet page, dotted curved path from fish to shell, start and finish circles, black and white' }
      @{ Name = '07'; Prompt = 'line tracing worksheet page, dotted curved path from duck to pond, start and finish circles, black and white' }
      @{ Name = '08'; Prompt = 'line tracing worksheet page, dotted curved path from apple to basket, start and finish circles, black and white' }
      @{ Name = '09'; Prompt = 'line tracing worksheet page, dotted curved path from hat to jam jar, start and finish circles, black and white' }
      @{ Name = '10'; Prompt = 'line tracing worksheet page, dotted curved path from whale to starfish, start and finish circles, black and white' }
    )
  }
)

function Wait-ComfyReady {
  param([string]$Uri)
  for ($i = 0; $i -lt 120; $i++) {
    try {
      $null = Invoke-RestMethod -Uri "$Uri/system_stats" -Method Get -TimeoutSec 3
      return
    } catch {
      Start-Sleep -Seconds 2
    }
  }
  throw "ComfyUI API is not reachable at $Uri"
}

function New-PromptGraph {
  param(
    [string]$CheckpointName,
    [string]$PositivePrompt,
    [string]$NegativePrompt,
    [string]$Prefix,
    [int]$Seed,
    [int]$StepCount,
    [double]$CfgScale,
    [int]$ImageWidth,
    [int]$ImageHeight
  )

  return @{
    '3' = @{
      class_type = 'KSampler'
      inputs = @{
        seed = $Seed
        steps = $StepCount
        cfg = $CfgScale
        sampler_name = 'dpmpp_2m'
        scheduler = 'karras'
        denoise = 1
        model = @('4', 0)
        positive = @('6', 0)
        negative = @('7', 0)
        latent_image = @('5', 0)
      }
    }
    '4' = @{
      class_type = 'CheckpointLoaderSimple'
      inputs = @{ ckpt_name = $CheckpointName }
    }
    '5' = @{
      class_type = 'EmptyLatentImage'
      inputs = @{ width = $ImageWidth; height = $ImageHeight; batch_size = 1 }
    }
    '6' = @{
      class_type = 'CLIPTextEncode'
      inputs = @{ text = $PositivePrompt; clip = @('4', 1) }
    }
    '7' = @{
      class_type = 'CLIPTextEncode'
      inputs = @{ text = $NegativePrompt; clip = @('4', 1) }
    }
    '8' = @{
      class_type = 'VAEDecode'
      inputs = @{ samples = @('3', 0); vae = @('4', 2) }
    }
    '9' = @{
      class_type = 'SaveImage'
      inputs = @{ filename_prefix = $Prefix; images = @('8', 0) }
    }
  }
}

function Invoke-ComfyGeneration {
  param([string]$Uri,[hashtable]$PromptGraph)

  $clientId = [guid]::NewGuid().ToString()
  $body = @{ prompt = $PromptGraph; client_id = $clientId } | ConvertTo-Json -Depth 20 -Compress
  $response = Invoke-RestMethod -Uri "$Uri/prompt" -Method Post -ContentType 'application/json' -Body $body
  $promptId = $response.prompt_id

  for ($i = 0; $i -lt 360; $i++) {
    Start-Sleep -Seconds 2
    $history = Invoke-RestMethod -Uri "$Uri/history/$promptId" -Method Get
    if ($history.$promptId) {
      if ($history.$promptId.status.status_str -ne 'success') {
        throw "Generation failed for prompt $promptId"
      }
      return $history.$promptId.outputs.'9'.images[0]
    }
  }

  throw "Timed out waiting for ComfyUI prompt $promptId"
}

Wait-ComfyReady -Uri $ComfyApi

$selectedSets = if ($Themes.Count -gt 0) {
  $sets | Where-Object { $Themes -contains $_.Theme }
} else {
  $sets
}

foreach ($set in $selectedSets) {
  $themeDir = Join-Path $assetRoot $set.Theme
  if (-not (Test-Path $themeDir)) {
    New-Item -ItemType Directory -Path $themeDir -Force | Out-Null
  }

  $items = if ($ItemLimit -gt 0) { $set.Items | Select-Object -First $ItemLimit } else { $set.Items }

  foreach ($item in $items) {
    $prefix = "activity_$($set.Theme)_$($item.Name)"
    $seed = Get-Random -Minimum 100000000 -Maximum 999999999
    $positive = "$($item.Prompt), $($set.Style)"
    $graph = New-PromptGraph -CheckpointName $Checkpoint -PositivePrompt $positive -NegativePrompt $globalNegative -Prefix $prefix -Seed $seed -StepCount $Steps -CfgScale $Cfg -ImageWidth $Width -ImageHeight $Height
    $image = Invoke-ComfyGeneration -Uri $ComfyApi -PromptGraph $graph
    $sourcePath = Join-Path $comfyOutput $image.filename
    $destPath = Join-Path $themeDir ($item.Name + '.png')
    Copy-Item -LiteralPath $sourcePath -Destination $destPath -Force
    Write-Output ("CREATED {0}" -f $destPath)
  }
}
