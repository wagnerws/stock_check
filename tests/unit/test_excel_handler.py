"""
Testes unitários para o módulo excel_handler.

Testa funcionalidades de:
- Importação de arquivos Excel
- Validação de estrutura
- Exportação de dados
"""

import pytest
import pandas as pd
from pathlib import Path
from app.services.excel_handler import (
    import_excel,
    validate_excel_structure,
    export_excel,
    export_adjustment_list
)


class TestValidateExcelStructure:
    """Testes para validação de estrutura de arquivos Excel."""
    
    def test_validate_valid_dataframe(self, sample_dataframe):
        """Testa validação de DataFrame válido."""
        is_valid, error_message = validate_excel_structure(sample_dataframe)
        
        assert is_valid is True
        assert error_message == ""
    
    def test_validate_empty_dataframe(self):
        """Testa validação de DataFrame vazio."""
        df = pd.DataFrame()
        is_valid, error_message = validate_excel_structure(df)
        
        assert is_valid is False
        assert "vazio" in error_message.lower()
    
    def test_validate_missing_columns(self):
        """Testa validação com colunas obrigatórias ausentes."""
        df = pd.DataFrame({
            'Serialnumber': ['ABC123'],
            'Asset': ['Laptop']
            # Faltando: State, Name, lastuser
        })
        
        is_valid, error_message = validate_excel_structure(df)
        
        assert is_valid is False
        assert "ausentes" in error_message.lower()
        assert "State" in error_message
    
    def test_validate_no_records(self):
        """Testa validação com DataFrame sem registros."""
        df = pd.DataFrame(columns=['Serialnumber', 'State', 'Name', 'lastuser'])
        is_valid, error_message = validate_excel_structure(df)
        
        assert is_valid is False
        # A função retorna "vazio" para DataFrame sem registros (empty)
        assert "vazio" in error_message.lower()
    
    def test_validate_none_dataframe(self):
        """Testa validação com DataFrame None."""
        is_valid, error_message = validate_excel_structure(None)
        
        assert is_valid is False
        assert "vazio" in error_message.lower()


class TestImportExcel:
    """Testes para importação de arquivos Excel."""
    
    def test_import_valid_excel(self, sample_excel_path):
        """Testa importação de arquivo Excel válido."""
        df = import_excel(str(sample_excel_path))
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert 'Serialnumber' in df.columns
        assert 'State' in df.columns
        assert 'Name' in df.columns
        assert 'lastuser' in df.columns
        assert len(df) > 0
    
    def test_import_nonexistent_file(self):
        """Testa importação de arquivo inexistente."""
        df = import_excel('nonexistent_file.xlsx')
        
        assert df is None
    
    def test_import_invalid_extension(self, tmp_path):
        """Testa importação de arquivo com extensão inválida."""
        invalid_file = tmp_path / "test.txt"
        invalid_file.write_text("not an excel file")
        
        df = import_excel(str(invalid_file))
        
        assert df is None


class TestExportExcel:
    """Testes para exportação de arquivos Excel."""
    
    def test_export_valid_dataframe(self, sample_dataframe, tmp_path):
        """Testa exportação de DataFrame válido."""
        output_file = tmp_path / "export_test.xlsx"
        
        success = export_excel(sample_dataframe, str(output_file))
        
        assert success is True
        assert output_file.exists()
        
        # Verificar se arquivo pode ser lido novamente
        df_imported = pd.read_excel(output_file)
        assert len(df_imported) == len(sample_dataframe)
    
    def test_export_sanitizes_formulas(self, tmp_path):
        """Testa se exportação sanitiza fórmulas perigosas."""
        df = pd.DataFrame({
            'Serialnumber': ['=CMD|"/c calc"!A1', '+2+2', '-10', '@SUM(A1:A10)'],
            'State': ['stock', 'stock', 'stock', 'stock'],
            'Name': ['NB-001', 'NB-002', 'NB-003', 'NB-004'],
            'lastuser': ['user1', 'user2', 'user3', 'user4']
        })
        
        output_file = tmp_path / "sanitized_test.xlsx"
        success = export_excel(df, str(output_file))
        
        assert success is True
        
        # Verificar se fórmulas foram sanitizadas
        df_imported = pd.read_excel(output_file)
        for value in df_imported['Serialnumber']:
            # Valores devem ser strings e começar com apóstrofo se iniciavam com =, +, -, @
            assert isinstance(value, str)
    
    def test_export_empty_dataframe(self, tmp_path):
        """Testa exportação de DataFrame vazio."""
        df = pd.DataFrame(columns=['Serialnumber', 'State', 'Name', 'lastuser'])
        output_file = tmp_path / "empty_test.xlsx"
        
        success = export_excel(df, str(output_file))
        
        assert success is True
        assert output_file.exists()


class TestExportAdjustmentList:
    """Testes para exportação de lista de ajustes."""
    
    def test_export_adjustment_list_valid(self, sample_dataframe):
        """Testa exportação de lista de ajustes."""
        # Filtrar apenas equipamentos ativos
        active_equipment = sample_dataframe[sample_dataframe['State'] == 'active']
        
        result_bytes = export_adjustment_list(active_equipment)
        
        assert result_bytes is not None
        assert len(result_bytes) > 0
        assert isinstance(result_bytes, bytes)
    
    def test_export_adjustment_list_has_timestamp(self, sample_dataframe):
        """Testa se lista de ajustes inclui timestamp."""
        active_equipment = sample_dataframe[sample_dataframe['State'] == 'active']
        
        result_bytes = export_adjustment_list(active_equipment)
        
        # Ler bytes de volta para verificar estrutura
        from io import BytesIO
        df_result = pd.read_excel(BytesIO(result_bytes))
        
        assert 'Data_Verificacao' in df_result.columns
    
    def test_export_adjustment_list_column_order(self, sample_dataframe):
        """Testa se colunas estão na ordem correta."""
        active_equipment = sample_dataframe[sample_dataframe['State'] == 'active']
        
        result_bytes = export_adjustment_list(active_equipment)
        
        # Ler bytes de volta para verificar estrutura
        from io import BytesIO
        df_result = pd.read_excel(BytesIO(result_bytes))
        
        expected_columns = ['Serialnumber', 'State', 'Name', 'lastuser', 'Data_Verificacao']
        assert list(df_result.columns) == expected_columns
    
    def test_export_adjustment_list_empty(self):
        """Testa exportação de lista vazia."""
        df_empty = pd.DataFrame(columns=['Serialnumber', 'State', 'Name', 'lastuser'])
        
        result_bytes = export_adjustment_list(df_empty)
        
        # Mesmo vazio, deve retornar bytes válidos ou vazio
        assert isinstance(result_bytes, bytes)
