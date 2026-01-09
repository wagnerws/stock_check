"""
Módulo de validação de dados.

Responsabilidades:
- Validação de estados de equipamentos
- Validação de números de série
- Regras de negócio para identificação de inconsistências
"""

# TODO: Implementar em P2-001 - Validação de Estados

from typing import Tuple


def validate_state(state: str) -> Tuple[bool, str]:
    """
    Valida se o estado do equipamento é válido.
    
    Args:
        state: Estado a ser validado
        
    Returns:
        Tupla (is_valid, validation_message)
    """
    # TODO: Implementar validação usando VALID_STATES
    pass


def requires_adjustment(state: str) -> bool:
    """
    Verifica se o estado requer ajuste manual no Lansweeper.
    
    Args:
        state: Estado do equipamento
        
    Returns:
        True se requer ajuste (estado "active"), False caso contrário
    """
    # TODO: Implementar verificação
    pass


def validate_serial_number(serial: str) -> Tuple[bool, str]:
    """
    Valida formato de número de série.
    
    Args:
        serial: Número de série a ser validado
        
    Returns:
        Tupla (is_valid, error_message)
    """
    # TODO: Implementar validação de serial
    pass
