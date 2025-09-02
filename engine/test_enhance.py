# engine/test_enhance.py
from analyze import analyze_resume
from enhance import generate_package

# 1) read your resume text (from Day 1)
data = analyze_resume("sample.pdf")
resume_text = data["raw_text"]
name = data.get("name") or "Candidate"

# 2) read the job description (from Day 2)
with open("engine/jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

# 3) generate everything
pack = generate_package(resume_text, jd_text, name=name)

print("\n=== FOUND SKILLS ===")
print(pack["found"])
print("\n=== MISSING SKILLS ===")
print(pack["missing"])
print(f"\n=== SCORE === {pack['score']}%")
print("\n=== IMPROVED BULLETS ===")
for b in pack["improved_bullets"]:
    print(" -", b)
print("\n=== SUMMARY ===")
print(pack["summary"])
print("\n=== COVER LETTER ===")
print(pack["cover_letter"])

# 4) save the Markdown so you can open it
with open("engine/output_pack.md", "w", encoding="utf-8") as f:
    f.write(pack["markdown"])
print("\nSaved: engine/output_pack.md ✅")
