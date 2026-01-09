
import streamlit as st
import pandas as pd
from datetime import datetime
from app.services.excel_handler import export_adjustment_list, export_scanned_history

def render_report_component():
    """
    Renderiza o componente de relatórios e exportação.
    Permite baixar lista de ajustes e histórico completo.
    """
    st.markdown("### 📊 Relatórios e Exportação")
    
    # 1. Verifica se há itens escaneados
    if 'scanned_items' not in st.session_state or not st.session_state.scanned_items:
        st.info("ℹ️ Nenhum item verificado nesta sessão para exportar.")
        return

    scanned_items = st.session_state.scanned_items
    total_items = len(scanned_items)
    
    # 2. Filtrar itens que requerem ajuste ("active")
    items_for_adjustment = [item for item in scanned_items if item.get('requires_adjustment')]
    total_adjustment = len(items_for_adjustment)
    
    # 3. Métricas Rápidas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Verificado", total_items)
    with col2:
        st.metric("Requerem Ajuste (Active)", total_adjustment, delta_color="inverse")
        
    st.divider()
    
    # 4. Seção de Download
    st.markdown("#### 📥 Opções de Download")
    
    col_down1, col_down2 = st.columns(2)
    
    # --- Download 1: Lista de Ajustes ---
    with col_down1:
        st.markdown("**Lista de Ajustes (Lansweeper)**")
        st.caption("Apenas itens com estado 'active'. Use para dar baixa.")
        
        if total_adjustment > 0:
            # Convert list of dicts to DataFrame for the handler
            df_adjustment = pd.DataFrame(items_for_adjustment)
            
            # Generate excel bytes
            excel_adjustment = export_adjustment_list(df_adjustment)
            
            st.download_button(
                label="📥 Baixar Lista de Ajustes",
                data=excel_adjustment,
                file_name="ajustar_lansweeper.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn_download_adjustment",
                type="primary"
            )
        else:
            st.success("✅ Nenhum item requer ajuste!")
            
    # --- Download 2: Histórico Completo ---
    with col_down2:
        st.markdown("**Histórico Completo da Sessão**")
        st.caption("Todos os itens verificados (com ou sem ajuste).")
        
        # Generate filename with current date: verificacao_stock_dd_mm_yyyy.xlsx
        current_date = datetime.now().strftime("%d_%m_%Y")
        filename_history = f"verificacao_stock_{current_date}.xlsx"
        
        # Generate excel bytes
        excel_history = export_scanned_history(scanned_items)
        
        st.download_button(
            label="📥 Baixar Histórico Completo",
            data=excel_history,
            file_name=filename_history,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="btn_download_history"
        )
        
    # 5. Preview Table (Opcional, apenas ajustes)
    if total_adjustment > 0:
        st.divider()
        st.markdown("#### 👀 Prévia: Itens para Ajuste")
        
        df_preview = pd.DataFrame(items_for_adjustment)
        # Select relevant columns for preview
        cols_to_show = ['serialnumber', 'state', 'name', 'lastuser']
        # Filter only existing columns
        cols_to_show = [c for c in cols_to_show if c in df_preview.columns]
        
        st.dataframe(
            df_preview[cols_to_show],
            use_container_width=True,
            hide_index=True
        )
