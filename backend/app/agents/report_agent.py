from app.services.report_service import ReportService
from typing import List, Dict


def create_report(title: str, rows: List[Dict], insights: List[str], charts: List[Dict]) -> bytes:
    service = ReportService()
    pdf = service.generate_pdf(title=title, rows=rows, insights=insights, charts=charts)
    return pdf
