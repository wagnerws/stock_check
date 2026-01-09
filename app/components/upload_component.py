"""
Componente de upload de arquivo Excel.

Responsabilidades:
- Interface para upload de arquivo Lansweeper
- Validação de arquivo (tamanho, formato)
- Preview dos dados carregados
- Feedback visual de sucesso/erro
"""

import streamlit as st
import pandas as pd
from typing import Optional
from app.services.excel_handler import import_excel, validate_excel_structure
from app.config import MAX_FILE_SIZE_MB
from app.utils.constants import ALLOWED_EXTENSIONS


def render_upload_component() -> Optional[pd.DataFrame]:
    """
    Renderiza componente de upload de arquivo Excel.
    
    Returns:
        DataFrame carregado ou None se nenhum arquivo válido
    """
    st.subheader("📥 Upload da Base Lansweeper")
    st.markdown(
        """
        Faça upload do arquivo Excel exportado do **Lansweeper** contendo os dados dos equipamentos.
        
        **Colunas obrigatórias:** `Serialnumber`, `State`, `Name`, `lastuser`
        """
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Selecione o arquivo Excel (.xlsx ou .xls)",
        type=['xlsx', 'xls'],
        help=f"Tamanho máximo: {MAX_FILE_SIZE_MB} MB"
    )
    
    if uploaded_file is None:
        st.info("ℹ️ Aguardando upload do arquivo...")
        return None
    
    # Validate file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(
            f"❌ Arquivo muito grande ({file_size_mb:.2f} MB). "
            f"Tamanho máximo permitido: {MAX_FILE_SIZE_MB} MB"
        )
        return None
    
    # Show file info
    st.success(f"✅ Arquivo carregado: **{uploaded_file.name}** ({file_size_mb:.2f} MB)")
    
    # Load Excel with spinner
    with st.spinner("🔄 Processando arquivo Excel..."):
        try:
            # Save to temporary file for processing
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Import Excel
            df = import_excel(tmp_path)
            
            # Remove temporary file
            os.unlink(tmp_path)
            
            if df is None:
                st.error("❌ Erro ao processar arquivo. Verifique o formato e tente novamente.")
                return None
            
            # Validate structure
            is_valid, error_message = validate_excel_structure(df)
            
            if not is_valid:
                st.error(f"❌ **Erro de validação:** {error_message}")
                st.warning(
                    "⚠️ **Certifique-se de que o arquivo contém as seguintes colunas:**\n\n"
                    "- `Serialnumber` - Número de série do equipamento\n"
                    "- `State` - Estado do equipamento\n"
                    "- `Name` - Hostname do equipamento\n"
                    "- `lastuser` - Último usuário que usou o equipamento"
                )
                return None
            
            # Success - show preview
            st.success(f"✅ **Arquivo validado com sucesso!** {len(df)} registros encontrados.")
            
            # Display preview
            _render_data_preview(df)
            
            # Store in session state
            st.session_state.lansweeper_data = df
            st.session_state.filename = uploaded_file.name
            
            return df
        
        except Exception as e:
            st.error(f"❌ **Erro inesperado:** {str(e)}")
            return None


def _render_data_preview(df: pd.DataFrame) -> None:
    """
    Renderiza preview dos dados carregados.
    
    Args:
        df: DataFrame a ser exibido
    """
    st.markdown("---")
    st.subheader("👀 Preview dos Dados")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de Registros", len(df))
    
    with col2:
        unique_states = df['State'].nunique()
        st.metric("🏷️ Estados Únicos", unique_states)
    
    with col3:
        active_count = len(df[df['State'].str.lower() == 'active'])
        st.metric("⚠️ Equipamentos Ativos", active_count)
    
    with col4:
        stock_count = len(df[df['State'].str.lower() == 'stock'])
        st.metric("✅ Em Estoque", stock_count)
    
    # State distribution
    st.markdown("#### Distribuição por Estado")
    state_counts = df['State'].value_counts()
    st.bar_chart(state_counts)
    
    # Data table preview
    st.markdown("#### Primeiros Registros")
    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True
    )
    
    # Show all columns available
    with st.expander("📋 Ver todas as colunas disponíveis"):
        st.write("**Colunas encontradas no arquivo:**")
        for i, col in enumerate(df.columns, 1):
            st.text(f"{i}. {col}")
