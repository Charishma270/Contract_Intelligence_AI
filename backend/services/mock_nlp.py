from backend.schemas.nlp_schema import ClausePrediction, EntityPrediction, NLPOutput


def run_mock_nlp(contract_id: str) -> NLPOutput:
    clauses = [
        ClausePrediction(
            clause_type="Termination For Convenience",
            answer_text=(
                "Either party may terminate this Agreement for convenience "
                "upon sixty (60) days' prior written notice to the other party."
            ),
            start_char=620,
            end_char=740,
            page=2,
            confidence=0.94,
            is_present=True,
        ),
        ClausePrediction(
            clause_type="Renewal Term",
            answer_text=(
                "This Agreement shall automatically renew for successive one (1) year "
                "periods unless either party provides written notice of non-renewal at "
                "least ninety (90) days prior to the end of the then-current term."
            ),
            start_char=380,
            end_char=580,
            page=2,
            confidence=0.91,
            is_present=True,
        ),
        ClausePrediction(
            clause_type="Cap On Liability",
            answer_text=(
                "NEITHER PARTY'S TOTAL AGGREGATE LIABILITY SHALL EXCEED THE AMOUNTS "
                "PAID OR PAYABLE UNDER THIS AGREEMENT DURING THE TWELVE (12) MONTH "
                "PERIOD PRECEDING THE CLAIM."
            ),
            start_char=810,
            end_char=980,
            page=3,
            confidence=0.88,
            is_present=True,
        ),
        ClausePrediction(
            clause_type="Uncapped Liability",
            answer_text=(
                "NEITHER PARTY'S LIABILITY FOR BREACH OF CONFIDENTIALITY OBLIGATIONS, "
                "WILLFUL MISCONDUCT, OR GROSS NEGLIGENCE SHALL BE SUBJECT TO ANY LIMITATION."
            ),
            start_char=1020,
            end_char=1180,
            page=3,
            confidence=0.86,
            is_present=True,
        ),
    ]

    entities = [
        EntityPrediction(entity_type="ORGANIZATION", value="Acme Corporation", position=95),
        EntityPrediction(entity_type="ORGANIZATION", value="TechServ Solutions Inc.", position=155),
        EntityPrediction(entity_type="JURISDICTION", value="Delaware", position=115),
        EntityPrediction(entity_type="JURISDICTION", value="California", position=170),
        EntityPrediction(entity_type="DATE", value="January 15, 2025", position=75),
        EntityPrediction(entity_type="MONETARY_VALUE", value="1.5% per month", position=1350),
        EntityPrediction(entity_type="DURATION", value="three (3) years", position=320),
        EntityPrediction(entity_type="DURATION", value="one (1) year", position=440),
        EntityPrediction(entity_type="DURATION", value="sixty (60) days", position=670),
        EntityPrediction(entity_type="DURATION", value="ninety (90) days", position=530),
        EntityPrediction(entity_type="DURATION", value="five (5) years", position=1500),
    ]

    return NLPOutput(
        contract_id=contract_id,
        clauses=clauses,
        entities=entities,
    )
