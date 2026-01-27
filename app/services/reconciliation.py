"""
Módulo de reconciliação de estoque.

Responsabilidades:
- Identificar itens que constam como estoque na base mas não foram escaneados
- Gerar relatórios de divergência entre estoque sistêmico e físico
"""

import pandas as pd
from typing import Dict, List


def get_missing_items(database: pd.DataFrame, scanned_serials: List[str]) -> pd.DataFrame:
    """
    Identifica equipamentos marcados como estoque na base que não foram bipados.
    
    Args:
        database: DataFrame completo do Lansweeper
        scanned_serials: Lista de seriais que foram escaneados fisicamente
        
    Returns:
        DataFrame com itens de estoque não bipados (faltantes)
    """
    if database is None or database.empty:
        return pd.DataFrame()
    
    # Normalize scanned serials to uppercase for comparison
    scanned_serials_normalized = [s.upper() for s in scanned_serials]
    
    # Filter items marked as 'stock'
    stock_items = database[
        database['State'].str.lower() == 'stock'
    ].copy()
    
    # Find missing items (not scanned)
    missing_stock = stock_items[
        ~stock_items['Serialnumber'].str.upper().isin(scanned_serials_normalized)
    ].copy()
    
    # Select relevant columns
    columns_to_keep = ['Serialnumber', 'State', 'Model', 'Name', 'lastuser']
    
    # Ensure columns exist
    for col in columns_to_keep:
        if col not in missing_stock.columns:
            missing_stock[col] = 'N/A'
    
    return missing_stock[columns_to_keep]


def get_stock_metrics(database: pd.DataFrame, scanned_items: List[Dict]) -> Dict[str, int]:
    """
    Calcula métricas de estoque para exibição.
    
    Args:
        database: DataFrame completo do Lansweeper
        scanned_items: Lista de itens escaneados (histórico da sessão)
        
    Returns:
        Dicionário com métricas:
        - total_expected: Total de itens esperados no estoque
        - total_scanned_stock: Total de itens do estoque que foram bipados
        - total_missing: Total de itens faltantes
    """
    if database is None or database.empty:
        return {
            'total_expected': 0,
            'total_scanned_stock': 0,
            'total_missing': 0
        }
    
    # Count expected items (only stock)
    total_expected = len(database[database['State'].str.lower() == 'stock'])
    
    # Count scanned stock items
    scanned_stock_count = sum(
        1 for item in scanned_items 
        if item.get('found') and item.get('state') == 'stock'
    )
    
    # Count other scanned items (found but NOT stock)
    scanned_others_count = sum(
        1 for item in scanned_items
        if item.get('found') and item.get('state') != 'stock'
    )
    
    # Calculate missing
    total_missing = total_expected - scanned_stock_count
    
    return {
        'total_expected': total_expected,
        'total_scanned_stock': scanned_stock_count,
        'total_scanned_others': scanned_others_count,
        'total_missing': max(0, total_missing)  # Ensure non-negative
    }


def calculate_full_reconciliation(database: pd.DataFrame, scanned_items: List[Dict]) -> pd.DataFrame:
    """
    Gera um comparativo completo de Base vs Scaneado para TODOS os estados.
    
    Args:
        database: DataFrame Lansweeper
        scanned_items: Lista de itens escaneados
        
    Returns:
        DataFrame com colunas: [Estado, Esperado, Encontrado, Divergencia]
    """
    if database is None or database.empty:
        return pd.DataFrame()

    # 1. Contagem Esperada (Base)
    # Agrupa por State e conta
    expected_counts = database['State'].value_counts().reset_index()
    expected_counts.columns = ['state', 'expected']
    expected_counts['state'] = expected_counts['state'].str.lower()
    
    # 2. Contagem Encontrada (Scan)
    # Filtra apenas encontrados e conta por state
    scanned_df = pd.DataFrame(scanned_items)
    if not scanned_df.empty and 'state' in scanned_df.columns:
        found_items = scanned_df[scanned_df['found'] == True]
        scanned_counts = found_items['state'].value_counts().reset_index()
        scanned_counts.columns = ['state', 'scanned']
        scanned_counts['state'] = scanned_counts['state'].str.lower()
    else:
        scanned_counts = pd.DataFrame(columns=['state', 'scanned'])
        
    # 3. Merge dos dados
    # Outer join para garantir que estados que só existem em um lado apareçam
    merged = pd.merge(expected_counts, scanned_counts, on='state', how='outer').fillna(0)
    
    # 4. Formatação
    merged['expected'] = merged['expected'].astype(int)
    merged['scanned'] = merged['scanned'].astype(int)
    
    # Divergência = Esperado - Encontrado
    merged['divergence'] = merged['expected'] - merged['scanned']
    
    # Filtro: Remover 'sold' se existir
    merged = merged[merged['state'] != 'sold']
    
    # Renomear colunas para exibição
    merged = merged.rename(columns={
        'state': 'Estado',
        'expected': 'Esperado (Base)',
        'scanned': 'Encontrado (Físico)',
        'divergence': 'Divergência'
    })
    
    # Ordenar por maior quantidade esperada
    merged = merged.sort_values(by='Esperado (Base)', ascending=False)
    
    return merged
