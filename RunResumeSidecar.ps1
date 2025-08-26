param([Parameter(Mandatory=$true)][string]$File)

$script = Join-Path $env:USERPROFILE "Documents\RunResume.ps1"
if (-not (Test-Path $script)) { throw "Analyzer not found: $script" }
if (-not (Test-Path $File))   { throw "PDF not found: $File"   }

# run analyzer
$r = & $script -File $File
if (-not $r) { throw "Analyzer returned nothing." }

# sidecar paths
$folder    = Split-Path -Parent $File
$baseName  = [IO.Path]::GetFileNameWithoutExtension($File)
$jsonPath  = Join-Path $folder  "$baseName.analysis.json"
$mdPath    = Join-Path $folder  "$baseName.analysis.md"

# save JSON
$r | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 $jsonPath

# save Markdown
$md = @"
**Resume ID:** $($r.id)

## Summary
$($r.analysis.summary)

## Contact
$(@{ $true = "**Email:** $($r.analysis.email)" }[$([string]::IsNullOrWhiteSpace($r.analysis.email) -eq $false)])
$(@{ $true = "**Phone:** $($r.analysis.phone)" }[$([string]::IsNullOrWhiteSpace($r.analysis.phone) -eq $false)])

## Skills
$([string]::Join(", ", $r.analysis.skills))

## Highlights
$($r.analysis.bullets | ForEach-Object { "- $_" } | Out-String)
"@

$md | Set-Content -Encoding utf8 $mdPath

# open results
Start-Process notepad $jsonPath
Start-Process notepad $mdPath

return $r
