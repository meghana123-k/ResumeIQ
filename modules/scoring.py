# modules/scoring.py

def generate_explanation(dynamic_skill_score):
    if dynamic_skill_score >= 75:
        return "Strong alignment with job-required skills."
    elif dynamic_skill_score >= 50:
        return "Moderate alignment; some important job-specific skills could be strengthened."
    else:
        return "Low alignment due to missing key job-required skills."
