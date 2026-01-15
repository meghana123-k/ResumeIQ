import os

from flask import Flask, render_template, request
from modules.text_processor import extract_resume_text, clean_text
from modules.skill_extractor import extract_skills

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

    return f"""
    <h3>Resume Skills</h3>
    <pre>{resume_skills}</pre>

    <h3>JD Skills</h3>
    <pre>{jd_skills}</pre>

    <h3>Missing Skills</h3>
    <pre>{missing_skills}</pre>
    """

    # return f"<pre>{resume_text[:3000]}</pre>"
    # return f"File uploaded successfully: {file.filename}"

if __name__ == "__main__":
    app.run(debug=True)
