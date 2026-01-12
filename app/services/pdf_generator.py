"""
Módulo de geração de relatórios PDF para compliance.

Responsabilidades:
- Gerar PDFs profissionais com logo Anbima
- Templates para relatórios de verificação
- Metadados de compliance (hash SHA256, timestamp, session ID)
- Documentos imutáveis para auditoria
"""

import io
import hashlib
from datetime import datetime
from typing import Optional, Dict, List
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from zoneinfo import ZoneInfo


def generate_session_report_pdf(
    session_data: dict,
    scanned_items: List[dict],
    dataframe: pd.DataFrame,
    format_type: str = "complete"
) -> bytes:
    """
    Gera relatório PDF de verificação de estoque.
    
    Args:
        session_data: Dados da sessão (session_id, timestamp, etc.)
        scanned_items: Lista de itens verificados
        dataframe: DataFrame completo do Lansweeper
        format_type: Tipo de relatório ("complete", "adjustments_only", "summary")
        
    Returns:
        Bytes do PDF gerado
    """
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),  # Azul corporativo
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceBefore=12,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    
    # Header - Logo (placeholder for now)
    # TODO: Add Anbima logo when provided
    # if logo_path exists:
    #     logo = RLImage(logo_path, width=4*cm, height=1.5*cm)
    #     elements.append(logo)
    
    # Title
    if format_type == "complete":
        title_text = "RELATÓRIO DE VERIFICAÇÃO DE ESTOQUE"
    elif format_type == "adjustments_only":
        title_text = "LISTA DE AJUSTES NECESSÁRIOS - LANSWEEPER"
    else:
        title_text = "RESUMO DE VERIFICAÇÃO"
    
    elements.append(Paragraph(title_text, title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Session metadata
    session_id = session_data.get('session_id', 'N/A')
    timestamp = session_data.get('timestamp', datetime.now(ZoneInfo("America/Sao_Paulo")))
    
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            timestamp = datetime.now(ZoneInfo("America/Sao_Paulo"))
    
    timestamp_str = timestamp.strftime('%d/%m/%Y %H:%M:%S %Z')
    
    metadata_text = f"""
    <b>Data/Hora:</b> {timestamp_str}<br/>
    <b>Session ID:</b> {session_id}<br/>
    <b>Versão:</b> Stock Check v0.6.0
    """
    
    elements.append(Paragraph(metadata_text, normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Summary statistics
    total_scanned = len(scanned_items)
    items_ok = sum(1 for item in scanned_items if not item.get('requires_adjustment', False))
    items_adjustment = sum(1 for item in scanned_items if item.get('requires_adjustment', False))
    
    elements.append(Paragraph("RESUMO EXECUTIVO", heading_style))
    
    summary_data = [
        ['Métrica', 'Quantidade'],
        ['Total de Itens Verificados', str(total_scanned)],
        ['Itens OK (em estoque)', str(items_ok)],
        ['Itens que Requerem Ajuste', str(items_adjustment)],
    ]
    
    summary_table = Table(summary_data, colWidths=[10*cm, 4*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 1*cm))
    
    # Detailed items table
    if format_type == "adjustments_only":
        # Only items that require adjustment
        filtered_items = [item for item in scanned_items if item.get('requires_adjustment', False)]
    else:
        filtered_items = scanned_items
    
    if filtered_items:
        if format_type == "adjustments_only":
            elements.append(Paragraph("ITENS QUE REQUEREM AJUSTE NO LANSWEEPER", heading_style))
        else:
            elements.append(Paragraph("DETALHAMENTO DOS ITENS VERIFICADOS", heading_style))
        
        # Table header
        table_data = [['Serial', 'Estado', 'Hostname', 'Usuário', 'Hora']]
        
        for item in filtered_items:
            serial = item.get('serialnumber', 'N/A')
            state = item.get('state', 'N/A')
            name = item.get('name', 'N/A')
            lastuser = item.get('lastuser', 'N/A')
            
            # Format ativo as integer if present
            ativo_value = item.get('ativo')
            if ativo_value:
                try:
                    ativo_display = str(int(float(ativo_value)))
                except (ValueError, TypeError):
                    ativo_display = 'N/A'
            else:
                ativo_display = 'N/A'
            
            item_timestamp = item.get('timestamp', '')
            if isinstance(item_timestamp, str):
                try:
                    dt = datetime.fromisoformat(item_timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime('%H:%M:%S')
                except:
                    time_str = 'N/A'
            else:
                time_str = 'N/A'
            
            table_data.append([
                str(serial)[:20],  # Limit length
                str(state).upper(),
                str(name)[:20],
                str(lastuser)[:15],
                time_str
            ])
        
        # Create table with adjusted column widths
        items_table = Table(table_data, colWidths=[4*cm, 2.5*cm, 3.5*cm, 3*cm, 2*cm])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(items_table)
    
    # Compliance footer with hash
    elements.append(Spacer(1, 1*cm))
    
    # Generate hash of session data for integrity
    hash_content = f"{session_id}_{timestamp_str}_{total_scanned}".encode('utf-8')
    doc_hash = hashlib.sha256(hash_content).hexdigest()[:16]
    
    footer_text = f"""
    <br/><br/>
    ──────────────────────────────────────────────────────<br/>
    <b>Documento gerado automaticamente pelo Stock Check v0.6.0</b><br/>
    Hash de Integridade: {doc_hash}<br/>
    Este documento é imutável e destina-se a fins de auditoria e compliance.
    """
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def generate_adjustment_list_pdf(scanned_items: List[dict], session_id: str = None) -> bytes:
    """
    Gera PDF apenas com itens que requerem ajuste (estado "active").
    
    Args:
        scanned_items: Lista completa de itens verificados
        session_id: ID da sessão (opcional)
        
    Returns:
        Bytes do PDF gerado
    """
    # Filter only items requiring adjustment
    adjustment_items = [item for item in scanned_items if item.get('requires_adjustment', False)]
    
    if not adjustment_items:
        # Return empty or minimal PDF if no adjustments needed
        return generate_empty_adjustment_pdf()
    
    session_data = {
        'session_id': session_id or 'N/A',
        'timestamp': datetime.now(ZoneInfo("America/Sao_Paulo"))
    }
    
    return generate_session_report_pdf(
        session_data=session_data,
        scanned_items=adjustment_items,
        dataframe=pd.DataFrame(),  # Not needed for adjustment list
        format_type="adjustments_only"
    )


def generate_empty_adjustment_pdf() -> bytes:
    """
    Gera PDF vazio quando não há ajustes necessários.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    styles = getSampleStyleSheet()
    elements = []
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.green,
        alignment=TA_CENTER
    )
    
    elements.append(Spacer(1, 5*cm))
    elements.append(Paragraph("✅ NENHUM AJUSTE NECESSÁRIO", title_style))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("Todos os itens verificados estão com status correto no Lansweeper.", styles['Normal']))
    
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def generate_historical_session_pdf(session_file_data: dict) -> bytes:
    """
    Gera PDF de uma sessão histórica a partir de dados salvos.
    
    Args:
        session_file_data: Dados completos da sessão salva
        
    Returns:
        Bytes do PDF gerado
    """
    session_metadata = session_file_data.get('metadata', {})
    scanned_items = session_file_data.get('scanned_items', [])
    
    session_data = {
        'session_id': session_metadata.get('session_id', 'N/A'),
        'timestamp': session_metadata.get('start_time', datetime.now(ZoneInfo("America/Sao_Paulo")))
    }
    
    return generate_session_report_pdf(
        session_data=session_data,
        scanned_items=scanned_items,
        dataframe=pd.DataFrame(),
        format_type="complete"
    )
