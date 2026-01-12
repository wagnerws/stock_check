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
