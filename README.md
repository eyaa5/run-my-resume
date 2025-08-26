# run-my-resume

A tiny Windows tool to analyze a PDF resume by **dragging & dropping** it onto a launcher.  
Converts the PDF to text (via `pdftotext`), extracts email/phone/skills, and writes a friendly summary to Markdown and JSON.

## ✨ Features
- Drag-and-drop `.pdf` onto `RunMyResume.bat`
- Extracts **email**, **phone**, and top **skills**
- Saves:
  - `cv.analysis.md` – human-readable summary
  - `cv.analysis.json` – machine-readable
- Runs locally (no internet needed)

## ⚙️ Requirements
- Windows 10/11
- PowerShell 5+ (built-in)
- Poppler `pdftotext` (auto-installs on first run via `winget`)

## 🚀 Quick Start
1. **Clone** this repo (GitHub Desktop or `git clone`).
2. Put your resume PDF in the folder (e.g., `cv.pdf`).
3. **Option A – Drag & Drop:** drag your PDF onto `RunMyResume.bat`.
4. **Option B – PowerShell:**
   ```powershell
   # from the repo folder
   powershell -NoProfile -ExecutionPolicy Bypass -File .\RunResume.ps1 -File ".\cv.pdf"
