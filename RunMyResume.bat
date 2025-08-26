@echo off
setlocal
if "%~1"=="" (
  echo Drag a PDF onto this file to analyze.
  pause
  exit /b
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Documents\RunResumeSidecar.ps1" -File "%~1"
