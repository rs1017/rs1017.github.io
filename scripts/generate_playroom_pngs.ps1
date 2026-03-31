param(
  [string]$ComfyApi = "http://127.0.0.1:8188",
  [string]$Checkpoint = "sd_xl_base_1.0.safetensors",
  [int]$Steps = 12,
  [double]$Cfg = 6.5,
  [int]$Width = 1024,
  [int]$Height = 768
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$assetRoot = Join-Path $repoRoot "assets\\img\\playroom"
$comfyOutput = "D:\ComfyUI-Easy-Install-Windows\ComfyUI-Easy-Install\ComfyUI\output"

$defaultStyle = "preschool printable worksheet source art, black and white line art, bold clean outlines, simple shapes, white background, high contrast, no text, no watermark"
$negative = "text, watermark, logo, extra limbs, malformed anatomy, photorealistic noise, dark horror mood, cluttered background, blurry, frame, border, painterly shading, heavy gradients"

$sets = @(
  @{
    Theme = "spring"
    Style = "preschool coloring page, black and white line art, bold clean outlines, wide coloring spaces, white background, no text, no watermark"
    Items = @(
      @{ Name = "01"; Prompt = "spring rabbit with large tulips" }
      @{ Name = "02"; Prompt = "tulip hill with simple rabbit house" }
      @{ Name = "03"; Prompt = "butterflies around a blossom tree" }
      @{ Name = "04"; Prompt = "flower basket on a garden path" }
      @{ Name = "05"; Prompt = "wide spring field with clouds" }
      @{ Name = "06"; Prompt = "rabbit on a cloud swing" }
      @{ Name = "07"; Prompt = "small sprout cottage" }
      @{ Name = "08"; Prompt = "petals along a walking path" }
      @{ Name = "09"; Prompt = "spring pond with flowers" }
      @{ Name = "10"; Prompt = "sleepy rabbit in a forest clearing" }
    )
  }
  @{
    Theme = "garden"
    Style = "preschool hidden picture worksheet scene, black and white line art, many clear objects, simple printable outlines, low clutter background, no text, no watermark"
    Items = @(
      @{ Name = "01"; Prompt = "garden gate scene with hidden flower tools" }
      @{ Name = "02"; Prompt = "garden path with birdhouse and hidden leaves" }
      @{ Name = "03"; Prompt = "flower fence with small hidden bugs" }
      @{ Name = "04"; Prompt = "watering can scene with hidden seeds" }
      @{ Name = "05"; Prompt = "pond corner with hidden butterflies" }
      @{ Name = "06"; Prompt = "fruit tree scene with hidden apples" }
      @{ Name = "07"; Prompt = "round pots with hidden garden items" }
      @{ Name = "08"; Prompt = "arched garden gate with hidden flowers" }
      @{ Name = "09"; Prompt = "bench scene with hidden tools" }
      @{ Name = "10"; Prompt = "tree shade scene with hidden petals" }
    )
  }
  @{
    Theme = "ocean"
    Style = "preschool cut and paste worksheet source objects, isolated sea animals, black and white line art, clean cuttable silhouettes, white background, no text, no watermark"
    Items = @(
      @{ Name = "01"; Prompt = "single whale cuttable silhouette" }
      @{ Name = "02"; Prompt = "single fish cuttable silhouette" }
      @{ Name = "03"; Prompt = "single shell cuttable silhouette" }
      @{ Name = "04"; Prompt = "single octopus cuttable silhouette" }
      @{ Name = "05"; Prompt = "single coral cuttable silhouette" }
      @{ Name = "06"; Prompt = "single dolphin cuttable silhouette" }
      @{ Name = "07"; Prompt = "single seahorse cuttable silhouette" }
      @{ Name = "08"; Prompt = "single starfish cuttable silhouette" }
      @{ Name = "09"; Prompt = "single submarine cuttable silhouette" }
      @{ Name = "10"; Prompt = "single wave cuttable silhouette" }
    )
  }
  @{
    Theme = "maze"
    Style = "preschool maze worksheet, bold black maze path, clear entrance and exit, simple theme icons, black and white printable line art, white background, no text, no watermark"
    Items = @(
      @{ Name = "01"; Prompt = "rainbow themed maze page" }
      @{ Name = "02"; Prompt = "rabbit themed maze page" }
      @{ Name = "03"; Prompt = "shell themed maze page" }
      @{ Name = "04"; Prompt = "balloon themed maze page" }
      @{ Name = "05"; Prompt = "fruit themed maze page" }
      @{ Name = "06"; Prompt = "star themed maze page" }
      @{ Name = "07"; Prompt = "dinosaur themed maze page" }
      @{ Name = "08"; Prompt = "kite themed maze page" }
      @{ Name = "09"; Prompt = "train themed maze page" }
      @{ Name = "10"; Prompt = "candy themed maze page" }
    )
  }
)

function Wait-ComfyReady {
  param([string]$Uri)
  for ($i = 0; $i -lt 60; $i++) {
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
    "3" = @{
      class_type = "KSampler"
      inputs = @{
        seed = $Seed
        steps = $StepCount
        cfg = $CfgScale
        sampler_name = "dpmpp_2m"
        scheduler = "karras"
        denoise = 1
        model = @("4", 0)
        positive = @("6", 0)
        negative = @("7", 0)
        latent_image = @("5", 0)
      }
    }
    "4" = @{
      class_type = "CheckpointLoaderSimple"
      inputs = @{ ckpt_name = $CheckpointName }
    }
    "5" = @{
      class_type = "EmptyLatentImage"
      inputs = @{ width = $ImageWidth; height = $ImageHeight; batch_size = 1 }
    }
    "6" = @{
      class_type = "CLIPTextEncode"
      inputs = @{ text = $PositivePrompt; clip = @("4", 1) }
    }
    "7" = @{
      class_type = "CLIPTextEncode"
      inputs = @{ text = $NegativePrompt; clip = @("4", 1) }
    }
    "8" = @{
      class_type = "VAEDecode"
      inputs = @{ samples = @("3", 0); vae = @("4", 2) }
    }
    "9" = @{
      class_type = "SaveImage"
      inputs = @{ filename_prefix = $Prefix; images = @("8", 0) }
    }
  }
}

function Invoke-ComfyGeneration {
  param(
    [string]$Uri,
    [hashtable]$PromptGraph
  )

  $clientId = [guid]::NewGuid().ToString()
  $body = @{ prompt = $PromptGraph; client_id = $clientId } | ConvertTo-Json -Depth 20 -Compress
  $response = Invoke-RestMethod -Uri "$Uri/prompt" -Method Post -ContentType "application/json" -Body $body
  $promptId = $response.prompt_id

  for ($i = 0; $i -lt 300; $i++) {
    Start-Sleep -Seconds 2
    $history = Invoke-RestMethod -Uri "$Uri/history/$promptId" -Method Get
    if ($history.$promptId) {
      if ($history.$promptId.status.status_str -ne "success") {
        throw "Generation failed for prompt $promptId"
      }
      return $history.$promptId.outputs."9".images[0]
    }
  }

  throw "Timed out waiting for ComfyUI prompt $promptId"
}

Wait-ComfyReady -Uri $ComfyApi

foreach ($set in $sets) {
  $themeDir = Join-Path $assetRoot $set.Theme
  if (-not (Test-Path $themeDir)) {
    New-Item -ItemType Directory -Path $themeDir -Force | Out-Null
  }

  foreach ($item in $set.Items) {
    $prefix = "playroom_$($set.Theme)_$($item.Name)"
    $seed = Get-Random -Minimum 100000000 -Maximum 999999999
    $style = if ($set.ContainsKey("Style")) { $set.Style } else { $defaultStyle }
    $positive = "$($item.Prompt), $style"
    $graph = New-PromptGraph -CheckpointName $Checkpoint -PositivePrompt $positive -NegativePrompt $negative -Prefix $prefix -Seed $seed -StepCount $Steps -CfgScale $Cfg -ImageWidth $Width -ImageHeight $Height
    $image = Invoke-ComfyGeneration -Uri $ComfyApi -PromptGraph $graph

    $sourcePath = Join-Path $comfyOutput $image.filename
    $destPath = Join-Path $themeDir ($item.Name + ".png")
    Copy-Item -LiteralPath $sourcePath -Destination $destPath -Force
    Write-Output ("CREATED {0}" -f $destPath)
  }
}
