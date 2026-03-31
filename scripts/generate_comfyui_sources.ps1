param(
  [string]$ComfyApi = 'http://127.0.0.1:8188',
  [string]$Checkpoint = 'sd_xl_base_1.0.safetensors',
  [int]$Steps = 16,
  [double]$Cfg = 7.0,
  [int]$Width = 1024,
  [int]$Height = 768,
  [string[]]$Groups = @(),
  [int]$ItemLimit = 0
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$assetRoot = Join-Path $repoRoot 'assets\img\playroom\comfy-src'
$comfyOutput = 'D:\ComfyUI-Easy-Install-Windows\ComfyUI-Easy-Install\ComfyUI\output'
$negative = 'color, colored, gray fill, gradients, painted shading, watercolor, photorealistic, messy lines, clutter, watermark, logo, text paragraph, frame, border, blur, low contrast'

$groupsData = @(
  @{
    Group = 'icons'
    Style = 'isolated preschool printable line art icon, black and white coloring book outline, centered, white background, bold clean outline, no extra objects, no watermark'
    Items = @(
      @{ Name='flower'; Prompt='flower icon' }
      @{ Name='apple'; Prompt='apple icon' }
      @{ Name='butterfly'; Prompt='butterfly icon' }
      @{ Name='bee'; Prompt='bee icon' }
      @{ Name='fish'; Prompt='fish icon' }
      @{ Name='shell'; Prompt='shell icon' }
      @{ Name='starfish'; Prompt='starfish icon' }
      @{ Name='whale'; Prompt='whale icon' }
      @{ Name='octopus'; Prompt='octopus icon' }
      @{ Name='submarine'; Prompt='submarine icon' }
      @{ Name='cat'; Prompt='cat icon' }
      @{ Name='duck'; Prompt='duck icon' }
      @{ Name='egg'; Prompt='egg icon' }
      @{ Name='grapes'; Prompt='grapes icon' }
      @{ Name='hat'; Prompt='hat icon' }
      @{ Name='icecream'; Prompt='ice cream icon' }
      @{ Name='jam'; Prompt='jam jar icon' }
      @{ Name='rabbit'; Prompt='rabbit icon' }
      @{ Name='tulip'; Prompt='tulip flower icon' }
      @{ Name='sun'; Prompt='sun icon' }
      @{ Name='cloud'; Prompt='cloud icon' }
      @{ Name='basket'; Prompt='basket icon' }
    )
  }
  @{
    Group = 'coloring-spring'
    Style = 'preschool coloring worksheet scene, black and white line art, bold clean outlines, wide coloring spaces, white background, no text, no watermark'
    Items = @(
      @{ Name='01'; Prompt='cute rabbit in spring flowers scene' }
      @{ Name='02'; Prompt='simple spring house with tulips scene' }
      @{ Name='03'; Prompt='blossom tree with butterflies scene' }
      @{ Name='04'; Prompt='flower basket spring scene' }
      @{ Name='05'; Prompt='spring flower field scene' }
      @{ Name='06'; Prompt='rabbit swing spring scene' }
      @{ Name='07'; Prompt='sprout cottage spring scene' }
      @{ Name='08'; Prompt='petal path spring scene' }
      @{ Name='09'; Prompt='spring pond scene' }
      @{ Name='10'; Prompt='sleeping rabbit forest scene' }
    )
  }
  @{
    Group = 'hidden-garden'
    Style = 'simple preschool garden worksheet scene, black and white line art, cottage path tree fence and flowers, open whitespace, no text, no watermark'
    Items = @(
      @{ Name='01'; Prompt='simple garden scene with cottage and path' }
      @{ Name='02'; Prompt='simple garden scene with birdhouse path and flowers' }
      @{ Name='03'; Prompt='simple garden scene with flower pots and tree' }
      @{ Name='04'; Prompt='simple garden scene with fence and flowers' }
      @{ Name='05'; Prompt='simple garden scene with seed box and flowers' }
      @{ Name='06'; Prompt='simple garden scene with apple tree and path' }
      @{ Name='07'; Prompt='simple garden pond corner scene' }
      @{ Name='08'; Prompt='simple garden bench scene with flowers' }
      @{ Name='09'; Prompt='simple garden flower path scene' }
      @{ Name='10'; Prompt='simple garden tree shade scene' }
    )
  }
)

function Wait-ComfyReady {
  param([string]$Uri)
  for ($i = 0; $i -lt 120; $i++) {
    try { $null = Invoke-RestMethod -Uri "$Uri/system_stats" -Method Get -TimeoutSec 3; return } catch { Start-Sleep -Seconds 2 }
  }
  throw "ComfyUI API is not reachable at $Uri"
}

function New-PromptGraph {
  param([string]$CheckpointName,[string]$PositivePrompt,[string]$NegativePrompt,[string]$Prefix,[int]$Seed,[int]$StepCount,[double]$CfgScale,[int]$ImageWidth,[int]$ImageHeight)
  return @{
    '3'=@{ class_type='KSampler'; inputs=@{ seed=$Seed; steps=$StepCount; cfg=$CfgScale; sampler_name='dpmpp_2m'; scheduler='karras'; denoise=1; model=@('4',0); positive=@('6',0); negative=@('7',0); latent_image=@('5',0) } }
    '4'=@{ class_type='CheckpointLoaderSimple'; inputs=@{ ckpt_name=$CheckpointName } }
    '5'=@{ class_type='EmptyLatentImage'; inputs=@{ width=$ImageWidth; height=$ImageHeight; batch_size=1 } }
    '6'=@{ class_type='CLIPTextEncode'; inputs=@{ text=$PositivePrompt; clip=@('4',1) } }
    '7'=@{ class_type='CLIPTextEncode'; inputs=@{ text=$NegativePrompt; clip=@('4',1) } }
    '8'=@{ class_type='VAEDecode'; inputs=@{ samples=@('3',0); vae=@('4',2) } }
    '9'=@{ class_type='SaveImage'; inputs=@{ filename_prefix=$Prefix; images=@('8',0) } }
  }
}

function Invoke-ComfyGeneration {
  param([string]$Uri,[hashtable]$PromptGraph)
  $clientId=[guid]::NewGuid().ToString()
  $body=@{ prompt=$PromptGraph; client_id=$clientId } | ConvertTo-Json -Depth 20 -Compress
  $response=Invoke-RestMethod -Uri "$Uri/prompt" -Method Post -ContentType 'application/json' -Body $body
  $promptId=$response.prompt_id
  for($i=0;$i -lt 360;$i++){
    Start-Sleep -Seconds 2
    $history=Invoke-RestMethod -Uri "$Uri/history/$promptId" -Method Get
    if($history.$promptId){
      if($history.$promptId.status.status_str -ne 'success'){ throw "Generation failed for prompt $promptId" }
      return $history.$promptId.outputs.'9'.images[0]
    }
  }
  throw "Timed out waiting for ComfyUI prompt $promptId"
}

Wait-ComfyReady -Uri $ComfyApi
$selected = if($Groups.Count -gt 0){ $groupsData | Where-Object { $Groups -contains $_.Group } } else { $groupsData }

foreach($group in $selected){
  $dir = Join-Path $assetRoot $group.Group
  if(-not (Test-Path $dir)){ New-Item -ItemType Directory -Path $dir -Force | Out-Null }
  $items = if($ItemLimit -gt 0){ $group.Items | Select-Object -First $ItemLimit } else { $group.Items }
  foreach($item in $items){
    $prefix = "src_$($group.Group)_$($item.Name)"
    $seed = Get-Random -Minimum 100000000 -Maximum 999999999
    $positive = "$($item.Prompt), $($group.Style)"
    $graph = New-PromptGraph -CheckpointName $Checkpoint -PositivePrompt $positive -NegativePrompt $negative -Prefix $prefix -Seed $seed -StepCount $Steps -CfgScale $Cfg -ImageWidth $Width -ImageHeight $Height
    $image = Invoke-ComfyGeneration -Uri $ComfyApi -PromptGraph $graph
    $sourcePath = Join-Path $comfyOutput $image.filename
    $destPath = Join-Path $dir ($item.Name + '.png')
    Copy-Item -LiteralPath $sourcePath -Destination $destPath -Force
    Write-Output ("CREATED {0}" -f $destPath)
  }
}
