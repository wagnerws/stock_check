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
    - Display de informações do equipamento encontrado
    - Indicadores visuais (✅ OK, ⚠️ Atenção, ❌ Não encontrado)
    - Histórico de verificações
    - Contador de progresso
    """
    st.info("ℹ️ Componente de comparação em tempo real será implementado aqui")
    st.markdown("""
    **Funcionalidades planejadas:**
    - 📊 Histórico de verificações
    - 📈 Contador de progresso
    - 🔍 Busca rápida de equipamentos
    """)
