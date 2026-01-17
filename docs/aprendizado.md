# Aprendizados do Projeto - Stock Check

## Data: 16/01/2026

### Controle de Abas no Streamlit

**Lição:** `st.tabs()` não permite controle programático da aba ativa.

**Contexto:**
- Modal de "Serial Não Encontrado" fazia `st.rerun()` após ação do usuário
- Após rerun, aplicação voltava sempre para primeira aba (Upload)
- Usuário precisava clicar manualmente na aba Verificação

**Problema:**
```python
# st.tabs() não tem parâmetro para selecionar aba ativa
tab1, tab2, tab3 = st.tabs(["Upload", "Verificação", "Relatórios"])
# Não há como fazer: st.tabs(..., active_tab=1)
```

**Solução:**
Substituir `st.tabs()` por `st.radio()` horizontal com session_state:

```python
# Inicializar aba ativa
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📤 Upload"

# Flag para forçar aba específica
if st.session_state.get('force_verification_tab', False):
    st.session_state.active_tab = "🔍 Verificação"
    st.session_state.force_verification_tab = False

# Seletor de abas controlável
selected_tab = st.radio(
    "Navegação",
    ["📤 Upload", "🔍 Verificação", "📊 Relatórios", "📜 Histórico"],
    index=options.index(st.session_state.active_tab),
    horizontal=True,
    label_visibility="collapsed"
)

# Renderizar baseado na seleção
if selected_tab == "📤 Upload":
    render_upload()
elif selected_tab == "🔍 Verificação":
    render_verification()
```

**Benefícios:**
- ✅ Controle programático completo
- ✅ Visual praticamente idêntico a tabs
- ✅ Persistência entre reruns via session_state
- ✅ Permite forçar mudança de aba via código

**Aprendizado:**
- Para interfaces que requerem controle programático, usar `st.radio()` horizontal
- `st.tabs()` é bom para UI estática sem necessidade de controle
- Session_state é essencial para manter estado entre reruns

---

### Deploy e Cache no Streamlit Cloud

**Lição:** Streamlit Cloud pode manter cache mesmo após push correto.

**Problema Encontrado:**
- Código correto presente no GitHub (origin/main)
- Função `render_history_table()` existia no repositório
- Streamlit Cloud reportava `ImportError: cannot import render_history_table`
- Verificação manual: `git show origin/main:arquivo.py` confirmou presença da função

**Causa:**
- Cache agressivo do Streamlit Cloud
- Build anterior pode ser mantido mesmo com novo commit

**Solução:**
```bash
# Forçar redeploy com commit vazio
git commit --allow-empty -m "chore: force Streamlit Cloud redeploy"
git push origin main
```

**Verificação:**
```bash
# Sempre verificar código no remote antes de culpar cache
git show origin/main:app/components/comparison_component.py | grep "render_history_table"
```

**Aprendizado:**
1. Sempre verificar que código está realmente no remoto
2. Commit vazio é válido para forçar rebuild
3. Streamlit Cloud pode levar 2-3 minutos para detectar mudanças
4. No caso de ImportError inesperado, verificar logs do Streamlit Cloud

---

## Data: 12/01/2026

### Filtros de Dados com Pandas

**Lição:** Filtros restritivos demais podem eliminar dados válidos inesperadamente.

**Contexto:**
- Filtro de notebooks estava eliminando 93% dos registros (932 → 62)
- Problema: campos vazios/null eram tratados como inválidos

**Solução:**
```python
# RUIM: Exclui registros com campo vazio
filter = df['Model'].str.contains('pattern')

# BOM: Inclui registros com padrão OU campo vazio
has_value = df['Model'].notna() & (df['Model'] != '')
has_pattern = df['Model'].str.contains('pattern')
filter_inclusive = has_pattern | ~has_value  # OR logic
```

**Aprendizado:**
- Sempre considerar valores NULL/vazios em filtros
- Usar lógica OR quando apropriado (inclusão ao invés de exclusão)
- Adicionar logging detalhado em cada etapa do filtro
- Testar com dados reais o mais cedo possível

---

### Debug de Filtros Multicritério

**Técnica Eficaz:** Logging progressivo mostrando quantos registros passam em cada etapa.

**Implementação:**
```python
total = len(df)
print(f"📊 Total original: {total}")

# Filtro 1
after_filter1 = filter1.sum()
print(f"📊 Após filtro 1: {total} → {after_filter1}")

# Filtro 2
after_filter2 = (filter1 & filter2).sum()
print(f"📊 Após filtro 2: {after_filter1} → {after_filter2}")

# Final
final = df[filter1 & filter2 & filter3]
print(f"✅ Resultado final: {len(final)} registros")
```

**Benefícios:**
- Identifica rapidamente qual filtro está causando problema
- Visível no terminal durante execução
- Ajuda usuário a entender o que está acontecendo

---

### Tabelas Pivotadas com Pandas

**Uso:** `pd.crosstab()` é perfeito para análises de inventário.

**Exemplo:**
```python
# Criar tabela Model x State
pivot = pd.crosstab(
    df['Model'],      # Linhas
    df['State'],      # Colunas
    margins=True,     # Adiciona linha/coluna TOTAL
    margins_name='TOTAL'
)

# Reordenar colunas em ordem lógica
desired_order = ['stock', 'active', 'broken', ...]
pivot = pivot[desired_order]
```

**Vantagens:**
- Visualização clara de distribuição
- Fácil de exportar para Excel/PDF
- Linha TOTAL automática
- Integrável com gráficos Streamlit

---

# Aprendizados do Projeto Stock Check

## Formatação de Números no Excel com openpyxl (12/01/2026)

### Problema
Ao exportar DataFrames para Excel, colunas numéricas (especialmente "Ativo"/patrimônio) exibiam com decimais desnecessários (1234.0 ao invés de 1234), mesmo após conversão para int no Python.

### Causa Raiz
- Python/pandas pode converter para int corretamente
- Mas ao exportar para Excel, o formato da célula permanece como "Number" com casas decimais
- Excel exibe baseado no formato da célula, não no tipo do valor

### Solução
Usar openpyxl para formatar células após exportação:

```python
from openpyxl import load_workbook

# 1. Exportar normalmente
df.to_excel(output, index=False, engine='openpyxl')

# 2. Reabrir com openpyxl
output.seek(0)
wb = load_workbook(output)
ws = wb.active

# 3. Formatar células específicas
for row in range(2, ws.max_row + 1):
    cell = ws.cell(row=row, column=ativo_col_idx)
    cell.number_format = '0'  # Formato inteiro, sem decimais

# 4. Salvar novamente
wb.save(output)
```

### Alternativas Consideradas
1. ❌ `df['col'].astype(int)` - Não afeta formato Excel
2. ❌ `df['col'].apply(str)` - Perde tipo numérico
3. ✅ `cell.number_format = '0'` - Preserva número mas sem decimais

### Lições Aprendidas
1. **Separar conversão de dados de formatação visual**
   - Python cuida dos dados (int, float, str)
   - Excel/openpyxl cuida da apresentação (number_format)

2. **Formatos Excel comuns:**
   - `'0'` = inteiro sem decimais
   - `'0.00'` = duas casas decimais
   - `'#,##0'` = inteiro com separador de milhares
   - `'@'` = texto

3. **Fluxo correto:**
   - Converter dados no DataFrame primeiro
   - Exportar para Excel
   - Reabrir com openpyxl
   - Aplicar formatação de células
   - Salvar novamente

4. **Performance:** Aceitável para arquivos até ~10k linhas

---

## Normalização de Estados PT-BR / EN (10/01/2026)

### Problema
Ao processar Excel com estados em português ("Reservado", "Ativo"), o sistema não reconhecia corretamente causando exibição de "❓ Estado desconhecido".

### Solução
Criar dicionário de normalização e função que converte PT-BR → EN antes de buscar no mapeamento de estados:

```python
STATE_NORMALIZATION = {
    'reservado': 'reserved',
    'ativo': 'active',
    # ... + inglês para idempotência
}

def normalize_state(state: str) -> str:
    state_lower = state.lower().strip()
    return STATE_NORMALIZATION.get(state_lower, 'unknown')
```

### Lições Aprendidas
1. **Sempre considerar múltiplos idiomas** ao processar inputs de usuário
2. **Normalização deve ser idempotente** (EN → EN deve funcionar também)
3. **Case-insensitive é essencial** para dados vindos de Excel
4. **Trim de espaços** previne bugs sutis
5. **Testes devem cobrir PT-BR e EN** para garantir suporte completo

---
