"""
Risk Rules for CUAD Legal Clause Categories
=============================================

Maps each CUAD clause label to a risk profile containing:
  - risk_level: HIGH / MEDIUM / LOW
  - base_score:  0-100 (severity before confidence adjustment)
  - reason:      plain-English explanation for non-lawyers

Design decisions:
  - HIGH risk:   clauses that expose the organization to financial,
                 legal, or operational liability if missed.
  - MEDIUM risk: clauses with significant business impact but that
                 are common and manageable with awareness.
  - LOW risk:    informational or protective clauses that reduce
                 rather than increase organizational risk.

Scores are intentionally coarse (not ML-derived) because this is
a first-version rule layer. Future versions can learn weights
from review outcomes or domain-expert feedback.
"""


# =============================================================
# RISK RULES — one entry per CUAD label
# =============================================================

RISK_RULES = {

    # ---------------------------------------------------------
    # HIGH RISK — financial / legal exposure
    # ---------------------------------------------------------

    "Uncapped Liability": {
        "risk_level": "HIGH",
        "base_score": 95,
        "reason": (
            "No cap on liability exposes the organization "
            "to unlimited financial damages."
        ),
    },

    "Cap On Liability": {
        "risk_level": "HIGH",
        "base_score": 85,
        "reason": (
            "A liability cap exists but must be reviewed "
            "to ensure the limit is commercially reasonable."
        ),
    },

    "Liquidated Damages": {
        "risk_level": "HIGH",
        "base_score": 85,
        "reason": (
            "Pre-agreed damage amounts may result in "
            "disproportionate financial penalties."
        ),
    },

    "Non-Compete": {
        "risk_level": "HIGH",
        "base_score": 85,
        "reason": (
            "Non-compete restrictions limit future "
            "business operations and market access."
        ),
    },

    "Exclusivity": {
        "risk_level": "HIGH",
        "base_score": 80,
        "reason": (
            "Exclusivity locks the organization into a "
            "single provider or market channel."
        ),
    },

    "Ip Ownership Assignment": {
        "risk_level": "HIGH",
        "base_score": 90,
        "reason": (
            "IP ownership transfer may permanently remove "
            "control of critical intellectual property."
        ),
    },

    "Irrevocable Or Perpetual License": {
        "risk_level": "HIGH",
        "base_score": 80,
        "reason": (
            "An irrevocable or perpetual license cannot be "
            "terminated, limiting future flexibility."
        ),
    },

    "Change Of Control": {
        "risk_level": "HIGH",
        "base_score": 80,
        "reason": (
            "Change-of-control provisions may trigger "
            "termination or renegotiation on acquisition."
        ),
    },

    "Unlimited/All-You-Can-Eat-License": {
        "risk_level": "HIGH",
        "base_score": 75,
        "reason": (
            "Unlimited licensing may create uncontrolled "
            "usage exposure or revenue leakage."
        ),
    },

    "Rofr/Rofo/Rofn": {
        "risk_level": "HIGH",
        "base_score": 75,
        "reason": (
            "Right of first refusal/offer/negotiation "
            "restricts deal-making flexibility."
        ),
    },

    # ---------------------------------------------------------
    # MEDIUM RISK — significant but manageable
    # ---------------------------------------------------------

    "Renewal Term": {
        "risk_level": "MEDIUM",
        "base_score": 65,
        "reason": (
            "Auto-renewal terms may lock the organization "
            "into unfavorable contract extensions."
        ),
    },

    "Notice Period To Terminate Renewal": {
        "risk_level": "MEDIUM",
        "base_score": 60,
        "reason": (
            "Missing the notice window causes automatic "
            "renewal; deadline tracking is critical."
        ),
    },

    "Anti-Assignment": {
        "risk_level": "MEDIUM",
        "base_score": 60,
        "reason": (
            "Assignment restrictions may block corporate "
            "restructuring or asset transfers."
        ),
    },

    "Revenue/Profit Sharing": {
        "risk_level": "MEDIUM",
        "base_score": 65,
        "reason": (
            "Profit-sharing obligations impact margins "
            "and require ongoing financial monitoring."
        ),
    },

    "Minimum Commitment": {
        "risk_level": "MEDIUM",
        "base_score": 65,
        "reason": (
            "Minimum purchase or service commitments create "
            "fixed financial obligations."
        ),
    },

    "Volume Restriction": {
        "risk_level": "MEDIUM",
        "base_score": 55,
        "reason": (
            "Volume limits may constrain growth or create "
            "penalties for exceeding thresholds."
        ),
    },

    "Price Restrictions": {
        "risk_level": "MEDIUM",
        "base_score": 55,
        "reason": (
            "Price controls limit pricing flexibility and "
            "may affect profitability."
        ),
    },

    "Most Favored Nation": {
        "risk_level": "MEDIUM",
        "base_score": 60,
        "reason": (
            "MFN clauses require matching the best terms "
            "given to any other party."
        ),
    },

    "No-Solicit Of Employees": {
        "risk_level": "MEDIUM",
        "base_score": 55,
        "reason": (
            "Non-solicitation of employees restricts "
            "talent acquisition from the counterparty."
        ),
    },

    "No-Solicit Of Customers": {
        "risk_level": "MEDIUM",
        "base_score": 60,
        "reason": (
            "Non-solicitation of customers limits "
            "business development opportunities."
        ),
    },

    "Non-Disparagement": {
        "risk_level": "MEDIUM",
        "base_score": 45,
        "reason": (
            "Non-disparagement limits public commentary "
            "about the counterparty."
        ),
    },

    "Post-Termination Services": {
        "risk_level": "MEDIUM",
        "base_score": 55,
        "reason": (
            "Post-termination obligations may require "
            "continued service delivery after exit."
        ),
    },

    "Competitive Restriction Exception": {
        "risk_level": "MEDIUM",
        "base_score": 50,
        "reason": (
            "Exceptions to competitive restrictions "
            "must be reviewed for adequate scope."
        ),
    },

    "Insurance": {
        "risk_level": "MEDIUM",
        "base_score": 50,
        "reason": (
            "Insurance requirements impose ongoing "
            "compliance and cost obligations."
        ),
    },

    "Warranty Duration": {
        "risk_level": "MEDIUM",
        "base_score": 50,
        "reason": (
            "Extended warranty periods increase long-term "
            "service and liability exposure."
        ),
    },

    "Joint Ip Ownership": {
        "risk_level": "MEDIUM",
        "base_score": 60,
        "reason": (
            "Joint IP ownership creates shared control "
            "that may lead to commercialization disputes."
        ),
    },

    "Non-Transferable License": {
        "risk_level": "MEDIUM",
        "base_score": 45,
        "reason": (
            "Non-transferable licenses restrict the "
            "ability to sublicense or assign rights."
        ),
    },

    "Source Code Escrow": {
        "risk_level": "MEDIUM",
        "base_score": 45,
        "reason": (
            "Source code escrow provisions affect "
            "business continuity planning."
        ),
    },

    # ---------------------------------------------------------
    # LOW RISK — informational or protective
    # ---------------------------------------------------------

    "Termination For Convenience": {
        "risk_level": "LOW",
        "base_score": 20,
        "reason": (
            "Termination-for-convenience provides "
            "contractual exit flexibility."
        ),
    },

    "Audit Rights": {
        "risk_level": "LOW",
        "base_score": 25,
        "reason": (
            "Audit rights enable compliance verification "
            "and financial transparency."
        ),
    },

    "Governing Law": {
        "risk_level": "LOW",
        "base_score": 20,
        "reason": (
            "Governing law identifies the legal "
            "jurisdiction for dispute resolution."
        ),
    },

    "Covenant Not To Sue": {
        "risk_level": "LOW",
        "base_score": 30,
        "reason": (
            "Covenant not to sue reduces litigation risk "
            "but limits legal recourse."
        ),
    },

    "Third Party Beneficiary": {
        "risk_level": "LOW",
        "base_score": 30,
        "reason": (
            "Third-party beneficiary rights extend "
            "obligations beyond the direct parties."
        ),
    },

    "License Grant": {
        "risk_level": "LOW",
        "base_score": 20,
        "reason": (
            "License grant defines usage rights; "
            "scope should be verified for adequacy."
        ),
    },

    "Affiliate License-Licensee": {
        "risk_level": "LOW",
        "base_score": 25,
        "reason": (
            "Affiliate license (licensee side) extends "
            "usage rights to related entities."
        ),
    },

    "Affiliate License-Licensor": {
        "risk_level": "LOW",
        "base_score": 25,
        "reason": (
            "Affiliate license (licensor side) grants "
            "rights through related entities."
        ),
    },

    # ---------------------------------------------------------
    # INFORMATIONAL — metadata labels (minimal risk)
    # ---------------------------------------------------------

    "Agreement Date": {
        "risk_level": "LOW",
        "base_score": 5,
        "reason": (
            "Agreement date is informational metadata."
        ),
    },

    "Effective Date": {
        "risk_level": "LOW",
        "base_score": 10,
        "reason": (
            "Effective date establishes when "
            "obligations begin."
        ),
    },

    "Expiration Date": {
        "risk_level": "LOW",
        "base_score": 15,
        "reason": (
            "Expiration date defines the contract "
            "end — important for deadline tracking."
        ),
    },

    "Document Name": {
        "risk_level": "LOW",
        "base_score": 5,
        "reason": (
            "Document name is informational metadata."
        ),
    },

    "Parties": {
        "risk_level": "LOW",
        "base_score": 5,
        "reason": (
            "Party identification is informational "
            "metadata for contract tracking."
        ),
    },
}