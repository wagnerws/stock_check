from typing import List, Dict, Any, Tuple
import pandas as pd

def calculate_general_metrics(total_base: int, scanned_items: List[Dict[str, Any]]) -> Tuple[int, float, int]:
    """
    Calcula métricas gerais de progresso.
    
    Returns:
        Tuple[total_scanned, progress_pct, pending]
    """
    total_scanned = len(scanned_items)
    progress_pct = (total_scanned / total_base) if total_base > 0 else 0.0
    pending = total_base - total_scanned
    return total_scanned, progress_pct, pending

def get_adjustment_items(scanned_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Retorna lista filtrada apenas com itens que requerem ajuste.
    """
    return [i for i in scanned_items if i.get('requires_adjustment')]

def get_state_distribution(scanned_items: List[Dict[str, Any]]) -> pd.Series:
    """
    Retorna distribuição de estados como pandas Series.
    """
    if not scanned_items:
        return pd.Series(dtype=int)
    
    df = pd.DataFrame(scanned_items)
    if 'state' in df.columns:
        return df['state'].value_counts()
    return pd.Series(dtype=int)
