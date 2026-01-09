
import streamlit as st
from app.services.barcode_handler import process_serial

def render_scanner_input():
    """
    Renderiza o campo de input para o leitor de código de barras.
    O Zebra DS22 envia <DATA><ENTER>, o que aciona o reload do Streamlit.
    """
    st.markdown("### 📷 Scanner de Equipamentos")
    
    # Instruções visuais
    st.info("💡 Clique no campo abaixo e bipe o equipamento com o leitor.")
    
    # Inicializa session state para histórico se não existir
    if 'scanned_items' not in st.session_state:
        st.session_state.scanned_items = []
        
    if 'last_scan_message' not in st.session_state:
        st.session_state.last_scan_message = None

    # Callback para processar o input assim que o Enter for pressionado
    def on_scan():
        serial = st.session_state.scanner_input
        if serial:
            valid, processed_serial, message = process_serial(serial)
            
            if valid:
                # Adiciona à lista de verificados
                st.session_state.scanned_items.insert(0, processed_serial) # Adiciona no topo
                st.session_state.last_scan_message = {"type": "success", "text": f"✅ Item '{processed_serial}' registrado!"}
                st.toast(f"Item '{processed_serial}' registrado!", icon="✅")
            else:
                # Se for erro de duplicidade
                if "já foi verificado" in message:
                    st.session_state.last_scan_message = {"type": "warning", "text": f"⚠️ {message}"}
                    st.toast(message, icon="⚠️")
                else:
                    st.session_state.last_scan_message = {"type": "error", "text": f"❌ {message}"}
                    st.toast(message, icon="❌")
            
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
    
    # Exibir última mensagem de status (persistente)
    if st.session_state.last_scan_message:
        msg = st.session_state.last_scan_message
        if msg["type"] == "success":
            st.success(msg["text"])
        elif msg["type"] == "warning":
            st.warning(msg["text"])
        else:
            st.error(msg["text"])

    # Exibir histórico recente
    if st.session_state.scanned_items:
        st.divider()
        st.markdown("#### 📋 Itens Verificados Nesta Sessão")
        
        # Botão para limpar histórico
        if st.button("Limpar Histórico", type="secondary"):
            st.session_state.scanned_items = []
            st.session_state.last_scan_message = None
            st.rerun()
            
        # Lista simples dos últimos itens
        for item in st.session_state.scanned_items[:5]:
            st.text(f"• {item}")
            
        if len(st.session_state.scanned_items) > 5:
            st.caption(f"... e mais {len(st.session_state.scanned_items) - 5} itens")

