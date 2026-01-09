# Aprendizados - Stock Check

## 📚 Lições Aprendidas

### Data: 08/01/2026

#### 🎯 Decisão de Stack Tecnológico

**Contexto:**  
Decisão entre Streamlit (Python) vs React+Vite (Fullstack) para aplicação de controle de estoque.

**Aprendizado:**  
Para ferramentas internas com foco em **funcionalidade > estética**, Streamlit é superior devido a:
- ⚡ Velocidade de desenvolvimento (3-5x mais rápido)
- 🚀 Deploy simplificado (Streamlit Cloud gratuito)
- 📊 Integração nativa com pandas/Excel
- 🔧 Manutenção mais fácil (um único idioma: Python)

**Aplicação Futura:**  
Avaliar se a aplicação é **interna** (Streamlit) ou **externa/customer-facing** (React) antes de escolher stack.

---

#### 🔒 Segurança em Upload de Arquivos

**Problema Identificado:**  
Uploads de arquivos Excel podem ser vetores de ataque (macros maliciosas, tamanho excessivo, tipos incorretos).

**Solução:**
```python
import streamlit as st
import magic  # python-magic para validar MIME type real

def validate_uploaded_file(uploaded_file):
    # Validar tamanho
    MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    if uploaded_file.size > MAX_SIZE:
        st.error("Arquivo muito grande (máx: 10 MB)")
        return False
    
    # Validar extensão
    if not uploaded_file.name.endswith(('.xlsx', '.xls')):
        st.error("Formato inválido. Use .xlsx ou .xls")
        return False
    
    # Validar MIME type real (não confiar apenas na extensão)
    file_type = magic.from_buffer(uploaded_file.read(2048), mime=True)
    uploaded_file.seek(0)  # Reset file pointer
    
    if file_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          'application/vnd.ms-excel']:
        st.error("Tipo de arquivo suspeito detectado")
        return False
    
    return True
```

**Lição:**  
Sempre validar:
1. **Tamanho** do arquivo
2. **Extensão** do arquivo
3. **MIME type real** (não confiar apenas no nome)

---

#### 📊 Performance em Streamlit

**Problema:**  
Streamlit reexecuta todo o script a cada interação, causando lentidão com operações pesadas.

**Solução:**  
Usar decoradores de cache estrategicamente:

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_excel_data(file_path):
    """Cache de dados carregados do Excel"""
    return pd.read_excel(file_path)

@st.cache_resource
def initialize_barcode_scanner():
    """Cache de recursos que não mudam (conexões, modelos, etc.)"""
    return BarcodeScanner()
```

**Diferença:**
- `@st.cache_data`: Para dados (DataFrames, listas, dicionários)
- `@st.cache_resource`: Para objetos não-serializáveis (conexões, modelos ML)

**Lição:**  
Cachear **tudo** que não muda entre interações para melhor performance.

---

## 🚫 Anti-Padrões Identificados

### 1. ❌ Processar Arquivos Grandes Sem Feedback Visual

**Problema:**
```python
# Ruim: usuário não sabe se travou
df = pd.read_excel(uploaded_file)
processed_df = process_data(df)
```

**Solução:**
```python
# Bom: feedback visual com progressbar
with st.spinner("Carregando arquivo Excel..."):
    df = pd.read_excel(uploaded_file)

with st.progress(0) as progress_bar:
    total_rows = len(df)
    for idx, row in df.iterrows():
        process_row(row)
        progress_bar.progress((idx + 1) / total_rows)
```

---

### 2. ❌ Não Usar `st.session_state` para Dados Persistentes

**Problema:**
```python
# Ruim: dados perdidos a cada interação
uploaded_file = st.file_uploader("Upload Excel")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # df será recarregado a CADA clique em qualquer botão
```

**Solução:**
```python
# Bom: manter dados em session_state
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None

uploaded_file = st.file_uploader("Upload Excel")
if uploaded_file and st.session_state.dataframe is None:
    st.session_state.dataframe = pd.read_excel(uploaded_file)
    
# Usar st.session_state.dataframe em vez de recarregar
```

---

### 3. ❌ Injeção de Fórmulas em Excel Exportado

**Problema:**
Se um usuário malicioso inserir `=CMD|'/c calc'!A1` como serial, ao abrir o Excel exportado, pode executar comandos.

**Solução:**
```python
def sanitize_value(value):
    """Remove caracteres perigosos para prevenir formula injection"""
    if isinstance(value, str) and value.startswith(('=', '+', '-', '@')):
        return "'" + value  # Força como texto com aspas simples
    return value

# Aplicar antes de exportar
df_export = df.applymap(sanitize_value)
df_export.to_excel('output.xlsx', index=False)
```

---

## ✅ Boas Práticas Confirmadas

### 1. Estrutura de Projeto por Camadas

```
app/
├── components/   # UI (Streamlit components)
├── services/     # Business logic
└── utils/        # Helpers e constantes
```

**Benefício:**  
Separação clara de responsabilidades = código mais testável e manutenível.

---

### 2. Validação Rigorosa de Inputs

```python
def validate_serial_number(serial: str) -> tuple[bool, str]:
    """Valida serial e retorna (is_valid, error_message)"""
    if not serial:
        return False, "Serial não pode estar vazio"
    
    if len(serial) < 5:
        return False, "Serial deve ter no mínimo 5 caracteres"
    
    if not serial.isalnum():
        return False, "Serial deve conter apenas letras e números"
    
    return True, ""

# Uso
is_valid, error = validate_serial_number(user_input)
if not is_valid:
    st.error(error)
```

---

### 3. Configurações Centralizadas

**Arquivo:** `app/utils/constants.py`
```python
# Estados válidos
VALID_STATES = ['stock', 'broken', 'stolen', 'in repair', 'old', 'active']

# Configurações de validação
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['.xlsx', '.xls']

# Colunas obrigatórias no Excel
REQUIRED_COLUMNS = ['Serialnumber', 'State']

# Emoji para estados
STATE_EMOJI = {
    'stock': '✅',
    'broken': '🔧',
    'stolen': '🚨',
    'in repair': '⚙️',
    'old': '📦',
    'active': '⚠️'
}
```

**Benefício:**  
Fácil manutenção, sem magic numbers espalhados no código.

---

## 🔧 Ferramentas Úteis

### Para Desenvolvimento Streamlit
- **streamlit-aggrid**: Tabelas interativas avançadas
- **streamlit-extras**: Componentes adicionais úteis
- **pandas-profiling**: Análise rápida de DataFrames

### Para Testes
- **pytest-streamlit**: Testar aplicações Streamlit
- **faker**: Gerar dados de teste

### Para Deploy
- **Streamlit Cloud**: Deploy gratuito direto do GitHub
- **Railway/Render**: Alternativas com mais controle

---

## 📝 Checklist de Qualidade

Antes de considerar uma feature "completa":

- [ ] Código tem type hints (`def func(x: int) -> str:`)
- [ ] Inputs são validados
- [ ] Erros têm mensagens claras em PT-BR
- [ ] Há feedback visual (spinner, progressbar)
- [ ] Dados críticos estão em `st.session_state`
- [ ] Operações pesadas estão cacheadas
- [ ] Há testes unitários (pytest)
- [ ] Não há secrets no código
- [ ] Performance testada com arquivo grande (~1000 linhas)

---

#### 🎨 Exibição Condicional de Informações (08/01/2026)

**Contexto:**  
Necessidade de exibir informações adicionais (hostname e usuário) apenas para equipamentos com estado "active".

**Aprendizado:**  
Implementar exibição condicional baseada em estado do equipamento:

```python
def compare_and_flag(serial: str, database: pd.DataFrame) -> Dict[str, Any]:
    equipment = find_equipment(serial, database)
    
    result = {
        'found': True,
        'serialnumber': equipment['serialnumber'],
        'state': state,
        'requires_adjustment': requires_adjustment,
        # ... outros campos
    }
    
    # Add Name and lastuser ONLY for active equipment
    if requires_adjustment:
        result['name'] = equipment['name']
        result['lastuser'] = equipment['lastuser']
    
    return result
```

**Benefícios:**
- ✅ Evita poluição visual com informações irrelevantes
- ✅ Destaca dados críticos quando necessário
- ✅ Melhora UX com informações contextuais

**Aplicação Futura:**  
Sempre considerar exibição condicional de dados baseada em **contexto** e **estado** para melhor UX.

---

**Última Atualização:** 2026-01-08 20:46 BRT

#### 📷 Integração com Scanner USB (09/01/2026)

**Contexto:**
Integração de leitores de código de barras físicos (como Zebra DS22) em aplicações Web/Streamlit.

**Aprendizado:**
Leitores USB geralmente comportam-se como teclados (HID). Ao ler um código, eles enviam a string seguida de um `ENTER`.
- **Não é necessário** usar bibliotecas complexas de câmera (OpenCV/PyZbar) se o hardware for dedicado.
- O campo `st.text_input` do Streamlit captura o `ENTER` automaticamente e dispara o `on_change` ou reload.
- **UX:** É vital instruir o usuário a manter o foco no campo de input.
- **Validação de Duplicidade:** Como a leitura é muito rápida, é comum bipar o mesmo item 2x sem querer. Implementar verificação na sessão (`if serial in st.session_state.scanned_items`) é essencial para evitar registros sujos.

**Solução Adotada:**
```python
# Componente simples
st.text_input(..., on_change=process_scan_callback)

# Callback
def process_scan_callback():
    serial = st.session_state.input_val
    if serial in st.session_state.history:
        st.toast("Já verificado!", icon="⚠️")
        return
    # ... processa
```

---
