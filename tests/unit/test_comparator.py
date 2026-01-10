
import pytest
import pandas as pd
from app.services.comparator import find_equipment, compare_and_flag, get_adjustment_list
from app.utils.constants import VALID_STATES, REQUIRES_ADJUSTMENT_STATE

# Fixture local para testes do comparador
@pytest.fixture
def mock_database():
    data = {
        'Serialnumber': ['ABC12345', 'XYZ98765', 'DEF55555', 'OLD11111'],
        'State': ['stock', 'active', 'broken', 'old'],
        'Name': ['NB-STOCK-01', 'NB-USER-02', 'NB-BROKEN-03', 'NB-OLD-04'],
        'lastuser': ['IT-Room', 'joao.silva', 'maria.souza', 'legacy.user']
    }
    return pd.DataFrame(data)

def test_find_equipment_found(mock_database):
    """Testa busca de equipamento existente"""
    result = find_equipment('abc12345', mock_database) # Case insensitive search
    assert result is not None
    assert result['serialnumber'] == 'ABC12345'
    assert result['state'] == 'stock'
    assert result['name'] == 'NB-STOCK-01'

def test_find_equipment_not_found(mock_database):
    """Testa busca de equipamento inexistente"""
    result = find_equipment('NOTFOUND', mock_database)
    assert result is None

def test_find_equipment_empty_db():
    """Testa busca em banco vazio"""
    result = find_equipment('ABC', pd.DataFrame())
    assert result is None

def test_compare_and_flag_adjustment_needed(mock_database):
    """Testa flag de ajuste necessário (Active)"""
    # XYZ98765 is active
    result = compare_and_flag('XYZ98765', mock_database)
    
    assert result['found'] is True
    assert result['requires_adjustment'] is True
    assert result['status_emoji'] == '⚠️'
    assert 'name' in result
    assert result['name'] == 'NB-USER-02'
    assert 'lastuser' in result
    assert result['lastuser'] == 'joao.silva'

def test_compare_and_flag_stock_ok(mock_database):
    """Testa equipamento OK (Stock)"""
    # ABC12345 is stock
    result = compare_and_flag('ABC12345', mock_database)
    
    assert result['found'] is True
    assert result['requires_adjustment'] is False
    assert result['status_emoji'] == '✅'
    # Name/Lastuser optional for OK items (implementation detail: logic says only for active)
    # Check implementation: lines 97-99 of comparator.py only adds name/lastuser IF requires adjustment
    assert 'name' not in result 

def test_compare_and_flag_not_found(mock_database):
    """Testa equipamento não encontrado"""
    result = compare_and_flag('UNKNOWN', mock_database)
    
    assert result['found'] is False
    assert result['status_emoji'] == '❌'
    assert result['requires_adjustment'] is False

def test_get_adjustment_list(mock_database):
    """Testa filtro da lista de ajustes"""
    adj_list = get_adjustment_list(mock_database)
    
    assert len(adj_list) == 1
    assert adj_list.iloc[0]['Serialnumber'] == 'XYZ98765'
    assert adj_list.iloc[0]['State'] == 'active'

def test_get_adjustment_list_columns(mock_database):
    """Testa se colunas obrigatórias estão presentes"""
    adj_list = get_adjustment_list(mock_database)
    expected_cols = ['Serialnumber', 'State', 'Name', 'lastuser']
    
    for col in expected_cols:
        assert col in adj_list.columns


# Testes para busca por patrimônio
@pytest.fixture
def database_with_patrimonio():
    """Database de teste com coluna Ativo (patrimônio)"""
    data = {
        'Serialnumber': ['JQHP813', 'ABC123', 'XYZ789'],
        'State': ['Stock', 'Active', 'Broken'],
        'Name': ['NB-001', 'NB-002', 'NB-003'],
        'lastuser': ['user1', 'user2', 'user3'],
        'Ativo': [9856.0, 1234.0, 5678.0]  # Float como vem do Excel
    }
    return pd.DataFrame(data)


def test_find_equipment_by_patrimonio_returns_serialnumber(database_with_patrimonio):
    """Testa que busca por patrimônio retorna o serialnumber associado"""
    result = find_equipment('9856', database_with_patrimonio)
    
    assert result is not None
    assert result['serialnumber'] == 'JQHP813'
    assert result['state'] == 'stock'
    

def test_find_equipment_patrimonio_formatted_as_int(database_with_patrimonio):
    """Testa que patrimônio é formatado como inteiro (sem casas decimais)"""
    result = find_equipment('9856', database_with_patrimonio)
    
    assert result is not None
    assert result['ativo'] == 9856  # Int, não 9856.0
    assert isinstance(result['ativo'], int)


def test_find_equipment_by_serialnumber_still_works(database_with_patrimonio):
    """Testa que busca por serial continua funcionando normalmente"""
    result = find_equipment('JQHP813', database_with_patrimonio)
    
    assert result is not None
    assert result['serialnumber'] == 'JQHP813'
    assert result['ativo'] == 9856


def test_compare_and_flag_by_patrimonio(database_with_patrimonio):
    """Testa comparação completa ao buscar por patrimônio"""
    result = compare_and_flag('1234', database_with_patrimonio)
    
    assert result['found'] is True
    assert result['serialnumber'] == 'ABC123'  # Serial, não o patrimônio digitado
    assert result['requires_adjustment'] is True
    assert result['state'] == 'active'
    assert result.get('ativo') == 1234

