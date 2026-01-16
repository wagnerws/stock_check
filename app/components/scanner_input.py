


import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from app.services.barcode_handler import process_serial
from app.services.comparator import compare_and_flag
from app.services.history_manager import save_session_to_sharepoint


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
        if st.button("🗑️ Remover do Registro", use_container_width=True, type="primary", key="btn_remove"):
            # Remove última entrada (que foi a não encontrada)
            if st.session_state.scanned_items:
                st.session_state.scanned_items.pop(0)
                st.session_state.last_scan_result = st.session_state.scanned_items[0] if st.session_state.scanned_items else None
            st.session_state.blocked_scan = False
            st.session_state.blocked_serial = None
            st.session_state.scanner_input = ""
            st.session_state.force_verification_tab = True  # Força voltar para aba Verificação
            st.toast("✅ Registro removido com sucesso!", icon="✅")
            st.rerun()
    
    with col2:
        if st.button("✅ Manter e Continuar", use_container_width=True, key="btn_keep"):
            st.session_state.blocked_scan = False
            st.session_state.blocked_serial = None
            st.session_state.scanner_input = ""
            st.session_state.force_verification_tab = True  # Força voltar para aba Verificação
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
                    _auto_save_session()  # AUTO-SAVE
                    
                else:
                    # Serial não encontrado - BLOQUEAR próximo scan
                    st.toast(f"❌ {processed_serial} não encontrado na base!", icon="❌")
                    
                    # Adiciona ao histórico mesmo não encontrado
                    st.session_state.scanned_items.insert(0, result)
                    st.session_state.last_scan_result = result
                    _auto_save_session()  # AUTO-SAVE
                    
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


def _auto_save_session():
    """Salva automaticamente a sessão atual em storage local."""
    try:
        # Inicializa session_id se não existir (APENAS UMA VEZ)
        if 'current_session_id' not in st.session_state:
            st.session_state.current_session_id = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y%m%d_%H%M%S")
            st.session_state.session_started_at = datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat()
        
        # Preparar items convertendo datetime para string
        items_serializable = []
        for item in st.session_state.scanned_items:
            item_copy = item.copy()
            # Converter timestamp datetime para string ISO
            if 'timestamp' in item_copy and isinstance(item_copy['timestamp'], datetime):
                item_copy['timestamp'] = item_copy['timestamp'].isoformat()
            items_serializable.append(item_copy)
        
        # Preparar dados da sessão (INCLUINDO session_id fixo)
        session_data = {
            'session_id': st.session_state.current_session_id,  # MESMO ID sempre
            'started_at': st.session_state.get('session_started_at'),
            'lansweeper_file': st.session_state.get('filename', 'N/A'),
            'items': items_serializable
        }
        
        # Salvar (silenciosamente, sem mensagens)
        # Isso SOBRESCREVE o arquivo existente
        save_session_to_sharepoint(session_data)
        
    except Exception as e:
        # Mostrar erro apenas em desenvolvimento
        st.error(f"Erro ao salvar sessão: {str(e)}")

