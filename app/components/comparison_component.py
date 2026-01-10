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
    
    # Determine styles based on status
    status_color = "gray"
    if result['found']:
        if result['requires_adjustment']:
            status_color = "orange"
        else:
            status_color = "green"
    else:
        status_color = "red"
        
    # Main Result Card
    with st.container(border=True):
        st.markdown(f"### {result['status_emoji']} {result['status_message']}")
        
        # Serial display with large font
        st.markdown(
            f"""
            <div style="text-align: center; margin: 10px 0;">
                <span style="font-size: 1.2rem; color: gray;">SERIAL NUMBER</span><br>
                <span style="font-size: 2.5rem; font-weight: bold; font-family: monospace;">{result['serialnumber']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Display Patrimônio (Ativo) if available
        if result.get('ativo'):
            st.markdown(
                f"""
                <div style="text-align: center; margin: 5px 0;">
                    <span style="font-size: 0.9rem; color: gray;">Patrimônio:</span>
                    <span style="font-size: 1.2rem; font-weight: bold;">{result['ativo']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if result['found']:
            # Details Section
            if result['requires_adjustment']:
                st.warning("⚠️ **AÇÃO NECESSÁRIA:** Baixa Manual no Lansweeper", icon="⚠️")
                
                # Context info in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.caption("Hostname")
                    st.markdown(f"**{result.get('name', 'N/A')}**")
                with col2:
                    st.caption("Último Usuário")
                    st.markdown(f"**{result.get('lastuser', 'N/A')}**")
            else:
                # Stock/Good state
                st.success(f"Equipamento classificado como: **{result['state'].upper()}**", icon="✅")
        
        else:
            # Not found
            st.error("Serial não cadastrado na base importada.", icon="❌")


def render_comparison_component():
    """
    Renderiza componente de comparação de dados.
    
    Funcionalidades:
    - Display de informações do equipamento encontrado (último bip)
    - Indicadores visuais (✅ OK, ⚠️ Atenção, ❌ Não encontrado)
    - Histórico de verificações em tabela
    - Reset de histórico
    """
def render_session_metrics():
    """
    Renderiza métricas rápidas da sessão de verificação atual.
    """
    if 'scanned_items' not in st.session_state or not st.session_state.scanned_items:
        return

    items = st.session_state.scanned_items
    total = len(items)
    
    # Count stats
    total_ok = sum(1 for i in items if i.get('found') and not i.get('requires_adjustment'))
    total_adj = sum(1 for i in items if i.get('requires_adjustment'))
    total_err = sum(1 for i in items if not i.get('found'))
    
    # Render Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Verificado", total)
    m2.metric("✅ Em Ordem", total_ok)
    m3.metric("⚠️ Ajustar (Active)", total_adj, delta_color="inverse")
    
    st.divider()


def render_comparison_component():
    """
    Renderiza componente de comparação de dados.
    """
    # 1. Resultados em Tempo Real
    if 'last_scan_result' in st.session_state and st.session_state.last_scan_result:
        st.markdown("### 🔍 Resultado da Leitura")
        render_comparison_result(st.session_state.last_scan_result)

    # 2. Histórico de Verificações
    if 'scanned_items' in st.session_state and st.session_state.scanned_items:
        st.divider()
        
        # Header com botão de limpar
        col_head, col_btn = st.columns([0.8, 0.2])
        col_head.markdown("#### 🕒 Histórico da Sessão")
        
        if col_btn.button("🗑️ Limpar Sessão", type="secondary", use_container_width=True):
            st.session_state.scanned_items = []
            st.session_state.last_scan_result = None
            st.rerun()

        # Tabela simplificada
        history_data = []
        for item in st.session_state.scanned_items:
            history_data.append({
                "Timestamp": item['timestamp'], # Keep as datetime for sorting/formatting by column_config
                "Serial": item['serialnumber'],
                "Estado": item['state'].upper() if item.get('found') else "N/A",
                "Status": item['status_emoji']
            })
            
        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Timestamp": st.column_config.DatetimeColumn("Hora", format="HH:mm:ss"),
                "Serial": st.column_config.TextColumn("Serial", width="medium"),
                "Estado": st.column_config.TextColumn("Estado", width="small"),
                "Status": st.column_config.TextColumn("St", width="small")
            },
            height=300
        )
    else:
        st.info("💡 Bipe um equipamento para começar.")
