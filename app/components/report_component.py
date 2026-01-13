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
    st.markdown("### 📊 Dashboard de Relatórios")
    
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
    
    # --- 2. Métricas de Progresso (Topo) ---
    st.markdown("#### 📈 Progresso Geral")
    
    # Barra de progresso visual
    st.progress(progress_pct, text=f"Progresso da Sessão: {progress_pct:.1%}")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total na Base", total_base)
    with m2:
        st.metric("Verificados", f"{total_scanned}", f"{progress_pct:.1%}")
    with m3:
        st.metric("Pendentes", pendentes, delta_color="off")
    with m4:
        st.metric("Requerem Ajuste", count_adjustment, delta_color="inverse")

    st.divider()

    # --- 3. Análise da Sessão (Gráficos) ---
    if total_scanned > 0:
        st.markdown("#### 🔎 Análise da Sessão")
        
        c_chart, c_stats = st.columns([2, 1])
        
        with c_chart:
            st.markdown("**Distribuição por Estado (Itens Verificados)**")
            
            # Preparar dados para o gráfico
            df_scanned = pd.DataFrame(scanned_items)
            
            if 'state' in df_scanned.columns:
                # Contagem por estado
                state_counts = df_scanned['state'].value_counts()
                st.bar_chart(state_counts, color="#0068c9")
            else:
                st.info("Sem dados de estado para exibir gráfico.")

        with c_stats:
            st.markdown("**Detalhamento**")
            # Tabela resumida de contagem
            if 'state' in df_scanned.columns:
                summary_df = df_scanned['state'].value_counts().reset_index()
                summary_df.columns = ['Estado', 'Qtd']
                
                # Adicionar emojis se possível
                summary_df['Estado'] = summary_df['Estado'].apply(
                    lambda x: f"{STATE_EMOJI.get(x.lower(), '❓')} {x}"
                )
                
                st.dataframe(
                    summary_df, 
                    use_container_width=True, 
                    hide_index=True
                )

        st.divider()
        
        # --- 3.5 Inventário por Modelo (NOVO) ---
        st.markdown("#### 📦 Inventário por Modelo de Equipamento")
        st.caption("Distribuição de estados por modelo de notebook")
        
        # Buscar dados da base completa com estados
        if 'Model' in df_base.columns and 'State' in df_base.columns:
            # Criar DataFrame com Model e State
            inventory_df = df_base[['Model', 'State']].copy()
            
            # Normalizar estados (minúsculas)
            inventory_df['State'] = inventory_df['State'].str.lower().str.strip()
            
            # Criar tabela pivotada: Model x State
            pivot_table = pd.crosstab(
                inventory_df['Model'], 
                inventory_df['State'],
                margins=True,
                margins_name='TOTAL'
            )
            
            # Reordenar colunas para ter os estados principais primeiro
            desired_order = ['stock', 'active', 'broken', 'stolen', 'in repair', 'old', 'reserved', 'sold']
            existing_cols = [col for col in desired_order if col in pivot_table.columns]
            other_cols = [col for col in pivot_table.columns if col not in existing_cols and col != 'TOTAL']
            final_cols = existing_cols + other_cols + (['TOTAL'] if 'TOTAL' in pivot_table.columns else [])
            pivot_table = pivot_table[final_cols]
            
            # Adicionar emojis aos nomes das colunas
            pivot_table.columns = [
                f"{STATE_EMOJI.get(col, '')} {col.upper()}" if col != 'TOTAL' else col 
                for col in pivot_table.columns
            ]
            
            # Exibir tabela
            st.dataframe(
                pivot_table,
                use_container_width=True,
                height=400
            )
            
            # Gráfico de barras empilhadas
            st.markdown("**Visualização Gráfica**")
            
            # Remover linha de total para o gráfico
            pivot_for_chart = pivot_table.drop('TOTAL', errors='ignore')
            
            # Limitar aos top 10 modelos (sem linha TOTAL)
            if len(pivot_for_chart) > 10:
                # Ordenar por total e pegar top 10
                top_10_models = pivot_for_chart.iloc[:, :-1].sum(axis=1).nlargest(10).index
                pivot_for_chart = pivot_for_chart.loc[top_10_models]
                st.caption("ℹ️ Mostrando top 10 modelos com mais equipamentos")
            
            st.bar_chart(pivot_for_chart, stack=False)
            
        else:
            st.info("ℹ️ Colunas 'Model' e 'State' não encontradas na base de dados.")
    
        st.divider()

    # --- 4. Área de Exportação (Mantida e Melhorada) ---
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
