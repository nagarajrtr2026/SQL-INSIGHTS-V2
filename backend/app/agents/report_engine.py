from typing import List, Dict, Any
from app.services.report_service import ReportService

def compile_pdf_report(title: str, rows: List[Dict[str, Any]], insights: List[str]) -> bytes:
    """
    Assembles a professional analytics report containing executive summaries, grids, and insights into a PDF.
    """
    service = ReportService()
    # Leverage existing ReportService to compile the PDF binary data
    pdf_bytes = service.generate_pdf(title=title, rows=rows, insights=insights)
    return pdf_bytes
