import re
from modules.skills import SKILLS
from modules.skill_aliases import SKILL_ALIASES

# Build alias → canonical map
ALIAS_TO_CANONICAL = {}

for canonical, aliases in SKILL_ALIASES.items():
    for alias in aliases:
        ALIAS_TO_CANONICAL[alias.lower()] = canonical


def extract_skills(text):
    text = text.lower()
    found_skills = set()

    # Normalize aliases to canonical
    for alias, canonical in ALIAS_TO_CANONICAL.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, text):
            found_skills.add(canonical)

    # Direct canonical skill match ONLY
    for skill in SKILLS:
        if skill in SKILL_ALIASES:  # canonical skills only
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text):
                found_skills.add(skill)

    return sorted(found_skills)
