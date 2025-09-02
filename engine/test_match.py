# engine/test_match.py
from analyze import analyze_resume
from match import match_resume

# 1) read your resume text
data = analyze_resume("sample.pdf")
resume_text = data["raw_text"]

# 2) read the job description text
with open("engine/jd.txt", "r", encoding="utf-8") as f:

    jd_text = f.read()

# 3) compare!
result = match_resume(resume_text, jd_text)

print("\n=== JOB SKILLS I NEED ===")
print(result["job_skills"])
print("\n✅ FOUND IN MY CV:")
print(result["found"])
print("\n❌ MISSING FROM MY CV:")
print(result["missing"])
print(f"\n📊 SIMPLE SCORE: {result['score']}% match\n")
