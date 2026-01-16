
import streamlit as st
import sys
import os

# Adicionar a raiz do projeto ao sys.path para garantir que imports absolutos (app.config) funcionem
# quando rodar via 'streamlit run app/main.py'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import PAGE_TITLE, PAGE_ICON
from app.components.upload_component import render_upload_component
from app.components.scanner_input import render_scanner_input
from app.components.comparison_component import render_comparison_component, render_session_metrics, render_history_table
from app.components.report_component import render_report_component
from app.components.history_component import render_history_component

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
    st.sidebar.caption("v0.8.0 - Inventory by Model")
    
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
        - 🔖 Reserved
        - 💰 Sold
        """
    )
    
    # Main Content
    st.title("Controle de Estoque Físico")
    
    # Inicializar aba ativa no session_state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "📤 Upload"
    
    # Se houver flag para forçar aba Verificação, aplicar
    if st.session_state.get('force_verification_tab', False):
        st.session_state.active_tab = "🔍 Verificação"
        st.session_state.force_verification_tab = False  # Resetar flag
    
    # Seletor de abas (substitui st.tabs)
    tab_options = ["📤 Upload", "🔍 Verificação", "📊 Relatórios", "📜 Histórico"]
    
    selected_tab = st.radio(
        "Navegação",
        tab_options,
        index=tab_options.index(st.session_state.active_tab),
        horizontal=True,
        label_visibility="collapsed",
        key="tab_selector"
    )
    
    # Atualizar aba ativa
    st.session_state.active_tab = selected_tab
    
    st.divider()
    
    # Renderizar conteúdo baseado na aba selecionada
    if selected_tab == "📤 Upload":
        # Upload component
        df = render_upload_component()
        
        if df is not None:
            # Atualiza session state se necessário (geralmente tratado dentro do component, mas reforçando)
            # st.session_state.dataframe = df (render_upload_component já faz isso)
            pass
    
    elif selected_tab == "🔍 Verificação":
        # 1. Resultado da Leitura (no topo)
        render_comparison_component()
        
        st.divider()
        
        # 2. Scanner de Equipamentos
        render_scanner_input()
        
        st.divider()
        
        # 3. Histórico da Sessão (abaixo do scanner)
        render_history_table()
        
        st.divider()
        
        # 4. Métricas da Sessão
        render_session_metrics()
    
    elif selected_tab == "📊 Relatórios":
        render_report_component()
    
    elif selected_tab == "📜 Histórico":
        render_history_component()

if __name__ == "__main__":
    main()
