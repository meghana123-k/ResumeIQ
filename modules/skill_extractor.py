from modules.skills import SKILLS
from modules.skill_aliases import SKILL_ALIASES

def extract_skills(text):
    text = text.lower()
    found_skills = set()

    # Direct skill match
    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)

    # Alias-based match
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if alias in text:
                found_skills.add(canonical)

    return list(found_skills)
