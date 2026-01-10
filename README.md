# 📦 Stock Check - Sistema de Controle de Estoque

Sistema de verificação física de equipamentos com integração ao **Lansweeper**.

## 📋 Descrição

O **Stock Check** é uma aplicação web desenvolvida em **Streamlit** que facilita a verificação física de notebooks e equipamentos em estoque, comparando os itens escaneados fisicamente com a base de dados exportada do Lansweeper.

### Funcionalidades Principais

- 📥 **Upload de base Lansweeper** - Importação de arquivo Excel com validação completa de estrutura e dados
- 📊 **Preview de Dados** - Visualização com estatísticas, gráficos de distribuição e primeiros registros
- 📷 **Leitura de códigos de barras** - Suporte a QR Code, Code 128 e entrada manual (input direto)
- 🔍 **Comparação em tempo real** - Verificação instantânea do serial vs base de dados
- ✅ **Validação automatizada** - Validação de estados, detecção de equipamentos ativos e verificação de colunas obrigatórias
- ⚠️ **Detecção de inconsistências** - Identifica equipamentos com estado "active" mostrando hostname e usuário
- 📈 **Relatórios completos** - Métricas de verificação, histórico de escaneamentos e estatísticas detalhadas
- 📤 **Exportação de relatórios** - Gera lista de itens que requerem ajuste manual no Lansweeper com timestamp

---

## 🎯 Estados Válidos

O sistema reconhece os seguintes estados de equipamentos:

| Estado | Descrição | Status |
|--------|-----------|--------|
| `stock` | Em estoque | ✅ OK |
| `broken` | Quebrado | ✅ OK |
| `stolen` | Roubado | ✅ OK |
| `in repair` | Em reparo | ✅ OK |
| `old` | Equipamento antigo | ✅ OK |
| `active` | Ativo (em uso) | ⚠️ Requer ajuste |

**Regra de negócio:** Equipamentos físicos em estoque **não devem** estar com estado "active".

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.9+
- pip

### Instalação

1. **Clone o repositório:**

```bash
git clone <repository-url>
cd stock_check
```

2. **Crie um ambiente virtual:**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**

**Windows:**
```powershell
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

4. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente (opcional):**

```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

---

## 💻 Executando a Aplicação

### Modo Desenvolvimento

```bash
streamlit run app/main.py
```

A aplicação estará disponível em: **http://localhost:8501**

### Modo Produção

Para deploy em produção, utilize o **Streamlit Cloud** ou outro serviço compatível.

---

## 🧪 Testes

### Executar todos os testes:

```bash
pytest
```

### Executar com cobertura:

```bash
pytest --cov=app --cov-report=html
```

O relatório de cobertura estará em `htmlcov/index.html`.

### Executar testes de um módulo específico:

```bash
pytest tests/unit/
pytest tests/integration/
```

---

## 📁 Estrutura do Projeto

```
stock_check/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Entry point Streamlit
│   ├── config.py                    # Configurações da aplicação
│   ├── components/                  # Componentes UI
│   │   ├── upload_component.py      # Upload e preview de Excel
│   │   ├── scanner_input.py         # Input de código de barras
│   │   ├── comparison_component.py  # Comparação e exibição de resultados
│   │   └── report_component.py      # Relatórios e métricas
│   ├── services/                    # Lógica de negócio
│   │   ├── excel_handler.py         # Importação/exportação Excel
│   │   ├── barcode_handler.py       # Processamento de códigos de barras
│   │   ├── validator.py             # Validação de estados e dados
│   │   ├── comparator.py            # Comparação serial x base
│   │   └── report_metrics.py        # Métricas e estatísticas
│   └── utils/                       # Utilitários
│       ├── constants.py             # Estados válidos, configs
│       └── helpers.py               # Funções auxiliares
├── tests/
│   ├── conftest.py                  # Fixtures pytest
│   ├── unit/                        # Testes unitários
│   │   ├── test_excel_handler.py
│   │   ├── test_validator.py
│   │   ├── test_comparator.py
│   │   └── test_report_metrics.py
│   ├── integration/                 # Testes de integração
│   └── fixtures/                    # Arquivos Excel de teste
├── docs/                            # Documentação do projeto
│   ├── backlog.md
│   ├── config.md
│   ├── historico.md
│   ├── aprendizado.md
│   └── persona.md
├── .env.example                     # Exemplo de variáveis de ambiente
├── .gitignore
├── requirements.txt                 # Dependências Python
└── README.md                        # Este arquivo
```

---

## 🔒 Segurança

### Boas Práticas Implementadas

- ✅ Validação de tamanho e tipo de arquivos Excel (máx: 10 MB)
- ✅ Sanitização de valores para prevenir formula injection
- ✅ Validação de inputs de usuário (seriais, estados)
- ✅ Variáveis sensíveis em `.env` (nunca no código)
- ✅ `.gitignore` configurado para não versionar credenciais

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
DEBUG=False
LOG_LEVEL=INFO
```

---

## 🛠️ Stack Tecnológico

- **Framework:** Streamlit 1.30+
- **Processamento de Dados:** Pandas, OpenPyXL
- **Leitura de Códigos:** OpenCV, PyZBar
- **Testes:** pytest, pytest-cov
- **Deploy:** Streamlit Cloud / Railway

---

## 📊 Status do Projeto

### Progresso Geral: **50% Concluído** (7/14 tarefas)

| Fase | Status |
|------|--------|
| ✅ **P1-001:** Decisão de Arquitetura | Concluída |
| ✅ **P1-002:** Estrutura Base | Concluída |
| ✅ **P1-003:** Módulo de Importação Excel | Concluída |
| ✅ **P1-004:** Interface de Upload e Preview | Concluída |
| ✅ **P1-005:** Integração com Scanner | Concluída |
| ✅ **P2-001:** Validação de Estados | Concluída |
| ✅ **P2-002:** Comparação Serial x Base | Concluída |
| 🚧 **P2-003:** Interface de Verificação em Tempo Real | Em desenvolvimento |
| 🚧 **P2-004:** Exportação para Excel | Planejada |
| 🟡 **P3:** Funcionalidades Avançadas | Pendente |

### Testes Implementados
- ✅ 15 testes unitários para `excel_handler.py` (100% passando)
- ✅ 7 testes unitários para `validator.py` (100% passando)
- ✅ 9 testes unitários para `comparator.py` (100% passando)
- ✅ 5 testes unitários para `report_metrics.py` (100% passando)
- **Total:** 36 testes unitários | **Taxa de sucesso:** 100%

---

## 📝 Documentação Adicional

- [Backlog de Tarefas](docs/backlog.md)
- [Histórico de Desenvolvimento](docs/historico.md)
- [Configurações do Projeto](docs/config.md)
- [Aprendizados e Boas Práticas](docs/aprendizado.md)
- [Persona do Desenvolvedor](docs/persona.md)

---

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
2. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
3. Push para a branch (`git push origin feature/nova-feature`)
4. Abra um Pull Request

---

## 📄 Licença

Este projeto é de uso interno.

---

## 👤 Autor

Desenvolvido com ❤️ para otimizar o controle de estoque físico.

**Versão:** 0.2.0  
**Última atualização:** 2026-01-10  
**Progresso:** 50% (7/14 tarefas concluídas)
