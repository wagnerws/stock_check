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

**Status Atual:** P1-003 e P1-004 concluídas (4/5 tarefas P1), interface funcional testada

**Próximos Passos:**
1. Implementar P1-005: Integração com leitor de código de barras
   - Pesquisar bibliotecas (pyzbar, opencv)
   - Implementar captura em tempo real
   - Criar fallback para input manual

2. Iniciar P2-002: Módulo de Comparação Serial x Base
   - Implementar busca otimizada
   - Criar lógica de comparação
   - Flag para equipamentos ativos

3. Criar interface de verificação em tempo real (P2-003)

**Tarefas do Backlog em Foco:**
- ✅ **P1-001:** Decisão de Arquitetura - **CONCLUÍDA** (08/01/2026)
- ✅ **P1-002:** Estrutura Base do Projeto - **CONCLUÍDA** (08/01/2026 20:30)
- ✅ **P1-003:** Módulo de Importação Excel - **CONCLUÍDA** (08/01/2026 23:30)
- ✅ **P1-004:** Interface de Upload e Preview - **CONCLUÍDA** (08/01/2026 23:40)
- 🟡 **P1-005:** Integração com Leitor de Código de Barras - **PRÓXIMA**

---

## 📚 Lessons Learned

### Boas Práticas
- Usar `st.session_state` para manter dados entre interações
- Implementar cache com `@st.cache_data` para operações pesadas
- Validar arquivos antes de processar

### Anti-Padrões a Evitar
- ❌ Processar arquivos grandes sem progressbar
- ❌ Não validar colunas do Excel antes de uso
- ❌ Usar `st.write()` excessivamente (preferir componentes específicos)

---

**Última Atualização:** 2026-01-08 23:45 BRT
