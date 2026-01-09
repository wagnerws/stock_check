

import streamlit as st
import sys
import os

# Adicionar a raiz do projeto ao sys.path para garantir que imports absolutos (app.config) funcionem
# quando rodar via 'streamlit run app/main.py'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import PAGE_TITLE, PAGE_ICON
from app.components.upload_component import render_upload_component
from app.components.scanner_input import render_scanner_input
from app.components.comparison_component import render_comparison_component, render_session_metrics
from app.components.report_component import render_report_component

def main():
    st.set_page_config(
        page_title="Stock Check - Anbima",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state variables if they don't exist
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = None
    if 'filename' not in st.session_state:
        st.session_state.filename = None

    # Sidebar
    st.sidebar.title("📦 Stock Check")
    st.sidebar.caption("v0.2.1")
    
    st.sidebar.divider()
    
    # Status na sidebar
    if st.session_state.dataframe is not None:
        st.sidebar.success("✅ Base de Dados Carregada")
        st.sidebar.metric("Total de Itens", len(st.session_state.dataframe))
    else:
        st.sidebar.warning("⚠️ Nenhuma base carregada")

    items_verified = len(st.session_state.scanned_items) if 'scanned_items' in st.session_state else 0
    st.sidebar.metric("Itens Verificados (Sessão)", items_verified)

    st.sidebar.divider()
    st.sidebar.info(
        """
        **Estados Válidos:**
        - ✅ Stock
        - 🔧 Broken
        - 🚨 Stolen
        - ⚙️ In Repair
        - 📦 Old
        """
    )
    
    # Main Content
    st.title("Controle de Estoque Físico")
    
    tab1, tab2, tab3 = st.tabs(["📤 Upload", "🔍 Verificação", "📊 Relatórios"])
    
    with tab1:
        # Upload component
        df = render_upload_component()
        
        if df is not None:
            # Atualiza session state se necessário (geralmente tratado dentro do component, mas reforçando)
            # st.session_state.dataframe = df (render_upload_component já faz isso)
            pass
        
    with tab2:
        render_session_metrics()
        render_scanner_input()
        st.divider()
        render_comparison_component()
        
    with tab3:
        render_report_component()

if __name__ == "__main__":
    main()
