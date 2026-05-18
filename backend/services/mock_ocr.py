import uuid
from typing import Optional

from backend.schemas.ocr_schema import OCRChunk, OCROutput

_MOCK_PAGES = [
    (
        "MASTER SERVICES AGREEMENT\n\n"
        "This Master Services Agreement ('Agreement') is entered into as of January 15, 2025, "
        "by and between Acme Corporation, a Delaware corporation ('Client'), and "
        "TechServ Solutions Inc., a California corporation ('Provider').\n\n"
        "1. SCOPE OF SERVICES\n"
        "Provider shall provide the services described in each Statement of Work "
        "('SOW') executed by the parties from time to time."
    ),
    (
        "2. TERM AND TERMINATION\n\n"
        "2.1 Initial Term. This Agreement shall commence on the Effective Date and "
        "continue for a period of three (3) years ('Initial Term').\n\n"
        "2.2 Renewal. This Agreement shall automatically renew for successive one (1) year "
        "periods unless either party provides written notice of non-renewal at least "
        "ninety (90) days prior to the end of the then-current term.\n\n"
        "2.3 Termination for Convenience. Either party may terminate this Agreement "
        "for convenience upon sixty (60) days' prior written notice to the other party."
    ),
    (
        "3. LIABILITY\n\n"
        "3.1 Cap on Liability. EXCEPT FOR OBLIGATIONS UNDER SECTION 5 (CONFIDENTIALITY), "
        "NEITHER PARTY'S TOTAL AGGREGATE LIABILITY SHALL EXCEED THE AMOUNTS PAID OR "
        "PAYABLE UNDER THIS AGREEMENT DURING THE TWELVE (12) MONTH PERIOD PRECEDING THE CLAIM.\n\n"
        "3.2 Uncapped Liability. NOTWITHSTANDING SECTION 3.1, NEITHER PARTY'S LIABILITY "
        "FOR BREACH OF CONFIDENTIALITY OBLIGATIONS, WILLFUL MISCONDUCT, OR GROSS NEGLIGENCE "
        "SHALL BE SUBJECT TO ANY LIMITATION."
    ),
    (
        "4. PAYMENT TERMS\n\n"
        "4.1 Fees. Client shall pay Provider the fees set forth in each SOW within "
        "thirty (30) days of receipt of invoice.\n\n"
        "4.2 Late Payment. Any amounts not paid when due shall accrue interest at the "
        "rate of 1.5% per month or the maximum rate permitted by law.\n\n"
        "5. CONFIDENTIALITY\n\n"
        "Each party agrees to maintain the confidentiality of all Confidential Information "
        "disclosed by the other party for a period of five (5) years following disclosure."
    ),
]


def run_mock_ocr(contract_id: str, file_path: Optional[str] = None) -> OCROutput:
    chunks = []
    for page_num, text in enumerate(_MOCK_PAGES, start=1):
        chunks.append(
            OCRChunk(
                contract_id=contract_id,
                chunk_id=str(uuid.uuid4()),
                page=page_num,
                text=text,
            )
        )

    return OCROutput(
        contract_id=contract_id,
        chunks=chunks,
        total_pages=len(_MOCK_PAGES),
    )
