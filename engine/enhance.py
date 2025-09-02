# engine/enhance.py
# very simple writer (kid version 😊) — CLEANED + BOLD SKILLS

from typing import List, Dict
import re, random
from .match import match_resume

# 🔹 strong action verbs
ACTION_VERBS = [
    "Designed", "Built", "Implemented", "Developed", "Optimized",
    "Automated", "Improved", "Integrated", "Analyzed", "Deployed"
]
# 🔹 weak verbs to clean
WEAK_VERBS = ["worked on", "helped", "did", "made"]

# 🔹 regex helpers for cleaning junk
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d ()\-]{6,}")
YEAR_RE  = re.compile(r"\b(19|20)\d{2}\b")
ADDR_HINTS = ("str", "straße", "street", "st.", "pl.", "avenue", "rue", "wh", "zip", "merseburg", "gabes")

# --- NEW: bold keywords in HTML ---
def _bold_keywords_html(text: str, keywords: List[str]) -> str:
    for k in keywords[:5]:  # only bold top 5 skills
        if not k:
            continue
        text = re.sub(fr'(?i)\b{re.escape(k)}\b', f"<strong>{k}</strong>", text)
    return text

# --- clean resume lines ---
def _clean_lines(text: str) -> List[str]:
    lines = [l.strip("•-–\t ") for l in text.splitlines()]
    out: List[str] = []
    seen = set()

    for line in lines:
        if not line:
            continue
        low = line.lower()

        if EMAIL_RE.search(line): continue
        if PHONE_RE.search(line): continue
        if any(h in low for h in ADDR_HINTS): continue
        if YEAR_RE.search(line) and len(line) < 25: continue
        if len(line.split()) < 3: continue
        if len(line) < 20 or len(line) > 160: continue

        key = low
        if key in seen: continue
        seen.add(key)
        out.append(line.strip().rstrip("."))

    if not out:
        sentences = [s.strip() for s in re.split(r"[.\n]", text) if len(s.strip()) > 20]
        for s in sentences[:10]:
            if s.lower() not in seen:
                out.append(s)

    return out

def _pick_bullets(text: str, n: int = 3) -> List[str]:
    lines = _clean_lines(text)
    return lines[:n] if lines else []

def _upgrade_bullet(b: str, keywords: List[str]) -> str:
    s = b.strip()

    for w in WEAK_VERBS:
        if s.lower().startswith(w):
            s = s[len(w):].lstrip()
            break

    verb = random.choice(ACTION_VERBS)
    techs = ", ".join(keywords[:3]) if keywords else ""
    tech_part = f" using {techs}" if techs else ""

    sentence = f"{verb} {s}{tech_part}, improving results by ~X%."
    return _bold_keywords_html(sentence, keywords)

def make_summary(name: str, found_skills: List[str]) -> str:
    top = ", ".join(found_skills[:4]) if found_skills else "software and problem-solving"
    summary = (
        f"{name} — motivated student building practical tools. "
        f"Strengths: {top}. Seeking a software engineering internship."
    )
    return _bold_keywords_html(summary, found_skills)

def make_cover_letter(name: str, company: str, role: str, found_skills: List[str]) -> str:
    top = ", ".join(found_skills[:5]) if found_skills else "Python and problem-solving"
    cover = (
        f"Dear Hiring Team at {company},\n\n"
        f"My name is {name}. I built tools that analyze résumés and match them to job posts. "
        f"I enjoy creating useful, fast, privacy-friendly software. I’m applying for the {role} internship. "
        f"I can contribute with {top} and strong ownership.\n\n"
        f"Thank you for your time,\n{name}"
    )
    return _bold_keywords_html(cover, found_skills)

def generate_package(resume_text: str, job_text: str, name: str = "Candidate") -> Dict:
    m = match_resume(resume_text, job_text)
    found = m["found"]; missing = m["missing"]; score = m["score"]

    raw_bullets = _pick_bullets(resume_text, n=3)
    improved = [_upgrade_bullet(b, found) for b in raw_bullets]

    role = "Software Engineer Intern"
    m_role = re.search(r"(intern|internship).{0,30}", job_text, flags=re.I)
    if m_role:
        role = m_role.group(0).strip().title()

    company = "the company"
    m_co = re.search(r"at\s+([A-Z][A-Za-z0-9& ]+)", job_text)
    if m_co: company = m_co.group(1).strip()

    summary = make_summary(name, found)
    cover = make_cover_letter(name, company, role, found)

    md = [
        "# Tailored Application Pack",
        f"**Match score:** {score}%",
        "",
        "## Found skills",
        "- " + "\n- ".join(found) if found else "_None found yet_",
        "",
        "## Missing skills",
        "- " + "\n- ".join(missing) if missing else "_None_",
        "",
        "## Improved bullets",
        "- " + "\n- ".join(improved) if improved else "_No bullets extracted_",
        "",
        "## Summary",
        summary,
        "",
        "## Cover Letter",
        cover
    ]
    return {
        "found": found,
        "missing": missing,
        "score": score,
        "improved_bullets": improved,
        "summary": summary,
        "cover_letter": cover,
        "markdown": "\n".join(md)
    }
