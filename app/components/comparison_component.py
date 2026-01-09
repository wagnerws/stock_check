"""
Componente de comparação e exibição de resultados.

Responsável por mostrar resultado da verificação em tempo real.
"""

import streamlit as st
from typing import Dict, Any


def render_comparison_result(result: Dict[str, Any]):
    """
    Renderiza resultado da comparação de um equipamento.
    
    Args:
        result: Dicionário com informações do equipamento e status
        
    Funcionalidades:
    - Display de informações do equipamento encontrado
    - Indicadores visuais (✅ OK, ⚠️ Atenção, ❌ Não encontrado)
    - Informações de usuário e hostname para equipamentos ativos
    """
    if not result:
        return
    
    # Display header with emoji and status
    st.markdown(f"### {result['status_emoji']} {result['status_message']}")
    
    if result['found']:
        # Show serial number
        st.info(f"**Serial:** {result['serialnumber']}")
        
        # If equipment requires adjustment, show additional info
        if result['requires_adjustment']:
            st.warning("⚠️ **Este equipamento requer ajuste no Lansweeper**")
            
            # Display hostname and user in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="🖥️ Hostname",
                    value=result.get('name', 'N/A')
                )
            
            with col2:
                st.metric(
                    label="👤 Usuário",
                    value=result.get('lastuser', 'N/A')
                )
            
            st.markdown("---")
            st.markdown("📝 **Ação necessária:** Atualizar estado deste equipamento no Lansweeper")
        else:
            # Equipment is OK
            st.success(f"✅ Estado: **{result['state'].upper()}**")
    else:
        # Not found in database
        st.error("❌ Este serial não foi encontrado na base de dados do Lansweeper")
        st.info(f"**Serial buscado:** {result['serialnumber']}")


def render_comparison_component():
    """
    Renderiza componente de comparação de dados.
    
    Funcionalidades:
    - Display de informações do equipamento encontrado (último bip)
    - Indicadores visuais (✅ OK, ⚠️ Atenção, ❌ Não encontrado)
    - Histórico de verificações em tabela
    - Reset de histórico
    """
    st.markdown("### 📊 Resultado da Verificação")
    
    # 1. Exibir resultado do último scan (destaque)
    if 'last_scan_result' in st.session_state and st.session_state.last_scan_result:
        result = st.session_state.last_scan_result
        
        # Container visual para o resultado
        container_color = "green"
        if result.get('requires_adjustment'):
             container_color = "orange" # ou yellow
        elif not result.get('found'):
             container_color = "red"
             
        # Usando st.container com border (Streamlit 1.30+) ou apenas markdown com style
        with st.container(border=True):
             render_comparison_result(result)

    # 2. Histórico de Verificações
    if 'scanned_items' in st.session_state and st.session_state.scanned_items:
        st.divider()
        col_hist_1, col_hist_2 = st.columns([0.8, 0.2])
        col_hist_1.markdown("#### 🕒 Histórico Recente")
        
        if col_hist_2.button("Limpar", type="primary"):
            st.session_state.scanned_items = []
            st.session_state.last_scan_result = None
            st.rerun()

        # Prepara dados para tabela
        # Precisamos converter a lista de dicts para um formato amigável
        history_data = []
        for item in st.session_state.scanned_items:
            history_data.append({
                "Hora": item['timestamp'].strftime("%H:%M:%S"),
                "Serial": item['serialnumber'],
                "Status": item['status_emoji'],
                "Mensagem": item['status_message'],
                "Ação": "Ajustar" if item.get('requires_adjustment') else "-"
            })
            
        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn("St", width="small"),
                "Ação": st.column_config.TextColumn("Ação", width="medium"),
            }
        )
    else:
        st.info("Nenhum item verificado nesta sessão.")
