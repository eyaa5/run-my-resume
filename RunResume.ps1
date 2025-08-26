param([Parameter(Mandatory=$true)][string]$File)

# 1) HIER deine echte API-Basis-URL einsetzen:
$API = "https://<dein-endpunkt>/v1"

if (-not (Test-Path $File)) { throw "File not found: $File" }

# 2) Datei hochladen (ingest)
$b64   = [Convert]::ToBase64String([IO.File]::ReadAllBytes($File))
$fname = [IO.Path]::GetFileName($File)
$body  = @{ filename = $fname; content_b64 = $b64 } | ConvertTo-Json
$ingest = Invoke-RestMethod -Method Post -Uri "$API/ingest" -ContentType 'application/json' -Body $body
$rid = $ingest.id

# 3) Analyse starten
Invoke-RestMethod -Method Post -Uri "$API/analyze" -ContentType 'application/json' -Body (@{ id = $rid; filename = $fname } | ConvertTo-Json) | Out-Null

# 4) Ergebnis holen
$res = Invoke-RestMethod -Method Get -Uri "$API/resume/$rid"

# 5) Sidecar-Dateien neben deine PDF schreiben
$folder   = Split-Path -Parent $File
$baseName = [IO.Path]::GetFileNameWithoutExtension($File)
$jsonPath = Join-Path $folder "$baseName.analysis.json"
$mdPath   = Join-Path $folder "$baseName.analysis.md"

$res | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 $jsonPath

$md = @"
**Resume ID:** $($res.id)

## Summary
$($res.analysis.summary)

## Skills
$([string]::Join(", ", $res.analysis.skills))

## Highlights
$($res.analysis.bullets | ForEach-Object { "- $_" } | Out-String)
"@
$md | Set-Content -Encoding utf8 $mdPath

# 6) Hübsche Konsolen-Ausgabe
"---- SUMMARY ----"
$res.analysis.summary
"---- SKILLS ----"
$res.analysis.skills -join ", "
"---- HIGHLIGHTS ----"
$res.analysis.bullets | ForEach-Object { "- $_" }

# 7) Objekt zurückgeben (nützlich für Skripting)
return $res
