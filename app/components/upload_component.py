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
    st.markdown("## 📥 Upload da Base Lansweeper")
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
            df, df_removed = import_excel(tmp_path)
            
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
            st.success(f"✅ **Arquivo validado com sucesso!** {len(df)} registros de notebooks encontrados.")
            
            # Info box about filtering
            st.info(
                "ℹ️ **Filtro automático aplicado:** Apenas notebooks (Dell Latitude, Dell Pro, MacBook) e Linux "
                "foram importados. Desktops e VMs foram excluídos automaticamente."
            )
            
            # Display preview
            _render_data_preview(df)
            
            # Render debug tool
            if df_removed is not None:
                _render_debug_tool(df, df_removed)
            
            # Store in session state
            st.session_state.dataframe = df
            st.session_state.removed_dataframe = df_removed
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
    
    # Format Ativo column as integer if present
    preview_df = df.head(10).copy()
    if 'Ativo' in preview_df.columns:
        preview_df['Ativo'] = preview_df['Ativo'].apply(
            lambda x: int(float(x)) if pd.notna(x) and str(x) != '' else x
        )
    
    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Show all columns available
    with st.expander("📋 Ver todas as colunas disponíveis"):
        st.write("**Colunas encontradas no arquivo:**")
        for i, col in enumerate(df.columns, 1):
            st.text(f"{i}. {col}")


def _render_debug_tool(df_included: pd.DataFrame, df_excluded: pd.DataFrame) -> None:
    """
    Renderiza ferramenta de diagnóstico para verificar por que um serial foi ou não importado.
    
    Args:
        df_included: DataFrame com registros aceitos
        df_excluded: DataFrame com registros rejeitados/filtrados
    """
    with st.expander("🕵️ Debug de Importação / Serial não encontrado"):
        st.markdown("Use esta ferramenta se você escaneou um item e ele não foi encontrado na base.")
        
        search_serial = st.text_input("Digite o Serial Number para pesquisar:", key="debug_serial_search")
        
        if search_serial:
            search_term = search_serial.strip().lower()
            
            # Search in Included
            found_included = df_included[
                df_included['Serialnumber'].fillna('').astype(str).str.lower() == search_term
            ]
            
            # Search in Excluded
            # Handle case where df_excluded might be None (though logic prevents it) or empty
            if df_excluded is not None and not df_excluded.empty:
                found_excluded = df_excluded[
                    df_excluded['Serialnumber'].fillna('').astype(str).str.lower() == search_term
                ]
            else:
                found_excluded = pd.DataFrame()
            
            if not found_included.empty:
                st.success(f"✅ O serial **{search_serial}** foi IMPORTADO corretamente e está na base ativa.")
                st.dataframe(found_included)
            elif not found_excluded.empty:
                st.warning(f"⚠️ O serial **{search_serial}** foi ENCONTRADO no arquivo, mas foi FILTRADO (Excluído).")
                st.markdown("**Detalhes do registro excluído:**")
                st.dataframe(found_excluded)
                
                # Try to explain why
                record = found_excluded.iloc[0]
                reasons = []
                
                # Check Model
                model = str(record.get('Model', '')).lower()
                from app.utils.constants import NOTEBOOK_MODEL_PATTERNS, EXCLUDE_MODEL_PATTERNS
                
                is_notebook = any(p in model for p in NOTEBOOK_MODEL_PATTERNS)
                is_excluded = any(p in model for p in EXCLUDE_MODEL_PATTERNS)
                
                if is_excluded:
                    reasons.append(f"Modelo '{record.get('Model')}' contém padrão de exclusão (ex: 'virtual', 'vm', 'desktop').")
                elif not is_notebook:
                    reasons.append(f"Modelo '{record.get('Model')}' não foi reconhecido como notebook (Dell Latitude/Pro, MacBook, OptiPlex).")
                
                # Check OS/Type if notebook check failed
                if not is_notebook and not is_excluded:
                    os_val = str(record.get('OS', '')).lower()
                    type_val = str(record.get('Type', '')).lower()
                    
                    if 'linux' not in os_val and 'ubuntu' not in os_val and 'linux' not in type_val:
                         reasons.append("Não possui OS (Linux/Ubuntu) ou Type (Notebook/Linux) identificados como válidos.")

                if reasons:
                    st.write("**Possíveis motivos:**")
                    for r in reasons:
                        st.markdown(f"- {r}")
                else:
                    st.write("Motivo exato não identificado automaticamente. Verifique as colunas Model, OS e Type.")
                    
            else:
                st.error(f"❌ O serial **{search_serial}** NÃO FOI ENCONTRADO em nenhum lugar do arquivo Excel carregado.")
                st.info("Verifique se digitou corretamente ou se o arquivo Excel está atualizado.")
