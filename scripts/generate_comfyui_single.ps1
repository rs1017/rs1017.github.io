param(
  [Parameter(Mandatory = $true)]
  [string]$Prompt,

  [Parameter(Mandatory = $true)]
  [string]$OutputPath,

  [string]$ComfyApi = "http://127.0.0.1:8188",
  [string]$Checkpoint = "animagine-xl-4.0-opt.safetensors",
  [int]$Steps = 22,
  [double]$Cfg = 7.5,
  [int]$Width = 1024,
  [int]$Height = 768
)

$ErrorActionPreference = "Stop"

$comfyOutput = "D:\ComfyUI-Easy-Install-Windows\ComfyUI-Easy-Install\ComfyUI\output"
$negative = "copyright character, logo, watermark, text paragraph, letters, words, filled black background, heavy black fill, dense shadows, gradient fill, color, colored, photorealistic, painterly shading, cluttered background, busy scene, duplicate limbs, blur, dark background, comic panel, frame"

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

  for ($i = 0; $i -lt 360; $i++) {
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

$seed = Get-Random -Minimum 100000000 -Maximum 999999999
$prefix = "single_" + [guid]::NewGuid().ToString("N")
$graph = New-PromptGraph -CheckpointName $Checkpoint -PositivePrompt $Prompt -NegativePrompt $negative -Prefix $prefix -Seed $seed -StepCount $Steps -CfgScale $Cfg -ImageWidth $Width -ImageHeight $Height
$image = Invoke-ComfyGeneration -Uri $ComfyApi -PromptGraph $graph

$sourcePath = Join-Path $comfyOutput $image.filename
$destDir = Split-Path -Parent $OutputPath
if (-not (Test-Path $destDir)) {
  New-Item -ItemType Directory -Path $destDir -Force | Out-Null
}
Copy-Item -LiteralPath $sourcePath -Destination $OutputPath -Force
Write-Output ("CREATED {0}" -f $OutputPath)

