"""
Módulo de comparação de dados.

Responsabilidades:
- Comparar serial lido com base de dados do Lansweeper
- Identificar equipamentos que requerem ajuste
- Otimizar busca para performance em grandes volumes
"""

import pandas as pd
from typing import Optional, Dict, Any
from app.utils.constants import VALID_STATES, REQUIRES_ADJUSTMENT_STATE
from app.utils.helpers import normalize_serial


def find_equipment(serial: str, database: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Busca equipamento na base de dados pelo número de série.
    
    Args:
        serial: Número de série a ser buscado
        database: DataFrame com base de dados do Lansweeper
        
    Returns:
        Dicionário com dados do equipamento ou None se não encontrado
    """
    if database is None or database.empty:
        return None
    
    # Normalize serial for comparison
    normalized_serial = normalize_serial(serial)
    
    # Search in database (case-insensitive)
    mask = database['Serialnumber'].str.upper() == normalized_serial.upper()
    result = database[mask]
    
    if result.empty:
        return None
    
    # Get first match
    equipment = result.iloc[0]
    
    return {
        'serialnumber': equipment['Serialnumber'],
        'state': equipment['State'].lower() if pd.notna(equipment['State']) else 'unknown',
        'name': equipment['Name'] if pd.notna(equipment['Name']) else 'N/A',
        'lastuser': equipment['lastuser'] if pd.notna(equipment['lastuser']) else 'N/A'
    }


def compare_and_flag(serial: str, database: pd.DataFrame) -> Dict[str, Any]:
    """
    Compara serial com base e retorna status de ajuste.
    
    Args:
        serial: Número de série lido
        database: DataFrame com base de dados
        
    Returns:
        Dicionário com informações e flag de ajuste necessário
    """
    equipment = find_equipment(serial, database)
    
    if not equipment:
        return {
            'found': False,
            'serialnumber': serial,
            'requires_adjustment': False,
            'status_emoji': '❌',
            'status_message': 'Serial não encontrado na base de dados'
        }
    
    state = equipment['state']
    requires_adjustment = (state == REQUIRES_ADJUSTMENT_STATE)
    
    # Get status description
    status_message = VALID_STATES.get(state, '❓ Estado desconhecido')
    
    # Determine emoji based on state
    if requires_adjustment:
        status_emoji = '⚠️'
    elif state in ['stock', 'broken', 'stolen', 'in repair', 'old']:
        status_emoji = '✅'
    else:
        status_emoji = '❓'
    
    result = {
        'found': True,
        'serialnumber': equipment['serialnumber'],
        'state': state,
        'requires_adjustment': requires_adjustment,
        'status_emoji': status_emoji,
        'status_message': status_message
    }
    
    # Add Name and lastuser only for active equipment
    if requires_adjustment:
        result['name'] = equipment['name']
        result['lastuser'] = equipment['lastuser']
    
    return result


def get_adjustment_list(database: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna lista de equipamentos que requerem ajuste.
    
    Args:
        database: DataFrame completo
        
    Returns:
        DataFrame filtrado com itens que têm estado "active"
    """
    if database is None or database.empty:
        return pd.DataFrame()
    
    # Filter equipment with 'active' state
    mask = database['State'].str.lower() == REQUIRES_ADJUSTMENT_STATE
    adjustment_list = database[mask].copy()
    
    # Select only relevant columns
    columns_to_keep = ['Serialnumber', 'State', 'Name', 'lastuser']
    
    # Ensure all columns exist
    for col in columns_to_keep:
        if col not in adjustment_list.columns:
            adjustment_list[col] = 'N/A'
    
    return adjustment_list[columns_to_keep]
