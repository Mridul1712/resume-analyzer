from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Skill database
skills_db = [
    "python", "java", "machine learning", "ai", "html", "css",
    "javascript", "flask", "django", "sql", "data analysis",
    "c++", "react", "nodejs"
]

# Extract text from PDF
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    text = text.lower()
    text = text.replace("\n", " ")

    return text

# Extract skills from text
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))

# Calculate match score
def calculate_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    match_count = 0

    for skill in jd_skills:
        if skill in resume_skills:
            match_count += 1

    score = int((match_count / len(jd_skills)) * 100)
    return score

@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    match_score = 0
    missing_skills = []

    if request.method == "POST":
        file = request.files.get("resume")
        jd_text = request.form.get("jd", "")

        if file:
            resume_text = extract_text(file)

            # DEBUG (optional)
            print("Resume Text:", resume_text)

            skills = extract_skills(resume_text)

            jd_text = jd_text.lower()
            jd_skills = extract_skills(jd_text)

            match_score = calculate_match(skills, jd_skills)

            missing_skills = list(set(jd_skills) - set(skills))

    return render_template(
        "index.html",
        skills=skills,
        match_score=match_score,
        missing_skills=missing_skills
    )

if __name__ == "__main__":
    app.run(debug=True)