import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from modules.text_processor import extract_resume_text, clean_text
from modules.skill_extractor import extract_skills
from modules.similarity import calculate_similarity
from modules.scoring import generate_explanation
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

    # -------- Skill Extraction --------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(clean_jd)

    resume_skill_set = set(resume_skills)
    jd_skill_set = set(jd_skills)

    # -------- Missing & Extra Skills --------
    missing_skills = sorted(list(jd_skill_set - resume_skill_set))
    extra_skills = sorted(list(resume_skill_set - jd_skill_set))

    # -------- Skill Match Percentage --------
    if jd_skill_set:
        skill_match_percentage = round(
            ((len(jd_skill_set) - len(missing_skills)) / len(jd_skill_set)) * 100,
            2
        )
    else:
        skill_match_percentage = 0.0

    # -------- Text Similarity --------
    similarity_score = round(
        calculate_similarity(resume_text, clean_jd),
        2
    )

    # -------- Final Match Score (Conditional Weighting) --------
    if skill_match_percentage == 100:
        final_match_score = round(
            (0.8 * skill_match_percentage) + (0.2 * similarity_score),
            2
        )
    else:
        final_match_score = round(
            (0.6 * skill_match_percentage) + (0.4 * similarity_score),
            2
        )

    # -------- Explanation (Centralized Logic) --------
    explanation = generate_explanation(
        skill_match_percentage=skill_match_percentage,
        text_similarity_percentage=similarity_score,
        missing_skills_count=len(missing_skills),
        extra_skills_count=len(extra_skills)
    )

    # -------- Response Object --------
    response = {
        "skill_match_percentage": skill_match_percentage,
        "similarity_score": similarity_score,
        "final_match_score": final_match_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
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
