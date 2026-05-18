def calculate_risk(label):

    high_risk = [
        "Unlimited Liability",
        "Auto Renewal"
    ]

    medium_risk = [
        "Termination For Convenience"
    ]

    if label in high_risk:
        return "High"

    elif label in medium_risk:
        return "Medium"

    return "Low"