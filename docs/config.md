# Configuração do Projeto - Stock Check

## 📊 Informações do Projeto

**Nome:** Stock Check  
**Descrição:** Sistema de controle de estoque físico com integração Lansweeper  
**Repositório:** `stock_check`  
**Branch Ativa:** `dev`  
**Data de Início:** 08/01/2026  

---

## 🎯 Stack Tecnológico

### ✅ Decisão Final: **Streamlit (Python)**

**Justificativa:**
- Deploy simplificado (Streamlit Cloud gratuito)
- Desenvolvimento rápido de protótipo funcional
- Ideal para ferramentas internas de estoque
- Integração nativa com pandas para manipulação de Excel
- Comunidade ativa e documentação excelente

**Tecnologias:**
- **Framework:** Streamlit 1.30+
- **Processamento de Dados:** Pandas, OpenPyXL
- **Leitura de Códigos:** OpenCV/ZBar (para QR Code)
- **Testes:** pytest
- **Deploy:** Streamlit Cloud ou Railway

---

## 📁 Estrutura do Projeto

```
stock_check/
├── app/
│   ├── main.py                  # Entry point Streamlit
│   ├── components/              # Componentes UI
│   │   ├── __init__.py
│   │   ├── upload_component.py
│   │   ├── scanner_component.py
│   │   └── comparison_component.py
│   ├── services/                # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── excel_handler.py     # Import/export Excel
│   │   ├── validator.py         # Validação de estados
│   │   └── comparator.py        # Comparação serial x base
│   ├── utils/                   # Utilitários
│   │   ├── __init__.py
│   │   ├── constants.py         # Estados válidos, configs
│   │   └── helpers.py           # Funções auxiliares
│   └── config.py                # Configurações da aplicação
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/                # Arquivos Excel de teste
├── docs/
│   ├── persona.md
│   ├── backlog.md
│   ├── historico.md
│   ├── config.md                # Este arquivo
│   └── aprendizado.md
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── Dockerfile                   # Opcional (P3)
```

---

## 🔒 Security & OpSec

### Secrets Management
- **NUNCA** commitar credenciais no código
- Usar `.env` para variáveis sensíveis (se houver API keys futuras)
- `.env` deve estar no `.gitignore`
- Fornecido `.env.example` com placeholders

### Validação de Arquivos Excel
```python
# Tamanho máximo: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Extensões permitidas
ALLOWED_EXTENSIONS = ['.xlsx', '.xls']

# Validar mime type real do arquivo
```

### Input Sanitization
- Validar serial numbers (formato esperado)
- Prevenir injeção de fórmulas em Excel exportado
- Escapar caracteres especiais em displays

---

## 🎨 Estados Válidos de Equipamentos

```python
VALID_STATES = {
    'stock': '✅ Em estoque - OK',
    'broken': '🔧 Quebrado - OK',
    'stolen': '🚨 Roubado - OK',
    'in repair': '⚙️ Em reparo - OK',
    'old': '📦 Equipamento antigo - OK',
    'active': '⚠️ ATIVO - Requer ajuste no Lansweeper'
}
```

---

## 📝 Convenções de Código

### Nomenclatura
- **Arquivos:** snake_case (`excel_handler.py`)
- **Classes:** PascalCase (`ExcelHandler`)
- **Funções/Variáveis:** snake_case (`validate_serial_number`)
- **Constantes:** UPPER_SNAKE_CASE (`MAX_FILE_SIZE`)

### Comentários
- **Código:** Inglês
- **Strings/Mensagens ao usuário:** Português (PT-BR)
- **Documentação:** Português (PT-BR)

### Exemplo
```python
def validate_serial_number(serial: str) -> bool:
    """
    Valida o formato do número de série.
    
    Args:
        serial: Número de série a ser validado
        
    Returns:
        True se válido, False caso contrário
    """
    if not serial or len(serial) < 5:
        st.error("Número de série inválido")  # PT-BR
        return False
    
    return True
```

---

## 🚀 Workflow de Desenvolvimento

### 1. Desenvolvimento
- Trabalhar na branch `dev`
- Commits descritivos em PT-BR ou EN
- Testar localmente com `streamlit run app/main.py`

### 2. Testes
- Executar `pytest` antes de commit
- Validar com arquivo Excel de exemplo

### 3. Deploy (Futuro)
- Push para `main` após aprovação
- Deploy automático no Streamlit Cloud

---

## 🔄 Resume Point

**Status Atual:** 🎉 Versão 0.3.1 - Pronto para Uso em Produção

**Última Sessão (10/01/2026 12:23):**
Sessão de manutenção com execução do comando "save" para fechamento de sessão.

**Estado da Aplicação:**
- ✅ Aplicação Streamlit rodando localmente na porta 8501
- ✅ Versão 0.3.1 estável e funcional
- ✅ Todas as funcionalidades core implementadas e testadas
- ✅ Deploy sincronizado (branches dev e main atualizadas)

**Últimas Implementações (Sessão Anterior - 10/01/2026 12:07):**

**1. Normalização de Estados PT-BR → EN:**
- ✅ Mapeamento `STATE_NORMALIZATION` criado
- ✅ Função `normalize_state()` implementada
- ✅ Suporte completo para Excel em português e inglês
- ✅ 6 testes passando

**2. Registro por Patrimônio:**
- ✅ Busca numérica corrigida (int comparison)
- ✅ Formatação sem casas decimais (9856, não 9856.0)
- ✅ Verificação de duplicidade usando serialnumber correto
- ✅ 5 testes novos, 12 testes total passando

**Próximos Passos Recomendados:**
1. **Validação em Produção** - Testar com leitor Zebra DS22 e Excel real do Lansweeper
2. **P3-002: Histórico de Verificações** - Implementar persistência de dados entre sessões
3. **P3-003: Modo Batch** - Implementar upload de lista de serials para verificação automática

**Tarefas do Backlog:**
- ✅ **P1 (Crítico):** 5/5 tarefas concluídas (100%)
- ✅ **P2 (Importante):** 4/4 tarefas concluídas (100%)
- ✅ **P3 (Desejável):** 1/5 tarefas concluídas (20%)
- 🟡 **Próxima Tarefa Sugerida:** P3-002 (Histórico de Verificações)


---

## 📚 Lessons Learned

### Boas Práticas
- Usar `st.session_state` para manter dados entre interações
- Implementar cache com `@st.cache_data` para operações pesadas
- Validar arquivos antes de processar
- Usar `@st.dialog` para modais de confirmação
- Configurar timezone explícito para timestamps críticos

### Anti-Padrões a Evitar
- ❌ Processar arquivos grandes sem progressbar
- ❌ Não validar colunas do Excel antes de uso
- ❌ Usar `st.write()` excessivamente (preferir componentes específicos)
- ❌ Confiar no timezone do servidor (sempre usar timezone explícito)

---

## 🔄 Resume Point

**Status Atual:** 🎉 Versão 0.8.0 - Inventário por Modelo Implementado

**Última Sessão (12/01/2026 19:49 BRT):**
Sessão de correção de filtros e implementação de novas funcionalidades.

**Estado da Aplicação:**
- ✅ Aplicação Streamlit rodando localmente
- ✅ Versão 0.8.0 estável e funcional
- ✅ Filtros de notebooks corrigidos
- ✅ Novo relatório de inventário por modelo implementado

**Resumo da Sessão (12/01/2026):**

**1. Correção do Filtro de Notebooks (v0.7.0 → v0.7.1):**
- ✅ **Problema identificado:** Filtro muito restritivo excluía registros com Model vazio (932 → 62 notebooks)
- ✅ **Solução v0.7.0:** Lógica mais inclusiva (Model vazio agora é incluído)
- ✅ **Solução v0.7.1:** 
  - Padrões de OS expandidos (microsoft, win 10, win 11, etc)
  - Filtro adicional por coluna Type (notebook|laptop|portable)
  - Lógica OR: passa se (OS válido OU Type válido)
- ✅ Debug logging detalhado em cada etapa do filtro

**2. Adição de Estado 'Sold' (v0.7.2):**
- ✅ Estado "sold" (vendido) 💰 adicionado
- ✅ Tratado como OK (não requer ajuste)
- ✅ Mapeamento PT-BR: "vendido" → "sold"
- ✅ Interface atualizada

**3. Inventário por Modelo (v0.8.0):**
- ✅ Nova seção na aba Relatórios
- ✅ Tabela pivotada: Model x Estado
- ✅ Mostra quantidade de cada modelo em cada estado (stock, broken, stolen, etc)
- ✅ Gráfico de barras com top 10 modelos
- ✅ Linha TOTAL para agregação

**Arquivos Modificados:**
- `app/services/excel_handler.py` - Filtros corrigidos e melhorados
- `app/utils/constants.py` - Padrões OS expandidos + estado sold
- `app/components/upload_component.py` - Mensagens informativas
- `app/components/report_component.py` - Inventário por modelo
- `app/services/comparator.py` - Suporte a sold
- `app/main.py` - Versões atualizadas (0.7.0 → 0.8.0)
- `docs/historico.md` - Documentação completa

**Próximos Passos Recomendados:**
1. **Validar filtros** - Fazer upload da base e confirmar que todos os notebooks aparecem
2. **Testar inventário** - Verificar visualização na aba Relatórios
3. **Deploy** - Quando pronto, fazer commit e push para produção

**Tarefas do Backlog:**
- ✅ **P1 (Crítico):** 5/5 tarefas concluídas (100%)
- ✅ **P2 (Importante):** 4/4 tarefas concluídas (100%)
- ✅ **P3 (Desejável):** 3/7 tarefas concluídas (42.8%)
- 🟡 **Próxima Tarefa Sugerida:** P3-007 (SharePoint Integration)

**Versão em Desenvolvimento:** v0.8.0
**Versão em Produção:** v0.6.3

---

## 📚 Lessons Learned

### Boas Práticas
- Usar `st.session_state` para manter dados entre interações
- Implementar cache com `@st.cache_data` para operações pesadas
- Validar arquivos antes de processar
- Usar `@st.dialog` para modais de confirmação
- Configurar timezone explícito para timestamps críticos
- **Formatar células Excel com openpyxl após exportação**
- **Converter dados numéricos na importação do DataFrame**

### Anti-Padrões a Evitar
- ❌ Processar arquivos grandes sem progressbar
- ❌ Não validar colunas do Excel antes de uso
- ❌ Usar `st.write()` excessivamente (preferir componentes específicos)
- ❌ Confiar no timezone do servidor (sempre usar timezone explícito)
- ❌ **Confiar apenas em conversão Python para formatar Excel**
- ❌ **Esquecer que Excel tem formatação própria de células**

---

**Última Atualização:** 2026-01-12 16:37 BRT
