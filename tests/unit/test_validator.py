
import pytest
from app.services.validator import validate_state, requires_adjustment, validate_serial_number
from app.utils.constants import VALID_STATES, REQUIRES_ADJUSTMENT_STATE

class TestValidator:
    
    def test_validate_state_valid_inputs(self):
        """Testa validação com estados válidos (case insensitive e whitespace)"""
        # Testar todos os estados válidos
        for state_key, friendly_name in VALID_STATES.items():
            # Teste exato
            is_valid, msg = validate_state(state_key)
            assert is_valid is True
            assert msg == friendly_name
            
            # Teste UPPERCASE
            is_valid, msg = validate_state(state_key.upper())
            assert is_valid is True
            
            # Teste Mixed Case
            is_valid, msg = validate_state(state_key.title())
            assert is_valid is True
            
            # Teste com espaços
            is_valid, msg = validate_state(f"  {state_key}  ")
            assert is_valid is True
            
    def test_validate_state_invalid_inputs(self):
        """Testa validação com estados inválidos"""
        invalid_states = ["lost", "missing", "unknown", "123", "", None]
        
        for state in invalid_states:
            is_valid, msg = validate_state(state)
            assert is_valid is False
            if not state:
                assert "não pode ser vazio" in msg
            else:
                assert f"Estado inválido: {state}" in msg

    def test_requires_adjustment(self):
        """Testa verificação de ajuste necessário"""
        # Caso positivo
        assert requires_adjustment(REQUIRES_ADJUSTMENT_STATE) is True
        assert requires_adjustment(REQUIRES_ADJUSTMENT_STATE.upper()) is True
        assert requires_adjustment(f" {REQUIRES_ADJUSTMENT_STATE} ") is True
        
        # Casos negativos (outros estados válidos)
        for state_key in VALID_STATES.keys():
            if state_key != REQUIRES_ADJUSTMENT_STATE:
                assert requires_adjustment(state_key) is False
                
        # Casos inválidos/vazios
        assert requires_adjustment("unknown") is False
        assert requires_adjustment("") is False
        assert requires_adjustment(None) is False

    def test_validate_serial_number(self):
        """Testa validação de números de série"""
        # Válidos
        assert validate_serial_number("12345")[0] is True
        assert validate_serial_number("ABC-123")[0] is True
        assert validate_serial_number("  SN123  ")[0] is True
        
        # Inválidos
        assert validate_serial_number("AB")[0] is False  # Curto
        assert validate_serial_number("")[0] is False    # Vazio
        assert validate_serial_number(None)[0] is False  # None
