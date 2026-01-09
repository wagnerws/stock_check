"""
Funções auxiliares gerais da aplicação.
"""

from typing import Any
from datetime import datetime


def sanitize_excel_value(value: Any) -> Any:
    """
    Remove caracteres perigosos para prevenir formula injection.
    
    Formula injection ocorre quando valores começam com =, +, -, @
    e podem executar comandos ao abrir o Excel.
    
    Args:
        value: Valor a ser sanitizado
        
    Returns:
        Valor sanitizado (string com aspas simples se perigoso)
    """
    if isinstance(value, str) and value.startswith(('=', '+', '-', '@')):
        return "'" + value  # Força tratamento como texto
    return value


def format_file_size(size_bytes: int) -> str:
    """
    Formata tamanho de arquivo em formato legível.
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        String formatada (ex: "2.5 MB", "1.3 GB")
    """
    if size_bytes < 0:
        return "Invalid size"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} PB"


def get_export_filename() -> str:
    """
    Gera nome de arquivo para exportação com timestamp.
    
    Returns:
        Nome do arquivo (ex: "ajustes_lansweeper_2026-01-08_20-30.xlsx")
    """
    from app.utils.constants import EXPORT_FILENAME_PATTERN
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return EXPORT_FILENAME_PATTERN.format(date=timestamp)


def normalize_serial(serial: str) -> str:
    """
    Normaliza número de série para comparação.
    
    Remove espaços em branco e converte para maiúsculas.
    
    Args:
        serial: Número de série original
        
    Returns:
        Número de série normalizado
    """
    if not serial:
        return ""
    
    return serial.strip().upper()
