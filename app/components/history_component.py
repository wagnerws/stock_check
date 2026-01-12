"""
Componente de visualização de histórico de verificações.

Permite ao usuário consultar sessões anteriores, visualizar detalhes
e exportar dados.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any
from app.services.history_manager import (
    list_sharepoint_sessions,
    load_session_from_sharepoint,
    delete_sharepoint_session
)
from app.services.excel_handler import export_scanned_history


def render_history_component():
    """
    Renderiza interface de histórico de verificações.
    
    SEGURANÇA: Só permite acesso após upload da base (compliance).
    
    Funcionalidades:
    - Lista de sessões anteriores
    - Visualização de sessão selecionada
    - Exportação para Excel
    - Deleção de sessão
    """
    st.markdown("## 📜 Histórico de Verificações")
    
    # COMPLIANCE: Bloquear acesso sem base carregada
    if st.session_state.dataframe is None:
        st.warning("🔒 **Acesso Restrito**")
        st.info("Por questões de compliance e segurança, o histórico só pode ser acessado após fazer upload da base de dados na aba 'Upload'.")
        st.stop()
    
    # Listar sessões disponíveis
    sessions = list_sharepoint_sessions()
    
    if not sessions:
        st.info("📭 Nenhuma sessão anterior encontrada. Comece a verificar equipamentos!")
        return
    
    st.info(f"📊 {len(sessions)} sessão(ões) disponível(eis)")
    
    # Criar lista de opções para dropdown
    session_options = {}
    for session in sessions:
        session_id = session['session_id']
        started = session.get('started_at', 'N/A')
        total = session.get('total', 0)
        
        # Formatar data para exibição
        try:
            dt = datetime.fromisoformat(started)
            date_str = dt.strftime("%d/%m/%Y %H:%M")
        except:
            date_str = "Data desconhecida"
        
        label = f"{date_str} - {total} itens"
        session_options[label] = session_id
    
    # Dropdown para selecionar sessão
    selected_label = st.selectbox(
        "Selecione uma sessão:",
        options=list(session_options.keys()),
        index=0
    )
    
    if selected_label:
        selected_id = session_options[selected_label]
        
        # Carregar dados da sessão
        session_data = load_session_from_sharepoint(selected_id)
        
        if session_data:
            _render_session_details(session_data)
        else:
            st.error("❌ Erro ao carregar dados da sessão.")


def _render_session_details(session_data: Dict[str, Any]):
    """Renderiza detalhes de uma sessão específica."""
    
    st.divider()
    
    # Cabeçalho com informações da sessão
    col1, col2, col3 = st.columns(3)
    
    items = session_data.get('items', [])
    total = len(items)
    total_ok = sum(1 for i in items if i.get('found') and not i.get('requires_adjustment'))
    total_adj = sum(1 for i in items if i.get('requires_adjustment'))
    total_err = sum(1 for i in items if not i.get('found'))
    
    col1.metric("Total Verificado", total)
    col2.metric("✅ OK", total_ok)
    col3.metric("⚠️ Requer Ajuste", total_adj, delta_color="inverse")
    
    # Informações adicionais
    st.caption(f"**Arquivo Lansweeper:** {session_data.get('lansweeper_file', 'N/A')}")
    st.caption(f"**Início:** {session_data.get('started_at', 'N/A')}")
    st.caption(f"**Fim:** {session_data.get('ended_at', 'N/A')}")
    
    st.divider()
    
    # Botões de ação
    col_export, col_delete = st.columns([0.7, 0.3])
    
    with col_export:
        if st.button("📥 Exportar para Excel", use_container_width=True, type="primary"):
            # Gerar Excel
            excel_data = export_scanned_history(items)
            
            if excel_data:
                timestamp = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y%m%d_%H%M%S")
                filename = f"sessao_{session_data['session_id']}.xlsx"
                
                st.download_button(
                    label="⬇️ Baixar Arquivo Excel",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    with col_delete:
        if st.button("🗑️ Deletar Sessão", use_container_width=True, type="secondary"):
            if delete_sharepoint_session(session_data['session_id']):
                st.success("✅ Sessão deletada com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao deletar sessão.")
    
    st.divider()
    
    # Tabela de itens verificados
    st.markdown("### 📋 Itens Verificados")
    
    if items:
        history_data = []
        for item in items:
            # Format ativo as integer if numeric
            ativo_value = item.get('ativo')
            if ativo_value:
                try:
                    ativo_display = str(int(float(ativo_value)))
                except (ValueError, TypeError):
                    ativo_display = str(ativo_value)
            else:
                ativo_display = '-'
            
            history_data.append({
                "Timestamp": item.get('timestamp', 'N/A'),
                "Serial": item.get('serialnumber', 'N/A'),
                "Patrimônio": ativo_display,
                "Estado": item['state'].upper() if item.get('found') else "N/A",
                "Status": item.get('status_emoji', '❓')
            })
        
        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Timestamp": st.column_config.DatetimeColumn("Hora", format="DD/MM/YYYY HH:mm:ss"),
                "Serial": st.column_config.TextColumn("Serial", width="medium"),
                "Patrimônio": st.column_config.TextColumn("Patrimônio", width="small"),
                "Estado": st.column_config.TextColumn("Estado", width="small"),
                "Status": st.column_config.TextColumn("St", width="small")
            },
            height=400
        )
    else:
        st.info("Nenhum item nesta sessão.")
