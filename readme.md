ResumeIQ – AI-Based Resume Analysis & Matching System
=====================================================

ResumeIQ is a backend-focused NLP project that analyzes resumes against job descriptions to determine **skill match**, **missing skills**, and **overall relevance**. The system is designed to be explainable, deterministic, and incrementally extensible, making it suitable for real-world resume screening scenarios.

***

## 📑 Table of Contents

- [Project Motivation](#-project-motivation)
- [What ResumeIQ Does](#-what-resumeiq-does)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Technologies Used](#️-technologies-used)
- [Core Modules Explained](#-core-modules-explained)
- [Example Output](#-example-output)
- [Why TF-IDF Instead of Deep Learning?](#-why-tf-idf-instead-of-deep-learning)
- [How to Run the Project](#-how-to-run-the-project)
- [Current Project Status](#-current-project-status)
- [Future Enhancements](#-future-enhancements)
- [Key Learning Outcomes](#-key-learning-outcomes)
- [Disclaimer](#-disclaimer)
- [Author](#-author)

***

## 🚀 Project Motivation

Most resume screening systems rely on naive keyword matching or opaque AI models that provide little transparency. ResumeIQ focuses on:

- Clean resume parsing  
- Controlled skill extraction  
- Explainable matching logic  
- Measurable resume–JD similarity  

The goal is **accuracy with clarity**, not black-box predictions.

***

## 🧠 What ResumeIQ Does

### Inputs

- Resume file (PDF or DOCX)  
- Job description (plain text)  

### Processing Pipeline

1. Resume text extraction  
2. Text cleaning and normalization  
3. Skill extraction from resume and JD  
4. Missing skill identification  
5. Resume–JD similarity scoring using NLP  

***

## 🏗️ System Architecture

> High-level idea:  
> - Web layer (Flask) exposes endpoints to upload a resume and submit a job description.  
> - Backend pipeline handles extraction, cleaning, skill matching, and similarity scoring.  
> - Optional database layer (MongoDB) can store resumes, job descriptions, and analysis history.



***

## 🗂 Project Structure

A suggested structure for this project:

```bash
ResumeIQ/
├─ app.py                  # Flask entry point
├─ requirements.txt
├─ README.md
├─ resume_iq/
│  ├─ __init__.py
│  ├─ parsers.py          # PDF/DOCX parsing logic
│  ├─ cleaning.py         # Text cleaning & normalization
│  ├─ skills.py           # Skill vocabulary & extraction
│  ├─ similarity.py       # TF-IDF & cosine similarity
│  └─ config.py           # Constants, paths, tunables
├─ data/
│  ├─ skills_vocab.json   # Predefined skill vocabulary
│  └─ samples/            # Sample resumes & JDs
└─ templates/
   └─ index.html          # Simple frontend for upload & results
```

You can adapt this to your actual repository layout.

***

## ⚙️ Technologies Used

- **Backend:** Python, Flask  
- **NLP:** TF-IDF, Cosine Similarity (scikit-learn)  
- **Parsing:** pdfplumber, python-docx  
- **Frontend:** HTML  
- **Database (Optional):** MongoDB  

***

## 🔍 Core Modules Explained

### 1️⃣ Resume Parsing

- Supports PDF and DOCX formats.  
- Extracts raw resume text.  
- Handles empty pages and encoding artifacts.

### 2️⃣ Text Cleaning

- Removes PDF encoding noise.  
- Preserves logical section structure where possible.  
- Normalizes whitespace.  
- Standardizes common technical keywords.

### 3️⃣ Skill Extraction

- Uses a predefined skill vocabulary.  
- Deterministic string or pattern matching (no ML black box).  
- Extracts skills from both resume and job description.  

### 4️⃣ Missing Skill Detection

- Identifies job description skills not present in the resume.  
- Highlights qualification gaps clearly.

### 5️⃣ Resume–JD Similarity

- Converts text into TF-IDF vectors.  
- Computes cosine similarity between resume and JD.  
- Produces an interpretable relevance score.

***

## 🧾 Example Output

A typical JSON-style output from the backend could look like:

```json
{
  "resume_skills": ["Python", "Flask", "NLP", "MongoDB"],
  "jd_skills": ["Python", "Flask", "Docker", "REST APIs"],
  "matched_skills": ["Python", "Flask"],
  "missing_skills": ["Docker", "REST APIs"],
  "similarity_score": 0.78,
  "comments": "Good match for backend Python stack; consider adding Docker and REST API experience."
}
```

You can also render this in the frontend as a simple HTML report.

***

## 🎯 Why TF-IDF Instead of Deep Learning?

- Transparent and explainable.  
- No external APIs required.  
- Well-suited for structured professional text such as resumes and JDs.  
- Easy to debug and justify during interviews and code walkthroughs.

This project prioritizes **engineering correctness over hype**, making it a great portfolio piece to showcase practical NLP and system design skills.

***

## 🧪 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd ResumeIQ
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Flask App

```bash
python app.py
```

### 5️⃣ Open in Browser

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

***

## 🧩 Current Project Status

- ✔ Resume parsing  
- ✔ Text cleaning  
- ✔ Skill extraction  
- ✔ Missing skill detection  
- ⏳ Similarity-based scoring (in progress)  
- ⏳ Final match score aggregation  

You can update these as features are completed.

***

## 🔮 Future Enhancements

- Role-based skill weighting (e.g., backend vs. data science roles).  
- Actionable resume improvement suggestions based on missing skills.  
- Multi-resume ranking for a single job description.  
- Dashboard-style visualization for HR/recruiters.  
- Authentication and persistence with a database.  
- OCR support for scanned PDF resumes.

***

## 📌 Key Learning Outcomes

- Practical NLP without relying on black-box models.  
- Backend-first project design and API thinking.  
- Hands-on experience with real-world text preprocessing challenges.  
- Explainable AI principles applied to resume screening.  
- Fundamentals of building a resume screening system.

***

## 🧠 Disclaimer

ResumeIQ is an educational project designed to demonstrate NLP and backend engineering concepts. It is not intended to replace professional hiring or ATS systems in production environments.

***

## 👤 Author

**Meghana Kothakonda**  
B.Tech CSE (Data Science)