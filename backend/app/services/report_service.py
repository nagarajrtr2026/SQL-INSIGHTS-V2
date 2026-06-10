from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from typing import List, Dict

class ReportService:
    def generate_pdf(self, title: str, rows: List[Dict], insights: List[str], charts: List[Dict]) -> bytes:
        buf = BytesIO()
        
        # Initialize document template with standard margins
        doc = SimpleDocTemplate(
            buf,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        
        # Custom Typography Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1e1b4b"), # Deep indigo
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSectionHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#4f46e5"), # Violet
            spaceBefore=15,
            spaceAfter=8,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155") # Slate gray
        )
        
        table_cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#1e293b")
        )
        
        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=11,
            textColor=colors.white
        )

        elements = []
        
        # 1. Title Banner
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 10))
        
        # 2. AI Business Insights Section
        if insights:
            elements.append(Paragraph("Automated Business Insights", subtitle_style))
            for idx, ins in enumerate(insights):
                bullet_text = f"<b>{idx + 1}.</b> {ins}"
                elements.append(Paragraph(bullet_text, body_style))
                elements.append(Spacer(1, 6))
            elements.append(Spacer(1, 15))
            
        # 3. Query Output Table Section
        if rows:
            elements.append(Paragraph("Database Records Table", subtitle_style))
            
            # Format rows and headers
            headers = list(rows[0].keys())
            table_data = []
            
            # Wrap headers
            table_data.append([Paragraph(h, table_header_style) for h in headers])
            
            # Wrap row contents
            for row in rows:
                row_cells = []
                for val in row.values():
                    str_val = "NULL" if val is None else str(val)
                    row_cells.append(Paragraph(str_val, table_cell_style))
                table_data.append(row_cells)
                
            # Automatically calculate column widths to utilize printable canvas space (532 points wide)
            col_count = len(headers)
            col_width = 532.0 / col_count if col_count > 0 else 532
            
            # Build and style the ReportLab Table
            output_table = Table(table_data, colWidths=[col_width] * col_count)
            output_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e1b4b")), # Indigo header
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), # Slate grid borders
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]), # Alternating white/gray
            ]))
            elements.append(output_table)

        # Build document flowables
        doc.build(elements)
        buf.seek(0)
        return buf.read()

