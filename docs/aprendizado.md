# Aprendizadose Lições - Stock Check

## UI/UX Simplificada
- **Menos é Mais**: Em aplicações operacionais (uso com scanner), cada pixel de tela conta. Títulos grandes e gráficos decorativos podem atrapalhar a visualização rápida do status.
- **Feedback Visual**: Ocultar labels de widgets nativos do Streamlit via CSS (`display: none`) é uma técnica útil para criar layouts customizados tipo "cards".

## Regras de Negócio (Conciliação)
- **Métricas Claras**: Quando se filtra uma base para validar estoque (ex: apenas itens 'Stock'), é crucial mostrar para o usuário o que conteceu com os itens 'Fora do Escopo' (ex: Reservados) que ele bipou. Sem isso ("Outros Bipados"), o usuário acha que o sistema ignorou a leitura.
- **Segregação de Estados**: Itens como 'Reservado' ou 'Vendido' existem fisicamente mas não contam como 'Estoque Disponível' para fins de auditoria de falta.

## Streamlit Tricks
- **Controle de Abas**: Usar `st.radio` na sidebar funcionou melhor que `st.tabs` nativo para navegação principal, liberando espaço vertical.
- **CSS Injection**: Essencial para remover margens padrão excessivas do Streamlit.
