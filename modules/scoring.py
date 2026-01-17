def generate_explanation(
    skill_match_percentage,
    text_similarity_percentage,
    missing_skills_count,
    extra_skills_count
):

    # Perfect skill match
    if skill_match_percentage == 100:
        if text_similarity_percentage < 30:
            return (
                "All required skills are present. "
                "Low textual similarity is likely due to wording or formatting differences."
            )
        return "Excellent alignment with all required job skills."

    # Strong match with minor gaps
    if skill_match_percentage >= 75:
        if missing_skills_count > 0:
            return (
                "Strong alignment with most required skills, "
                "with a few minor gaps to address."
            )
        return "Strong alignment with job-required skills."

    # Partial match
    if skill_match_percentage >= 50:
        return (
            "Moderate alignment; several important job-specific skills are missing "
            "and could be improved."
        )
    if skill_match_percentage == 100 and extra_skills_count >= 3:
        return (
            "All required skills are present. "
            "The profile shows broader expertise than required for this role."
        )

    # Low match
    return (
        "Low alignment due to multiple missing key job-required skills."
    )
