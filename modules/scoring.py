def generate_explanation(skill_match, similarity):
    if skill_match >= 70 and similarity >= 20:
        return "Strong alignment with required skills and relevant software development background."
    elif skill_match >= 70:
        return "Good skill match, but resume presentation differs from job description language."
    elif skill_match >= 40:
        return "Partial match; core skills present but some important gaps remain."
    else:
        return "Low match due to missing core required skills."
