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

**Status Atual:** 🎉 Versão 0.8.1 - Produção Atualizada e Refinada

**Última Sessão (16/01/2026 21:14 BRT):**
Sessão completa: melhorias massivas de UI, correções de filtros, reorganização de layout, remoção de código desnecessário e deploy.

**Estado da Aplicação:**
- ✅ Aplicação Streamlit rodando localmente (v0.8.1)
- ✅ **Ambas branches sincronizadas:**
  - Branch dev: 48b2d86 (atualizada no GitHub)
  - Branch main: eda4c31 (atualizada no GitHub + hotfix)
- ✅ Streamlit Cloud deploy concluído com sucesso
- ✅ **URL Produção:** https://check-stock.streamlit.app/

**Resumo da Sessão (16/01/2026):**

**1. Correções de Filtros:**
- ✅ OptiPlex incluído em `NOTEBOOK_MODEL_PATTERNS`
- ✅ "not scanned" adicionado a `VALID_OS_PATTERNS`
- ✅ Seriais OptiPlex 7040 agora são encontrados
- ✅ Equipamentos não escaneados incluídos

**2. Limpeza de Código:**
- ✅ Removida aba "Diagnóstico" completa
- ✅ Deletado `diagnostics_component.py`
- ✅ Removidos gráficos de inventário por modelo
- ✅ Limpado código de `filtered_out_records`

**3. Reorganização de Layout:**
- ✅ Aba Verificação reorganizada (Resultado → Scanner → Histórico → Métricas)
- ✅ Criada função `render_history_table()` separada
- ✅ Interface mais intuitiva e focada

**4. Correção Crítica de Navegação:**
- ✅ Substituído `st.tabs()` por `st.radio()` controlável
- ✅ Implementada flag `force_verification_tab`
- ✅ Usuário permanece na aba Verificação após modal

**5. Deploy:**
- ✅ Commit principal: `48b2d86`
- ✅ Merge dev → main: `b39be9f`
- ✅ Hotfix deploy: `eda4c31` (commit vazio para forçar rebuild)

**Commits Finais:**
- dev: `48b2d86` - "feat: major UI improvements and filter fixes"
- main: `eda4c31` - "chore: force Streamlit Cloud redeploy"

**Arquivos Modificados (sessão completa):**
- Código: 8 arquivos (constants, excel_handler, report, comparison, scanner, main)
- Deletados: 1 arquivo (diagnostics_component.py)
- Documentação: historico.md, aprendizado.md, config.md

**Próximos Passos:**
1. Validar filtros em produção com dados reais
2. Testar com leitor Zebra DS22
3. Coletar feedback dos usuários finais
4. Futuro: Implementar P3-007 (SharePoint) ou P3-009 (Persistência)

**Backlog Atualizado:**
- ✅ **P1 (Crítico):** 5/5 (100%)
- ✅ **P2 (Importante):** 4/4 (100%)
- 🟡 **P3 (Desejável):** 3/8 (37.5%)
  - P3-009: Em standby (persistência base)
  - P3-007: Aguardando Azure AD (SharePoint)

**Versão em Produção:** v0.8.1 (main)
**Versão em Desenvolvimento:** v0.8.1 (dev)
**URL Produção:** https://check-stock.streamlit.app/

---

**Última Atualização:** 2026-01-16 21:14 BRT

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
