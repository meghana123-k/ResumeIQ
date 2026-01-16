import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from modules.text_processor import extract_resume_text, clean_text
from modules.skill_extractor import extract_skills
from modules.similarity import calculate_similarity
from modules.db import save_result

# -------------------- CONFIG --------------------

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------- HELPERS --------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():

    # -------- Resume Validation --------
    if "resume" not in request.files:
        return "Resume file is missing", 400

    file = request.files["resume"]
    if file.filename == "":
        return "No resume file selected", 400

    if not allowed_file(file.filename):
        return "Invalid file type. Only PDF/DOCX allowed.", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # -------- JD Validation --------
    jd_text = request.form.get("jd", "").strip()
    if not jd_text:
        return "Job Description is required", 400

    # -------- Text Processing --------
    resume_text = extract_resume_text(file_path)
    clean_jd = clean_text(jd_text)

    # -------- Skill Extraction (STATIC) --------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(clean_jd)

    # -------- Missing Skills --------
    resume_skill_set = set(resume_skills)
    missing_skills = list(set(jd_skills) - resume_skill_set)

    # -------- Skill Match Percentage --------
    if jd_skills:
        skill_match_percentage = round(
            ((len(jd_skills) - len(missing_skills)) / len(jd_skills)) * 100,
            2
        )
    else:
        skill_match_percentage = 0.0

    # -------- Similarity Scoring --------
    similarity_score = calculate_similarity(resume_text, clean_jd)

    # -------- Final Match Score --------
    final_match_score = round(
        (0.6 * skill_match_percentage) + (0.4 * similarity_score),
        2
    )

    # -------- Simple Explanation --------
    if skill_match_percentage >= 70:
        explanation = "Strong alignment with required skills."
    elif skill_match_percentage >= 40:
        explanation = "Partial match; some important skills are missing."
    else:
        explanation = "Low match due to missing key required skills."

    # -------- Response Object --------
    response = {
        "skill_match_percentage": skill_match_percentage,
        "similarity_score": similarity_score,
        "final_match_score": final_match_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "explanation": explanation
    }

    # -------- Persist Result --------
    save_result(response)

    # -------- API vs UI --------
    if request.headers.get("Accept") == "application/json":
        return jsonify(response)

    return render_template("result.html", result=response)


# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(debug=True)
