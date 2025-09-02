from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from engine.analyze import analyze_resume
from engine.enhance import generate_package
import tempfile, os

app = FastAPI()

STYLE = """
<style>
  body { font-family: Arial, sans-serif; margin: 40px; background:#f9fafb; color:#222; }
  h2 { color:#2563eb; }
  h3 { margin-top:20px; color:#111827; }
  .score { font-size:20px; font-weight:bold; color:#16a34a; }
  textarea { width:100%; padding:8px; }
  .box { background:white; padding:20px; margin:20px 0; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1);}
  .btn { background:#2563eb; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; }
  .btn:hover { background:#1d4ed8; }
  ul { line-height:1.6; }
</style>
"""

@app.get("/")
def form_page():
    return HTMLResponse(f"""
    <html>
      <head>{STYLE}</head>
      <body>
        <h2>🚀 CareerForge Demo</h2>
        <div class="box">
          <form action="/analyze" enctype="multipart/form-data" method="post">
            <p><b>Upload your CV (PDF):</b><br><input type="file" name="file"></p>
            <p><b>Paste job description:</b><br>
            <textarea name="job_text" rows="10"></textarea></p>
            <input type="submit" class="btn" value="Analyze">
          </form>
        </div>
      </body>
    </html>
    """)

@app.post("/analyze")
async def analyze(file: UploadFile, job_text: str = Form(...)):
    # save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name
    
    # analyze CV
    data = analyze_resume(pdf_path)
    resume_text = data["raw_text"]
    name = data.get("name") or "Candidate"
    pack = generate_package(resume_text, job_text, name=name)

    # ✅ SAVE markdown for the Download button
    with open("engine/output_pack.md", "w", encoding="utf-8") as f:
        f.write(pack["markdown"])

    # delete temp file
    os.remove(pdf_path)

    # return results page
    return HTMLResponse(f"""
    <html>
      <head>{STYLE}</head>
      <body>
        <h2>📊 Analysis Result</h2>
        <p class="score">Match Score: {pack['score']}%</p>

        <div class="box">
          <h3>✅ Found skills</h3>
          <ul>{"".join(f"<li>{s}</li>" for s in pack['found']) or "<li>None</li>"}</ul>
        </div>

        <div class="box">
          <h3>❌ Missing skills</h3>
          <ul>{"".join(f"<li>{s}</li>" for s in pack['missing']) or "<li>None</li>"}</ul>
        </div>

        <div class="box">
          <h3>✨ Improved Bullets</h3>
          <ul>{"".join(f"<li>{b}</li>" for b in pack['improved_bullets']) or "<li>None</li>"}</ul>
        </div>

        <div class="box">
          <h3>📄 Summary</h3>
          <p>{pack['summary']}</p>
        </div>

        <div class="box">
          <h3>💌 Cover Letter</h3>
          <pre>{pack['cover_letter']}</pre>
        </div>

        <div class="box">
          <a class="btn" href="/download">⬇️ Download as Markdown</a>
        </div>

        <br><a href="/">🔙 Back</a>
      </body>
    </html>
    """)

@app.get("/download")
def download():
    with open("engine/output_pack.md", "r", encoding="utf-8") as f:
        text = f.read()
    return HTMLResponse(content=text, headers={
        "Content-Disposition": "attachment; filename=careerforge_output.md"
    })
