"""
Módulo de manipulação de arquivos Excel.

Responsabilidades:
- Importação de arquivos Excel do Lansweeper
- Validação de estrutura e colunas obrigatórias
- Exportação de relatórios em formato Excel
"""

import pandas as pd
from typing import Optional, Tuple
from datetime import datetime
from app.config import REQUIRED_COLUMNS
from app.utils.helpers import sanitize_excel_value


def import_excel(file_path: str) -> Optional[pd.DataFrame]:
    """
    Importa arquivo Excel do Lansweeper e valida estrutura.
    
    Args:
        file_path: Caminho do arquivo Excel
        
    Returns:
        DataFrame com dados importados ou None se inválido
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Validate structure
        is_valid, error_message = validate_excel_structure(df)
        
        if not is_valid:
            raise ValueError(error_message)
        
        return df
    
    except Exception as e:
        print(f"Erro ao importar Excel: {str(e)}")
        return None


def validate_excel_structure(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Valida se o DataFrame possui as colunas obrigatórias.
    
    Args:
        df: DataFrame a ser validado
        
    Returns:
        Tupla (is_valid, error_message)
    """
    if df is None or df.empty:
        return False, "Arquivo Excel está vazio"
    
    # Check for required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    
    if missing_columns:
        return False, f"Colunas obrigatórias ausentes: {', '.join(missing_columns)}"
    
    # Check if there's at least one row
    if len(df) == 0:
        return False, "Arquivo Excel não contém nenhum registro"
    
    return True, ""


def export_excel(df: pd.DataFrame, output_path: str) -> bool:
    """
    Exporta DataFrame para arquivo Excel.
    
    Args:
        df: DataFrame a ser exportado
        output_path: Caminho do arquivo de saída
        
    Returns:
        True se exportação bem-sucedida, False caso contrário
    """
    try:
        # Sanitize all values to prevent formula injection
        sanitized_df = df.copy()
        for col in sanitized_df.columns:
            sanitized_df[col] = sanitized_df[col].apply(
                lambda x: sanitize_excel_value(str(x)) if pd.notna(x) else ''
            )
        
        # Export to Excel
        sanitized_df.to_excel(output_path, index=False, engine='openpyxl')
        return True
    
    except Exception as e:
        print(f"Erro ao exportar Excel: {str(e)}")
        return False


def export_adjustment_list(equipment_list: pd.DataFrame) -> bytes:
    """
    Exporta lista de equipamentos que requerem ajuste para bytes.
    
    Args:
        equipment_list: DataFrame com equipamentos ativos
        
    Returns:
        Bytes do arquivo Excel gerado
    """
    try:
        # Add verification timestamp
        equipment_list = equipment_list.copy()
        equipment_list['Data_Verificacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Ensure columns are in correct order
        columns_order = ['Serialnumber', 'State', 'Name', 'lastuser', 'Data_Verificacao']
        equipment_list = equipment_list[columns_order]
        
        # Sanitize all values
        for col in equipment_list.columns:
            equipment_list[col] = equipment_list[col].apply(
                lambda x: sanitize_excel_value(str(x)) if pd.notna(x) else ''
            )
        
        # Export to bytes
        from io import BytesIO
        output = BytesIO()
        equipment_list.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        
        return output.getvalue()
    
    except Exception as e:
        print(f"Erro ao exportar lista de ajustes: {str(e)}")
        return b''
