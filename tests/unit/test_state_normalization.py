"""
Testes unitários para normalização de estados PT-BR/EN.
"""

import pytest
from app.services.comparator import normalize_state


class TestStateNormalization:
    """Testes para a função normalize_state."""
    
    def test_normalize_state_portuguese(self):
        """Testa normalização de estados em português."""
        assert normalize_state("Reservado") == "reserved"
        assert normalize_state("Ativo") == "active"
        assert normalize_state("Estoque") == "stock"
        assert normalize_state("Quebrado") == "broken"
        assert normalize_state("Roubado") == "stolen"
        assert normalize_state("Em Reparo") == "in repair"
        assert normalize_state("Antigo") == "old"
    
    def test_normalize_state_english(self):
        """Testa normalização de estados em inglês."""
        assert normalize_state("reserved") == "reserved"
        assert normalize_state("active") == "active"
        assert normalize_state("stock") == "stock"
        assert normalize_state("broken") == "broken"
        assert normalize_state("stolen") == "stolen"
        assert normalize_state("in repair") == "in repair"
        assert normalize_state("old") == "old"
    
    def test_normalize_state_case_insensitive(self):
        """Testa que a normalização é case-insensitive."""
        assert normalize_state("RESERVADO") == "reserved"
        assert normalize_state("ReSeRvAdO") == "reserved"
        assert normalize_state("ACTIVE") == "active"
        assert normalize_state("AcTiVe") == "active"
    
    def test_normalize_state_with_whitespace(self):
        """Testa que espaços extras são removidos."""
        assert normalize_state("  Reservado  ") == "reserved"
        assert normalize_state(" Em Reparo ") == "in repair"
    
    def test_normalize_state_unknown(self):
        """Testa estados desconhecidos."""
        assert normalize_state("InvalidState") == "unknown"
        assert normalize_state("xyz") == "unknown"
        assert normalize_state("") == "unknown"
        assert normalize_state(None) == "unknown"
    
    def test_normalize_state_non_string(self):
        """Testa que valores não-string retornam 'unknown'."""
        assert normalize_state(123) == "unknown"
        assert normalize_state(None) == "unknown"
