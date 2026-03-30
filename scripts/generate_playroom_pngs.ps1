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
$comfyOutput = "D:\\ComfyUI-Easy-Install-Windows\\ComfyUI-Easy-Install\\ComfyUI\\output"

$style = "preschool picture book illustration, detailed whimsical environment, charming children's art, bright pastel palette, clean silhouette, gentle daylight, paper-friendly composition, no text, no watermark"
$negative = "text, watermark, logo, extra limbs, malformed anatomy, photorealistic noise, dark horror mood, cluttered background, blurry, frame, border"

$sets = @(
  @{
    Theme = "spring"
    Items = @(
      @{ Name = "01"; Prompt = "white rabbit walking through a spring flower field, tulips and daisies, warm breeze" }
      @{ Name = "02"; Prompt = "rolling tulip hill under a soft spring sky, tiny rabbit in distance" }
      @{ Name = "03"; Prompt = "butterflies circling a blossom tree in spring meadow" }
      @{ Name = "04"; Prompt = "basket of flowers beside a rabbit on grass path" }
      @{ Name = "05"; Prompt = "sunny flower field with playful rabbit and soft clouds" }
      @{ Name = "06"; Prompt = "rabbit on a cloud swing above pastel spring garden" }
      @{ Name = "07"; Prompt = "small sprout cottage tucked into a spring grove" }
      @{ Name = "08"; Prompt = "petals falling along a spring walking path" }
      @{ Name = "09"; Prompt = "quiet spring pond with flowers and rabbit nearby" }
      @{ Name = "10"; Prompt = "rabbit napping in a peaceful spring forest clearing" }
    )
  }
  @{
    Theme = "garden"
    Items = @(
      @{ Name = "01"; Prompt = "secret garden entrance with flowers and hidden playful details" }
      @{ Name = "02"; Prompt = "garden path leading to a birdhouse among leaves" }
      @{ Name = "03"; Prompt = "flower fence around a cheerful little garden" }
      @{ Name = "04"; Prompt = "watering can in a bright child-friendly garden scene" }
      @{ Name = "05"; Prompt = "butterfly resting in a quiet corner of the garden" }
      @{ Name = "06"; Prompt = "fruit leaves and rounded shrubs in a playful garden" }
      @{ Name = "07"; Prompt = "round flower pots arranged in a sunny garden" }
      @{ Name = "08"; Prompt = "arched garden gate surrounded by blooms" }
      @{ Name = "09"; Prompt = "small green hedge maze in a cute family garden" }
      @{ Name = "10"; Prompt = "cool flower shade under a tree in a peaceful garden" }
    )
  }
  @{
    Theme = "ocean"
    Items = @(
      @{ Name = "01"; Prompt = "friendly ocean animals swimming together in bright blue water" }
      @{ Name = "02"; Prompt = "coral path under the sea with colorful fish" }
      @{ Name = "03"; Prompt = "gentle whale releasing a soft stream of bubbles" }
      @{ Name = "04"; Prompt = "shells resting on warm sandy ocean floor" }
      @{ Name = "05"; Prompt = "starfish on smooth rocks under shallow water" }
      @{ Name = "06"; Prompt = "curving wave tunnel with playful fish" }
      @{ Name = "07"; Prompt = "seahorses drifting through an underwater forest" }
      @{ Name = "08"; Prompt = "sea turtle strolling through a calm reef scene" }
      @{ Name = "09"; Prompt = "bright yellow fish in a simple cheerful ocean setting" }
      @{ Name = "10"; Prompt = "sleepy underwater scene with soft resting sea animals" }
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
    $positive = "$($item.Prompt), $style"
    $graph = New-PromptGraph -CheckpointName $Checkpoint -PositivePrompt $positive -NegativePrompt $negative -Prefix $prefix -Seed $seed -StepCount $Steps -CfgScale $Cfg -ImageWidth $Width -ImageHeight $Height
    $image = Invoke-ComfyGeneration -Uri $ComfyApi -PromptGraph $graph

    $sourcePath = Join-Path $comfyOutput $image.filename
    $destPath = Join-Path $themeDir ($item.Name + ".png")
    Copy-Item -LiteralPath $sourcePath -Destination $destPath -Force
    Write-Output ("CREATED {0}" -f $destPath)
  }
}
