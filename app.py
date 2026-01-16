import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from modules.text_processor import extract_resume_text, clean_text
from modules.skill_extractor import extract_skills
from modules.similarity import calculate_similarity
from modules.db import save_result
from modules.scoring import generate_explanation
from modules.role_resolver import resolve_role
from modules.weighted_scoring import calculate_weighted_skill_score


# -------------------- CONFIG --------------------

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------- HELPERS --------------------

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():

    # ---------- Resume Validation ----------
    if "resume" not in request.files:
        return "Resume file is missing", 400

    file = request.files["resume"]

    if file.filename == "":
        return "No resume file selected", 400

    if not allowed_file(file.filename):
        return "Invalid file type. Only PDF and DOCX allowed.", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # ---------- JD Validation ----------
    jd_text = request.form.get("jd", "").strip()
    if not jd_text:
        return "Job Description is required", 400

    job_title = request.form.get("job_title", "").strip()

    # ---------- Text Processing ----------
    resume_text = extract_resume_text(file_path)
    clean_jd = clean_text(jd_text)

    # ---------- Skill Extraction ----------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(clean_jd)

    missing_skills = list(set(jd_skills) - set(resume_skills))

    # ---------- Role Resolution ----------
    role, tags = resolve_role(job_title, clean_jd)

    # ---------- Weighted Skill Scoring ----------
    weighted_skill_score = calculate_weighted_skill_score(
        resume_skills,
        role
    )

    # ---------- Similarity Scoring ----------
    similarity_score = calculate_similarity(resume_text, clean_jd)

    # ---------- Final Score ----------
    final_score = round(
        (0.7 * weighted_skill_score) + (0.3 * similarity_score),
        2
    )

    # ---------- Explanation ----------
    explanation = generate_explanation(
        weighted_skill_score,
        similarity_score,
        role
    )

    # ---------- Response Object ----------
    response = {
        "canonical_role": role,
        "specializations": tags,
        "weighted_skill_score": weighted_skill_score,
        "similarity_score": similarity_score,
        "final_match_score": final_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "explanation": explanation
    }

    # ---------- Persist Result ----------
    save_result(response)

    # ---------- API vs UI ----------
    if request.headers.get("Accept") == "application/json":
        return jsonify(response)

    return render_template("result.html", result=response)


# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(debug=True)
