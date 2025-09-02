# Run My Resume 🚀

AI-powered CV analyzer & enhancer (FastAPI + Python).  
Upload a PDF CV and a Job Description → get:

- ✅ Skill match score
- ✅ Found & missing skills
- ✅ Improved CV bullet points
- ✅ Short summary + cover letter draft
- ✅ Downloadable markdown pack

---

## Quick Start
```bash
# Clone the repo
git clone https://github.com/eyaa5/run-my-resume.git
cd run-my-resume

# Create virtual environment
python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows

# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn api.main:app --reload
