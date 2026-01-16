from modules.specializations import SPECIALIZATION_TAGS

def resolve_role(job_title: str, jd_text: str):
    title = job_title.lower()
    text = jd_text.lower()

    # ---- Canonical Role Resolution ----
    if "automation" in title:
        role = "automation_tester"
    elif "lead" in title:
        role = "qa_lead"
    elif any(x in title for x in ["performance", "security", "database"]):
        role = "specialized_tester"
    else:
        role = "manual_tester"

    # ---- Specialization Detection ----
    detected_tags = []

    for tag, keywords in SPECIALIZATION_TAGS.items():
        for kw in keywords:
            if kw in text:
                detected_tags.append(tag)
                break

    return role, list(set(detected_tags))
