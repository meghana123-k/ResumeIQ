def generate_explanation(weighted_score, similarity_score, role):
    role_name = role.replace("_", " ").title()

    if weighted_score >= 80:
        return (
            f"Strong alignment with core skills required for the {role_name} role."
        )
    elif weighted_score >= 50:
        return (
            f"Moderate alignment with the {role_name} role; some important skills may be missing."
        )
    else:
        return (
            f"Low alignment with the {role_name} role due to missing critical skills."
        )
