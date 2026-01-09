
import streamlit as st
import pandas as pd
from datetime import datetime
from app.services.barcode_handler import process_serial
from app.services.comparator import compare_and_flag

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
                
                # Adiciona timestamp
                result['timestamp'] = datetime.now()
                
                # Verifica duplicidade na sessão atual (opcional mas recomendado)
                # Se já estiver na lista desta sessão, avisar mas permitir (ou bloquear)
                # Aqui vamos permitir mas avisar via toast
                already_scanned = any(item['serialnumber'] == processed_serial for item in st.session_state.scanned_items)
                
                if already_scanned:
                     st.toast(f"⚠️ Item '{processed_serial}' já verificado nesta sessão!", icon="⚠️")
                else:
                    if result['found']:
                        if result['requires_adjustment']:
                            st.toast(f"⚠️ Atenção: {processed_serial} requer ajuste!", icon="⚠️")
                        else:
                            st.toast(f"✅ {processed_serial} verificado com sucesso!", icon="✅")
                    else:
                        st.toast(f"❌ {processed_serial} não encontrado na base!", icon="❌")

                # Adiciona ao histórico (topo)
                st.session_state.scanned_items.insert(0, result)
                st.session_state.last_scan_result = result
                
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

