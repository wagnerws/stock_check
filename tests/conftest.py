"""
Configuração pytest e fixtures globais.
"""

import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture
def sample_dataframe():
    """
    Fixture: DataFrame de exemplo para testes.
    
    Simula dados exportados do Lansweeper com diferentes estados.
    """
    return pd.DataFrame({
        'Serialnumber': ['ABC123', 'DEF456', 'GHI789', 'JKL012', 'MNO345'],
        'State': ['stock', 'active', 'broken', 'in repair', 'stolen'],
        'Name': ['NB-USER-001', 'NB-ADMIN-002', 'NB-DEV-003', 'MB-DESIGN-004', 'NB-SALES-005'],
        'lastuser': ['joao.silva', 'maria.santos', 'pedro.oliveira', 'ana.costa', 'carlos.lima'],
        'Asset': ['Laptop Dell 1', 'Laptop HP 2', 'Laptop Lenovo 3', 'MacBook Pro', 'Laptop Asus'],
        'Model': ['Latitude 5420', 'EliteBook 840', 'ThinkPad X1', 'MacBook Pro 14', 'ZenBook']
    })


@pytest.fixture
def fixtures_path():
    """
    Fixture: Caminho para diretório de fixtures.
    """
    return Path(__file__).parent / 'fixtures'


@pytest.fixture
def sample_excel_path(fixtures_path):
    """
    Fixture: Caminho para arquivo Excel de teste.
    """
    excel_file = fixtures_path / 'sample_lansweeper.xlsx'
    
    # Criar arquivo se não existir
    if not excel_file.exists():
        df = pd.DataFrame({
            'Serialnumber': ['ABC123', 'DEF456', 'GHI789', 'JKL012', 'MNO345', 
                           'PQR678', 'STU901', 'VWX234', 'YZA567', 'BCD890'],
            'State': ['stock', 'active', 'broken', 'in repair', 'stolen',
                     'old', 'stock', 'active', 'broken', 'stock'],
            'Name': [f'NB-{chr(65+i)}-00{i}' for i in range(10)],
            'lastuser': [f'user{i}@company.com' for i in range(10)],
            'Asset': [f'Laptop {i}' for i in range(1, 11)],
            'Model': ['Model A', 'Model B', 'Model C', 'Model D', 'Model E',
                     'Model F', 'Model G', 'Model H', 'Model I', 'Model J']
        })
        df.to_excel(excel_file, index=False)
    
    return excel_file


@pytest.fixture
def valid_states():
    """
    Fixture: Lista de estados válidos.
    """
    from app.utils.constants import VALID_STATES
    return list(VALID_STATES.keys())
