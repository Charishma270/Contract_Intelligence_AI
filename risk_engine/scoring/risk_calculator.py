"""
Risk Calculator
===============

Converts a clause prediction (label + confidence) into a
structured risk assessment by looking up the label in
RISK_RULES and adjusting the base score by model confidence.

Usage:
    from risk_engine.scoring.risk_calculator import calculate_risk

    result = calculate_risk("Uncapped Liability", confidence=0.91)
    # {
    #     "clause_type":  "Uncapped Liability",
    #     "risk_level":   "HIGH",
    #     "risk_score":   86,
    #     "confidence":   0.91,
    #     "reason":       "No cap on liability exposes ..."
    # }
"""

from risk_engine.rules.risk_rules import RISK_RULES


# Default rule for clauses not found in RISK_RULES.
# Ensures the function never crashes on unknown labels.
_DEFAULT_RULE = {
    "risk_level": "LOW",
    "base_score": 10,
    "reason": "No specific risk rule defined for this clause type.",
}


def calculate_risk(
    clause_type: str,
    confidence: float,
) -> dict:
    """Calculate risk for a single clause prediction.

    Args:
        clause_type: The predicted clause label name
                     (must match a CUAD label string).
        confidence:  Model confidence (sigmoid probability),
                     expected range 0.0 – 1.0.

    Returns:
        Dictionary with:
            clause_type  — the input label name
            risk_level   — HIGH / MEDIUM / LOW
            risk_score   — base_score * confidence (0-100)
            confidence   — rounded model confidence
            reason       — plain-English risk explanation
    """

    # Look up the risk rule; fall back to default for unknown labels
    rule = RISK_RULES.get(clause_type, _DEFAULT_RULE)

    # Extract rule components
    risk_level = rule["risk_level"]
    base_score = rule["base_score"]
    reason = rule["reason"]

    # Adjust score by model confidence:
    # high confidence in a high-risk clause → high adjusted score
    # low confidence in a high-risk clause  → lower adjusted score
    adjusted_score = int(base_score * confidence)

    return {
        "clause_type": clause_type,
        "risk_level": risk_level,
        "risk_score": adjusted_score,
        "confidence": round(confidence, 2),
        "reason": reason,
    }
