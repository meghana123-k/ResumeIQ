import os

from flask import Flask, render_template, request
from modules.text_processor import extract_resume_text, clean_text
from modules.skill_extractor import extract_skills
from modules.similarity import calculate_similarity
from flask import jsonify

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]
    file = request.files["resume"]

    if file.filename == "":
        return "No selected file"

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    resume_text = extract_resume_text(file_path)
    print("Length:",len(resume_text))
    # with open("resume_text.txt", "w", encoding="utf-8") as f:
    #     f.write(resume_text)
    if "jd" not in request.form:
        return "Job Description is missing"

    jd_text = request.form["jd"]
    clean_jd = clean_text(jd_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(clean_jd)

    missing_skills = list(set(jd_skills) - set(resume_skills))
    similarity_score = calculate_similarity(resume_text, clean_jd)

    if len(jd_skills) == 0:
        skill_match_percentage = 0
    else:
        skill_match_percentage = round(
            (len(set(jd_skills) - set(missing_skills)) / len(jd_skills)) * 100, 2
        )
    final_score = round(
        (0.6 * skill_match_percentage) + (0.4 * similarity_score), 2
    )

    def generate_explanation(skill_match, similarity):
        if skill_match < 40:
            return "Low match due to missing core required skills."
        elif similarity < 20:
            return "Profile background differs significantly from the job role."
        elif skill_match >= 70 and similarity >= 50:
            return "Strong match with required skills and role alignment."
        else:
            return "Partial match; some skills and experience alignment present."

    explanation = generate_explanation(skill_match_percentage, similarity_score)

    response = {
        "skill_match_percentage": skill_match_percentage,
        "similarity_score": similarity_score,
        "final_match_score": final_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "explanation": explanation
    }

    return jsonify(response)

    # return f"<pre>{resume_text[:3000]}</pre>"
    # return f"File uploaded successfully: {file.filename}"

if __name__ == "__main__":
    app.run(debug=True)
