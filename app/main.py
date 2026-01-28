
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

    # Custom CSS for Sidebar Navigation Cards
    st.markdown("""
        <style>
        /* Remover padding padrão do topo da sidebar para compactar */
        section[data-testid="stSidebar"] > div > div:first-child {
            padding-top: 2rem;
        }

        /* remover margem negativa anterior pois vamos esconder o elemento */
        [data-testid="stSidebar"] [data-testid="stRadio"] {
            margin-top: 0 !important;
        }
        
        /* 🔴 Ocultar COMPLETAMENTE o Label do Widget (que o usuário mostrou no print) */
        [data-testid="stSidebar"] [data-testid="stRadio"] > label[data-testid="stWidgetLabel"] {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] > div {
            gap: 8px; /* Espaçamento vertical entre os cards */
            width: 100%;
        }

        /* Card Individual (Label) */
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            background-color: #262730 !important; /* Fundo Escuro */
            color: #FAFAFA !important; /* Texto Claro */
            padding: 12px 16px !important; /* Reduzido levemente para compactar */
            width: 100% !important;
            border-radius: 8px !important;
            border: 1px solid #41444C !important;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
        }

        /* Hover Effect */
        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
            background-color: #31333F !important;
            border-color: #FAFAFA !important;
            transform: translateY(-2px);
        }

        /* Estado Selecionado (Active) */
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
            background-color: #0E1117 !important;
            border: 1px solid #FF4B4B !important;
            color: #FF4B4B !important;
            font-weight: bold !important;
            box-shadow: inset 4px 0 0 0 #FF4B4B !important; /* Destaque lateral esquerdo */
        }

        /* 🔴 ESCONDER A BOLINHA DO RADIO (Input Nativo) */
        [data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
            display: none !important;
            width: 0 !important;
        }

        /* Ajuste do Texto/Conteúdo */
        [data-testid="stSidebar"] [data-testid="stRadio"] label [data-testid="stMarkdownContainer"] {
            width: 100%;
            text-align: left;
        }
        
        [data-testid="stSidebar"] [data-testid="stRadio"] label [data-testid="stMarkdownContainer"] p {
            font-size: 1rem !important;
            margin: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables if they don't exist
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = None
    if 'filename' not in st.session_state:
        st.session_state.filename = None

    # Sidebar
    st.sidebar.title("📦 Stock Check")
    st.sidebar.caption("v0.9.0 - Linux Filters & Debug Tool")
    
    st.sidebar.divider()
    
    # Navegação na Sidebar
    st.sidebar.markdown("### 🧭 Navegação")
    
    # Seletor de abas (substitui st.tabs)
    tab_options = ["📤 Upload", "🔍 Verificação", "📊 Relatórios", "📜 Histórico"]
    
    # Inicializar aba ativa no session_state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "📤 Upload"
    
    # Se houver flag para forçar aba Verificação, aplicar
    if st.session_state.get('force_verification_tab', False):
        st.session_state.active_tab = "🔍 Verificação"
        st.session_state.force_verification_tab = False  # Resetar flag
    
    # Seletor
    selected_tab = st.sidebar.radio(
        "Selecione o módulo:",
        tab_options,
        index=tab_options.index(st.session_state.active_tab),
        key="tab_selector",
        label_visibility="collapsed"
    )
    
    # Atualizar aba ativa
    st.session_state.active_tab = selected_tab
    
    st.sidebar.divider()
    
    # Status na sidebar (abaixo do menu)
    st.sidebar.markdown("### 📊 Status da Sessão")
    if st.session_state.dataframe is not None:
        st.sidebar.success("✅ Base Carregada")
        st.sidebar.metric("Total de Itens", len(st.session_state.dataframe))
    else:
        st.sidebar.warning("⚠️ Nenhuma base")

    items_verified = len(st.session_state.scanned_items) if 'scanned_items' in st.session_state else 0
    st.sidebar.metric("Itens Verificados", items_verified)

    st.sidebar.divider()
    
    # Legenda (colapsável para economizar espaço)
    with st.sidebar.expander("ℹ️ Legenda de Estados"):
        st.markdown(
            """
            - ✅ **Stock**
            - 🔧 **Broken**
            - 🚨 **Stolen**
            - ⚙️ **In Repair**
            - 📦 **Old**
            - 🏷️ **Reservado**
            """
        )
    
    
    # Renderizar conteúdo baseado na aba selecionada
    if selected_tab == "📤 Upload":
        # Upload component
        df = render_upload_component()
        
        if df is not None:
            # Atualiza session state se necessário (geralmente tratado dentro do component, mas reforçando)
            # st.session_state.dataframe = df (render_upload_component já faz isso)
            pass
    
    elif selected_tab == "🔍 Verificação":
        # Cabeçalho da Seção
        st.markdown("## 🔍 Verificação de Estoque")
        st.markdown("Utilize o scanner para bipar os códigos de barras dos equipamentos. O sistema comparará automaticamente com a base carregada.")
        st.divider()

        # Layout lado a lado: Resultado | Scanner
        col_result, col_scanner = st.columns(2)
        
        with col_result:
            # 1. Resultado da Leitura
            render_comparison_component()
            
        with col_scanner:
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
