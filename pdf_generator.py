"""
PDF Report Generator
Creates classification reports in PDF format
"""

from typing import Dict
from datetime import datetime
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_classification_pdf(
    canonical_obj: Dict,
    intended_use: str,
    classification_result: Dict
) -> bytes:
    """
    Generate PDF classification report
    
    Args:
        canonical_obj: Canonical classification object
        intended_use: Intended use statement
        classification_result: Classification result from rule engine or database
    
    Returns:
        PDF bytes
    """
    if not REPORTLAB_AVAILABLE:
        # Fallback: generate simple text report
        return generate_text_report(canonical_obj, intended_use, classification_result).encode('utf-8')
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    elements.append(Paragraph("Medical Device Classification Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Device Information
    elements.append(Paragraph("Device Information", heading_style))
    
    device_data = [
        ['Device Name:', canonical_obj.get('device_name', 'N/A')],
        ['Generic Category:', canonical_obj.get('generic_category', 'N/A')],
        ['Classification:', f"Class {classification_result.get('class', 'N/A')}"],
        ['Licensing Authority:', classification_result.get('authority', 'N/A')],
        ['Date:', datetime.now().strftime('%B %d, %Y')]
    ]
    
    device_table = Table(device_data, colWidths=[2*inch, 4*inch])
    device_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(device_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Classification Summary
    elements.append(Paragraph("Classification Summary", heading_style))
    
    class_color = {
        'A': colors.green,
        'B': colors.yellow,
        'C': colors.orange,
        'D': colors.red,
        'UNCERTAIN': colors.grey
    }.get(classification_result.get('class', 'UNCERTAIN'), colors.grey)
    
    summary_data = [
        ['Classification Result', f"Class {classification_result.get('class', 'N/A')}"],
        ['Risk Level', get_risk_level(classification_result.get('class', 'N/A'))],
        ['Source', classification_result.get('source', 'N/A').replace('_', ' ').title()],
        ['Confidence', f"{classification_result.get('confidence', 0)*100:.1f}%"]
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('BACKGROUND', (1, 0), (1, 0), class_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Intended Use Statement
    elements.append(Paragraph("Intended Use Statement", heading_style))
    intended_use_para = Paragraph(intended_use, styles['BodyText'])
    elements.append(intended_use_para)
    elements.append(Spacer(1, 0.3*inch))
    
    # Justification
    elements.append(Paragraph("Classification Justification", heading_style))
    justification_para = Paragraph(
        classification_result.get('justification', 'No justification provided'),
        styles['BodyText']
    )
    elements.append(justification_para)
    elements.append(Spacer(1, 0.3*inch))
    
    # Technical Specifications
    elements.append(Paragraph("Technical Specifications", heading_style))
    
    spec_data = [
        ['Invasiveness:', canonical_obj.get('invasiveness', 'N/A').replace('_', ' ').title()],
        ['Implantable:', 'Yes' if canonical_obj.get('implantable') else 'No'],
        ['Duration:', canonical_obj.get('duration', 'N/A').replace('_', ' ').title()],
        ['Active Device:', 'Yes' if canonical_obj.get('active') else 'No'],
        ['Body System:', canonical_obj.get('body_system', 'N/A').replace('_', ' ').title()],
        ['Delivers Substance:', 'Yes' if canonical_obj.get('delivers_medicinal_substance') else 'No'],
        ['Delivers Energy:', 'Yes' if canonical_obj.get('delivers_energy') else 'No'],
        ['Monitors Vitals:', 'Yes' if canonical_obj.get('monitors_vital_parameter') else 'No'],
        ['Diagnostic Role:', canonical_obj.get('diagnostic_role', 'N/A').title()],
        ['Life Supporting:', 'Yes' if canonical_obj.get('life_supporting') else 'No']
    ]
    
    spec_table = Table(spec_data, colWidths=[2.5*inch, 3.5*inch])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(spec_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Regulatory Notes
    elements.append(Paragraph("Regulatory Notes", heading_style))
    
    reg_notes = get_regulatory_notes(classification_result.get('class', 'N/A'))
    elements.append(Paragraph(reg_notes, styles['BodyText']))
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        "This report is generated automatically based on MDR 2017 classification rules. "
        "Final classification should be verified by regulatory experts.",
        footer_style
    ))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def get_risk_level(classification: str) -> str:
    """Map classification to risk level"""
    risk_map = {
        'A': 'Low Risk',
        'B': 'Medium Risk',
        'C': 'High Risk',
        'D': 'Very High Risk',
        'UNCERTAIN': 'Undetermined'
    }
    return risk_map.get(classification, 'Unknown')


def get_regulatory_notes(classification: str) -> str:
    """Get regulatory notes based on classification"""
    notes = {
        'A': "Class A devices are low risk and regulated by State Licensing Authority. "
             "These devices typically require basic documentation and conformity assessment.",
        'B': "Class B devices are medium risk and regulated by State Licensing Authority. "
             "These devices require more stringent conformity assessment and documentation.",
        'C': "Class C devices are high risk and regulated by Central Licensing Authority (CDSCO). "
             "These devices require comprehensive technical documentation and clinical evaluation.",
        'D': "Class D devices are very high risk and regulated by Central Licensing Authority (CDSCO). "
             "These devices require the most rigorous assessment including extensive clinical data.",
        'UNCERTAIN': "Classification could not be determined automatically. Manual review by regulatory "
                    "experts is required to determine the appropriate classification."
    }
    return notes.get(classification, "No regulatory notes available.")


def generate_text_report(
    canonical_obj: Dict,
    intended_use: str,
    classification_result: Dict
) -> str:
    """Generate simple text report as fallback"""
    
    report = f"""
MEDICAL DEVICE CLASSIFICATION REPORT
=====================================

Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}

DEVICE INFORMATION
------------------
Device Name: {canonical_obj.get('device_name', 'N/A')}
Generic Category: {canonical_obj.get('generic_category', 'N/A')}

CLASSIFICATION RESULT
--------------------
Class: {classification_result.get('class', 'N/A')}
Risk Level: {get_risk_level(classification_result.get('class', 'N/A'))}
Authority: {classification_result.get('authority', 'N/A')}
Confidence: {classification_result.get('confidence', 0)*100:.1f}%
Source: {classification_result.get('source', 'N/A').replace('_', ' ').title()}

INTENDED USE STATEMENT
---------------------
{intended_use}

JUSTIFICATION
-------------
{classification_result.get('justification', 'No justification provided')}

TECHNICAL SPECIFICATIONS
-----------------------
Invasiveness: {canonical_obj.get('invasiveness', 'N/A').replace('_', ' ').title()}
Implantable: {'Yes' if canonical_obj.get('implantable') else 'No'}
Duration: {canonical_obj.get('duration', 'N/A').replace('_', ' ').title()}
Active Device: {'Yes' if canonical_obj.get('active') else 'No'}
Body System: {canonical_obj.get('body_system', 'N/A').replace('_', ' ').title()}
Delivers Substance: {'Yes' if canonical_obj.get('delivers_medicinal_substance') else 'No'}
Delivers Energy: {'Yes' if canonical_obj.get('delivers_energy') else 'No'}
Monitors Vitals: {'Yes' if canonical_obj.get('monitors_vital_parameter') else 'No'}
Diagnostic Role: {canonical_obj.get('diagnostic_role', 'N/A').title()}
Life Supporting: {'Yes' if canonical_obj.get('life_supporting') else 'No'}

REGULATORY NOTES
----------------
{get_regulatory_notes(classification_result.get('class', 'N/A'))}

---
This report is generated automatically based on MDR 2017 classification rules.
Final classification should be verified by regulatory experts.
"""
    
    return report
