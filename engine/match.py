# engine/match.py
# very simple matcher (kid version 😊)

SKILL_LIST = [
    "python","java","javascript","react","node","fastapi","flask",
    "aws","lambda","api gateway","s3","dynamodb","ec2","docker",
    "kubernetes","sql","postgresql","mysql","nosql","rest",
    "git","github","testing","pytest","ci/cd"
]

def _norm(text: str) -> str:
    return " ".join(text.lower().split())

def match_resume(resume_text: str, job_text: str):
    r = _norm(resume_text)
    j = _norm(job_text)

    # skills that appear in the job text
    job_skills = [s for s in SKILL_LIST if s in j]

    # skills that appear in the resume (regardless of job)
    resume_skills = [s for s in SKILL_LIST if s in r]

    # intersection = found, difference = missing
    found = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]

    total = len(found) + len(missing)
    score = int(round(100 * (len(found) / total), 0)) if total else 0

    return {
        "resume_skills": sorted(resume_skills),  # 👈 new: shows what's in your CV
        "job_skills": sorted(job_skills),
        "found": sorted(found),
        "missing": sorted(missing),
        "score": score
    }

