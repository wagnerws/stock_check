"""
Módulo de validação de dados.

Responsabilidades:
- Validação de estados de equipamentos
- Validação de números de série
- Regras de negócio para identificação de inconsistências
"""

from typing import Tuple
from app.utils.constants import VALID_STATES, REQUIRES_ADJUSTMENT_STATE


def validate_state(state: str) -> Tuple[bool, str]:
    """
    Valida se o estado do equipamento é válido.
    
    Args:
        state: Estado a ser validado (case insensitive)
        
    Returns:
        Tupla (is_valid, validation_message)
    """
    if not state:
        return False, "Estado não pode ser vazio"
        
    state_lower = state.lower().strip()
    
    if state_lower in VALID_STATES:
        # Retorna a descrição amigável do estado
        return True, VALID_STATES[state_lower]
        
    return False, f"Estado inválido: {state}"


def requires_adjustment(state: str) -> bool:
    """
    Verifica se o estado requer ajuste manual no Lansweeper.
    
    Args:
        state: Estado do equipamento
        
    Returns:
        True se requer ajuste (estado "active"), False caso contrário
    """
    if not state:
        return False
        
    return state.lower().strip() == REQUIRES_ADJUSTMENT_STATE


def validate_serial_number(serial: str) -> Tuple[bool, str]:
    """
    Valida formato de número de série.
    
    Args:
        serial: Número de série a ser validado
        
    Returns:
        Tupla (is_valid, error_message)
    """
    if not serial:
        return False, "Número de série vazio"
        
    serial_clean = serial.strip()
    
    if len(serial_clean) < 3:
        return False, "Número de série muito curto (mínimo 3 caracteres)"
        
    # Validar caracteres permitidos (alfanumérico e alguns especiais comuns em etiquetas)
    # Adapte conforme necessidade real. Por enquanto, ser flexível.
    
    return True, "Serial válido"
