import streamlit as st
import pandas as pd
from datetime import datetime
from app.services.excel_handler import export_adjustment_list, export_scanned_history
from app.services.report_metrics import calculate_general_metrics, get_adjustment_items
from app.utils.constants import STATE_EMOJI

def render_report_component():
    """
    Renderiza o componente de relatórios com dashboard analítico e exportação.
    Inclui métricas de progresso, gráficos de distribuição e botões de download.
    """
    st.markdown("## 📊 Dashboard de Relatórios")
    
    # --- 1. Dados e Verificações Iniciais ---
    if 'dataframe' not in st.session_state or st.session_state.dataframe is None:
        st.warning("⚠️ Nenhuma base de dados carregada. Faça o upload na aba 'Upload' primeiro.")
        return

    df_base = st.session_state.dataframe
    scanned_items = st.session_state.scanned_items if 'scanned_items' in st.session_state else []
    
    total_base = len(df_base)
    
    # Use Service for logic
    total_scanned, progress_pct, pendentes = calculate_general_metrics(total_base, scanned_items)
    items_adjustment = get_adjustment_items(scanned_items)
    count_adjustment = len(items_adjustment)
    
    # --- 2. Métricas de Progresso e Análise REMOVIDOS ---
    # Motivo: Solicitação do usuário para simplificar a interface.
    
    st.divider()

    # --- 4. Área de Exportação (Mantida e Melhorada) ---
    # --- 4. Área de Exportação movida para o final ---

    # --- 5. Conciliação de Estoque ---
    st.markdown("#### 📦 Conciliação de Estoque")
    
    # Calculate reconciliation metrics
    from app.services.reconciliation import get_missing_items, get_stock_metrics
    
    scanned_serials = [item['serialnumber'] for item in scanned_items]
    missing_stock = get_missing_items(df_base, scanned_serials)
    metrics = get_stock_metrics(df_base, scanned_items)
    
    # Display metrics
    rec_col1, rec_col2, rec_col3, rec_col4 = st.columns(4)
    
    with rec_col1:
        st.metric("Esperado (Estoque)", metrics['total_expected'])
    with rec_col2:
        st.metric("Bipados (Estoque)", metrics['total_scanned_stock'])
    with rec_col3:
        st.metric("Outros Bipados", metrics.get('total_scanned_others', 0), help="Itens encontrados mas com estado diferente de 'Stock'")
    with rec_col4:
        st.metric("❌ Faltantes", metrics['total_missing'], delta_color="inverse")
    
    st.divider()
    
    # Detalhamento Completo por Estado
    from app.services.reconciliation import calculate_full_reconciliation
    
    st.markdown("##### 📋 Detalhamento por Estado")
    
    df_reconciliation = calculate_full_reconciliation(df_base, scanned_items)
    
    if not df_reconciliation.empty:
        # Adicionar emojis
        df_reconciliation['Estado'] = df_reconciliation['Estado'].apply(
            lambda x: f"{STATE_EMOJI.get(x.lower(), '❓')} {x.title()}"
        )
        
        st.dataframe(
            df_reconciliation,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Estado": st.column_config.TextColumn("Estado", width="medium"),
                "Esperado (Base)": st.column_config.NumberColumn("Esperado (Base)", format="%d"),
                "Encontrado (Físico)": st.column_config.NumberColumn("Encontrado (Físico)", format="%d"),
                "Divergência": st.column_config.NumberColumn("Divergência", format="%d", help="Positivo: Falta item físico | Negativo: Item extra")
            }
        )
    else:
        st.info("Sem dados para conciliação.")

    st.divider()
    
    # Display missing items (Stock only warning)
    if not missing_stock.empty:
        st.warning(f"⚠️ **{len(missing_stock)} item(ns)** marcado(s) como 'Estoque' não foi(ram) bipado(s):")
        
        st.dataframe(
            missing_stock,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Serialnumber": st.column_config.TextColumn("Serial", width="medium"),
                "State": st.column_config.TextColumn("Estado", width="small"),
                "Model": st.column_config.TextColumn("Modelo", width="medium"),
                "Name": st.column_config.TextColumn("Hostname", width="medium"),
                "lastuser": st.column_config.TextColumn("Último Usuário", width="medium")
            }
        )
        
        # Export missing items
        from app.services.excel_handler import export_excel
        from app.services.pdf_generator import generate_conciliation_pdf
        from io import BytesIO
        import openpyxl
        
        # Excel Button
        output = BytesIO()
        missing_stock.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        
        col_btn_excel, col_btn_pdf = st.columns(2)
        
        with col_btn_excel:
            st.download_button(
                label="📥 Excel (.xlsx)",
                data=output.getvalue(),
                file_name=f"faltantes_estoque_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn_missing_stock_xlsx",
                use_container_width=True,
            )
        
        # PDF Button
        with col_btn_pdf:
            try:
                session_data = {
                    'session_id': st.session_state.get('session_id', 'current'),
                    'timestamp': datetime.now()
                }
                
                pdf_bytes = generate_conciliation_pdf(
                    session_data=session_data,
                    missing_stock=missing_stock
                )
                
                st.download_button(
                    label="📄 Relatório PDF",
                    data=pdf_bytes,
                    file_name=f"relatorio_conciliacao_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    key="btn_missing_stock_pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error(f"Erro PDF: {e}")
    else:
        st.success("✅ Todos os itens de estoque conferem com o sistema!")

    st.divider()

    # --- 5. Área de Exportação (Final da Página) ---
    st.markdown("#### 📥 Exportação de Dados")
    
    if total_scanned == 0:
        st.info("Comece a verificar itens para liberar os relatórios de exportação.")
        return

    col_exp1, col_exp2 = st.columns(2)
    
    # Export 1: Ajustes
    with col_exp1:
        with st.container(border=True):
            st.markdown("##### ⚠️ Lista de Ajustes")
            st.caption(f"Itens ativos encontrados: **{count_adjustment}**")
            
            if count_adjustment > 0:
                df_adj = pd.DataFrame(items_adjustment)
                excel_adj = export_adjustment_list(df_adj)
                st.download_button(
                    label="Baixar Planilha de Ajustes (.xlsx)",
                    data=excel_adj,
                    file_name="ajustar_lansweeper.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="btn_rep_adj",
                    use_container_width=True,
                    type="primary"
                )
            else:
                st.success("Nada para ajustar!")

    # Export 2: Histórico Completo
    with col_exp2:
        with st.container(border=True):
            st.markdown("##### 📋 Histórico Completo")
            st.caption(f"Total de registros: **{total_scanned}**")
            
            current_date = datetime.now().strftime("%d_%m_%Y")
            excel_hist = export_scanned_history(scanned_items)
            
            st.download_button(
                label="Baixar Relatório Completo (.xlsx)",
                data=excel_hist,
                file_name=f"verificacao_stock_{current_date}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn_rep_full",
                use_container_width=True
            )

