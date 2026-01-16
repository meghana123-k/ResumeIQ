from modules.role_profiles import ROLE_PROFILES

def calculate_weighted_skill_score(resume_skills, role):
    profile = ROLE_PROFILES.get(role)
    if not profile:
        return 0.0

    resume_skills = set(skill.lower() for skill in resume_skills)

    score = 0
    max_score = 0

    for skill in profile.get("critical", []):
        max_score += 3
        if skill in resume_skills:
            score += 3

    for skill in profile.get("important", []):
        max_score += 2
        if skill in resume_skills:
            score += 2

    for skill in profile.get("optional", []):
        max_score += 1
        if skill in resume_skills:
            score += 1

    if max_score == 0:
        return 0.0

    return round((score / max_score) * 100, 2)
