


import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from app.services.barcode_handler import process_serial
from app.services.comparator import compare_and_flag


@st.dialog("⚠️ Serial Não Encontrado")
def show_not_found_dialog(serial):
    """
    Modal de confirmação quando serial não for encontrado na base.
    Permite ao usuário decidir se mantém ou remove o registro.
    """
    st.warning(f"O serial **{serial}** não foi encontrado na base de dados.")
    st.info("💡 Isso pode ter ocorrido devido a uma leitura incorreta do código de barras ou equipamento não cadastrado.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Remover do Registro", use_container_width=True, type="primary"):
            # Remove última entrada (que foi a não encontrada)
            if st.session_state.scanned_items:
                st.session_state.scanned_items.pop(0)
                st.session_state.last_scan_result = st.session_state.scanned_items[0] if st.session_state.scanned_items else None
            st.session_state.blocked_scan = False
            st.session_state.scanner_input = ""
            st.toast("✅ Registro removido com sucesso!", icon="✅")
            st.rerun()
    
    with col2:
        if st.button("✅ Manter e Continuar", use_container_width=True):
            st.session_state.blocked_scan = False
            st.session_state.scanner_input = ""
            st.toast("ℹ️ Registro mantido. Continue a verificação.", icon="ℹ️")
            st.rerun()


def render_scanner_input():
    """
    Renderiza o campo de input para o leitor de código de barras.
    O Zebra DS22 envia <DATA><ENTER>, o que aciona o reload do Streamlit.
    """
    st.markdown("### 📷 Scanner de Equipamentos")
    
    # Valida se há dataframe carregado
    if st.session_state.dataframe is None:
        st.warning("⚠️ Carregue uma base de dados na aba 'Upload' antes de verificar.")
        st.stop()
    
    # Instruções visuais
    st.info("💡 Clique no campo abaixo e bipe o equipamento com o leitor.")
    
    # Inicializa session state para histórico se não existir
    if 'scanned_items' not in st.session_state:
        st.session_state.scanned_items = []
        
    if 'last_scan_result' not in st.session_state:
        st.session_state.last_scan_result = None
    
    # Inicializa estado de bloqueio
    if 'blocked_scan' not in st.session_state:
        st.session_state.blocked_scan = False
    
    if 'blocked_serial' not in st.session_state:
        st.session_state.blocked_serial = None
    
    # Se bloqueado, mostrar modal e desabilitar input
    if st.session_state.blocked_scan:
        show_not_found_dialog(st.session_state.blocked_serial)
        st.text_input(
            "Bipar código do equipamento:",
            key="scanner_input_disabled",
            disabled=True,
            placeholder="Resolva a verificação anterior antes de continuar...",
            help="Serial não encontrado. Resolva o modal acima para continuar."
        )
        st.stop()

    # Callback para processar o input assim que o Enter for pressionado
    def on_scan():
        serial_input = st.session_state.scanner_input
        if serial_input:
            # 1. Processa e valida formato do serial
            valid_format, processed_serial, message = process_serial(serial_input)
            
            result = None
            
            if valid_format:
                # 2. Compara com a base de dados
                result = compare_and_flag(processed_serial, st.session_state.dataframe)
                
                # Adiciona timestamp com horário de Brasília (não do servidor Streamlit)
                result['timestamp'] = datetime.now(ZoneInfo("America/Sao_Paulo"))
                
                # Verifica duplicidade na sessão atual
                # IMPORTANTE: Usar serialnumber do resultado, não o input digitado
                # Se buscar por patrimônio 9856, deve verificar duplicidade pelo serial JQHP813
                serial_to_check = result.get('serialnumber', processed_serial) if result.get('found') else processed_serial
                already_scanned = any(item['serialnumber'] == serial_to_check for item in st.session_state.scanned_items)
                
                if already_scanned:
                     st.toast(f"⚠️ Item '{serial_to_check}' já verificado nesta sessão!", icon="⚠️")
                     # Limpa o input e retorna SEM adicionar ao histórico
                     st.session_state.scanner_input = ""
                     return
                
                # Item não é duplicata, prosseguir com feedback e registro
                if result['found']:
                    if result['requires_adjustment']:
                        st.toast(f"⚠️ Atenção: {processed_serial} requer ajuste!", icon="⚠️")
                    else:
                        st.toast(f"✅ {processed_serial} verificado com sucesso!", icon="✅")
                    
                    # Adiciona ao histórico (topo)
                    st.session_state.scanned_items.insert(0, result)
                    st.session_state.last_scan_result = result
                    
                else:
                    # Serial não encontrado - BLOQUEAR próximo scan
                    st.toast(f"❌ {processed_serial} não encontrado na base!", icon="❌")
                    
                    # Adiciona ao histórico mesmo não encontrado
                    st.session_state.scanned_items.insert(0, result)
                    st.session_state.last_scan_result = result
                    
                    # BLOQUEAR scan até decisão do usuário
                    st.session_state.blocked_scan = True
                    st.session_state.blocked_serial = processed_serial
                    st.session_state.scanner_input = ""
                    st.rerun()  # Força reload para mostrar modal
                
            else:
                # Serial inválido (curto ou caracteres ruins)
                st.toast(message, icon="❌")
                # Cria um objeto de erro para exibir no componente principal se desejar
                # Por hora, mantemos o anterior ou None, pois foi erro de input
            
            # Limpa o input para próxima leitura
            st.session_state.scanner_input = ""

    # Input field
    st.text_input(
        "Bipar código do equipamento:",
        key="scanner_input",
        placeholder="Aguardando leitura...",
        on_change=on_scan,
        help="Certifique-se que o leitor USB está conectado."
    )

