"""
Módulo de comparação de dados.

Responsabilidades:
- Comparar serial lido com base de dados do Lansweeper
- Identificar equipamentos que requerem ajuste
- Otimizar busca para performance em grandes volumes
"""

import pandas as pd
from typing import Optional, Dict, Any
from app.utils.constants import VALID_STATES, REQUIRES_ADJUSTMENT_STATE, STATE_NORMALIZATION
from app.utils.helpers import normalize_serial


def normalize_state(state: str) -> str:
    """
    Normaliza o estado do equipamento para o padrão em inglês.
    Suporta estados em PT-BR e EN.
    
    Args:
        state: Estado do equipamento (pode ser PT-BR ou EN)
        
    Returns:
        Estado normalizado em inglês minúsculo
    """
    if not state or not isinstance(state, str):
        return 'unknown'
    
    state_lower = state.lower().strip()
    return STATE_NORMALIZATION.get(state_lower, 'unknown')


def find_equipment(serial: str, database: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Busca equipamento na base de dados pelo número de série ou patrimônio.
    
    Args:
        serial: Número de série ou patrimônio a ser buscado
        database: DataFrame com base de dados do Lansweeper
        
    Returns:
        Dicionário com dados do equipamento ou None se não encontrado
    """
    if database is None or database.empty:
        print("⚠️ DEBUG: Database is None or empty")
        return None
    
    # Normalize serial for comparison
    normalized_serial = normalize_serial(serial)
    print(f"\n🔍 DEBUG: Buscando serial/patrimônio: '{serial}' -> Normalizado: '{normalized_serial}'")
    
    # Debug: Show sample of database serials
    if 'Serialnumber' in database.columns:
        sample_serials = database['Serialnumber'].head(5).tolist()
        print(f"📊 DEBUG: Amostra de serials na base: {sample_serials}")
    
    # 1. Search by Serialnumber (prioridade 1)
    print(f"🔎 DEBUG: Procurando em 'Serialnumber'...")
    mask = database['Serialnumber'].str.upper() == normalized_serial.upper()
    result = database[mask]
    print(f"   Resultados encontrados: {len(result)}")
    
    # 2. If not found and Ativo column exists, search by patrimônio (prioridade 2)
    if result.empty and 'Ativo' in database.columns:
        print(f"🔎 DEBUG: Não encontrado no Serial. Procurando em 'Ativo' (patrimônio)...")
        
        # Debug: Show sample of Ativo values
        sample_ativos = database['Ativo'].dropna().head(5).tolist()
        print(f"📊 DEBUG: Amostra de valores em 'Ativo': {sample_ativos}")
        
        try:
            # Tentar converter input para número (patrimônio pode ser numérico)
            input_as_number = int(float(normalized_serial))
            print(f"   Input convertido para número: {input_as_number}")
            
            # Comparar como números (Ativo pode vir como float do Excel)
            mask_ativo = database['Ativo'].apply(
                lambda x: int(float(x)) == input_as_number if pd.notna(x) else False
            )
            result = database[mask_ativo]
            print(f"   Resultados encontrados por número: {len(result)}")
        except (ValueError, TypeError) as e:
            print(f"   Não é número válido ({e}), tentando como string...")
            # Se não for número, tentar comparação como string (fallback)
            mask_ativo = database['Ativo'].astype(str).str.upper() == normalized_serial.upper()
            result = database[mask_ativo]
            print(f"   Resultados encontrados por string: {len(result)}")
    
    
    if result.empty:
        print(f"❌ DEBUG: Nenhum resultado encontrado para '{serial}'")
        return None
    
    # Get first match
    equipment = result.iloc[0]
    print(f"✅ DEBUG: Equipamento encontrado! Serial: {equipment['Serialnumber']}, State: {equipment.get('State', 'N/A')}")
    
    return {
        'serialnumber': equipment['Serialnumber'],
        'state': normalize_state(equipment['State']) if pd.notna(equipment['State']) else 'unknown',
        'name': equipment['Name'] if pd.notna(equipment['Name']) else 'N/A',
        'lastuser': equipment['lastuser'] if pd.notna(equipment['lastuser']) else 'N/A',
        'ativo': int(float(equipment['Ativo'])) if 'Ativo' in equipment and pd.notna(equipment['Ativo']) else None
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
    elif state in ['stock', 'broken', 'stolen', 'in repair', 'old', 'reserved', 'sold']:
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
    
    # Add ativo (patrimônio) if available
    if equipment.get('ativo'):
        result['ativo'] = equipment['ativo']
    
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
