
import re
import streamlit as st
from typing import Tuple, Optional

def process_serial(serial: str) -> Tuple[bool, str, Optional[str]]:
    """
    Processa e valida um serial lido pelo scanner.
    
    Args:
        serial: String do serial lido
        
    Returns:
        Tuple contendo:
        - bool: Se é válido
        - str: Serial processado/limpo (ou mensagem de erro)
        - str/None: Mensagem de status detalhada
    """
    if not serial:
        return False, "Serial vazio", "O campo de leitura está vazio."
        
    # Limpeza básica (remove espaços extras nas pontas)
    clean_serial = serial.strip()
    
    # Remove caracteres não imprimíveis que scanners podem enviar
    clean_serial = "".join(ch for ch in clean_serial if ch.isprintable())
    
    # Validação de tamanho mínimo (ajustar conforme padrão da Anbima se necessário)
    if len(clean_serial) < 3:
        return False, "Serial muito curto", f"O serial '{clean_serial}' parece incompleto."
        
    # Validação de duplicidade na sessão
    if 'scanned_items' not in st.session_state:
        st.session_state.scanned_items = []
        
    # Verifica se já foi lido (case insensitive se necessário)
    if clean_serial in st.session_state.scanned_items:
        return False, clean_serial, f"O item '{clean_serial}' já foi verificado nesta sessão!"
        
    return True, clean_serial, "Serial válido"
