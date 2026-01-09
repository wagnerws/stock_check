"""
Entry point da aplicação Stock Check.

Para executar: streamlit run app/main.py
"""

import streamlit as st
from app.config import PAGE_TITLE, PAGE_ICON
from app.components.upload_component import render_upload_component

# Configuração da página
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'lansweeper_data' not in st.session_state:
    st.session_state.lansweeper_data = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# Header principal
st.title("📦 Stock Check - Controle de Estoque")
st.markdown(
    """
    Sistema de verificação física de equipamentos com integração ao **Lansweeper**.
    
    ---
    """
)

# Main content
tab1, tab2, tab3 = st.tabs(["📥 Upload", "🔍 Verificação", "📊 Relatórios"])

with tab1:
    # Upload component
    df = render_upload_component()
    
    if df is not None:
        st.success(f"✅ Base carregada: **{st.session_state.filename}**")

with tab2:
    st.info("🚧 **Em desenvolvimento** - Módulo de verificação por código de barras")
    
    if st.session_state.lansweeper_data is not None:
        st.markdown(
            f"""
            **Base carregada:** {st.session_state.filename}  
            **Registros:** {len(st.session_state.lansweeper_data)}  
            **Status:** Pronto para verificação
            """
        )
    else:
        st.warning("⚠️ Faça upload da base Lansweeper na aba **Upload** primeiro")

with tab3:
    st.info("🚧 **Em desenvolvimento** - Relatórios e estatísticas")
    
    if st.session_state.lansweeper_data is not None:
        st.markdown("**Próximas funcionalidades:**")
        st.markdown(
            """
            - 📈 Análise de distribuição por estado
            - 🔍 Equipamentos que requerem ajuste
            - 📤 Exportação de relatórios em Excel
            """
        )

# Sidebar informativo
with st.sidebar:
    st.header("ℹ️ Informações")
    
    if st.session_state.lansweeper_data is not None:
        st.success(f"✅ Base carregada")
        st.caption(f"Arquivo: {st.session_state.filename}")
        st.caption(f"Registros: {len(st.session_state.lansweeper_data)}")
    else:
        st.warning("⚠️ Nenhuma base carregada")
    
    st.divider()
    
    st.markdown(
        """
        **Estados Válidos:**
        - ✅ Stock (Em estoque)
        - 🔧 Broken (Quebrado)
        - 🚨 Stolen (Roubado)
        - ⚙️ In Repair (Em reparo)
        - 📦 Old (Antigo)
        - ⚠️ Active (Requer ajuste)
        """
    )
    
    st.divider()
    
    st.markdown("**Versão:** 0.2.0")
    st.markdown("**Stack:** Streamlit + Python + Pandas")

