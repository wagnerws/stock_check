# Backlog - Sistema de Controle de Estoque

## 🔴 Prioridade 1 (P1) - Crítico

### P1-001: Decisão de Arquitetura e Stack Tecnológico
**Status:** ✅ Concluída  
**Data:** 08/01/2026  
**Decisão:** **Streamlit (Python)**  
**Complexidade:** Baixa  
**Descrição:** Definir se o projeto será desenvolvido com Streamlit (Python puro) ou React+Vite (fullstack). Considerar:
- Facilidade de deploy (Streamlit Cloud vs Vercel)
- Experiência de usuário desejada
- Integração com leitor de código de barras
- Manutenibilidade futura

---

### P1-002: Estrutura Base do Projeto
**Status:** ✅ Concluída  
**Data Conclusão:** 08/01/2026
**Dependências:** P1-001  
**Complexidade:** Baixa  
**Descrição:** Criar estrutura de diretórios, configuração de ambiente, e arquivos base (README, .gitignore, requirements.txt ou package.json)

**Resultados:**
- ✅ 7 diretórios criados (app/, tests/, components/, services/, utils/, unit/, integration/, fixtures/)
- ✅ 23 arquivos criados (config, constants, helpers, placeholders, conftest, README)
- ✅ Estrutura completa e validada

---

### P1-003: Módulo de Importação Excel
**Status:** ✅ Concluída  
**Data Conclusão:** 08/01/2026 23:30 BRT  
**Dependências:** P1-002  
**Complexidade:** Média  
**Descrição:** 
- Implementar leitura de arquivo Excel do Lansweeper
- Validar estrutura do arquivo
- Identificar automaticamente colunas "Serialnumber", "State", "Name" e "lastuser"
- Tratar erros comuns (arquivo inválido, colunas faltando)

**Resultados:**
- ✅ Funções implementadas: `import_excel()`, `validate_excel_structure()`, `export_excel()`, `export_adjustment_list()`
- ✅ 15 testes unitários (100% passando)
- ✅ Sanitização de fórmulas para segurança
- ✅ Validação completa de estrutura

---

### P1-004: Interface de Upload e Preview
**Status:** ✅ Concluída  
**Data Conclusão:** 08/01/2026 23:40 BRT  
**Dependências:** P1-003  
**Complexidade:** Média  
**Descrição:**
- Criar interface para upload do arquivo Excel
- Exibir preview dos dados carregados
- Permitir confirmação/ajuste das colunas identificadas
- Feedback visual de sucesso/erro

**Resultados:**
- ✅ Componente completo `upload_component.py`
- ✅ Upload com drag & drop
- ✅ Validação de tamanho e formato
- ✅ Preview com estatísticas e gráficos
- ✅ Session state para persistência
- ✅ Interface integrada em sistema de tabs

---

### P1-005: Integração com Leitor de Código de Barras
**Status:** ✅ Concluída  
**Data Conclusão:** 09/01/2026 12:45 BRT  
**Dependências:** P1-002  
**Complexidade:** Média  
**Descrição:**
- Implementar captura de código de barras via leitor USB (Zebra DS22)
- Componente de input otimizado com fluxo de "Enter" automático
- Validação de duplicidade na sessão (toast warning)
- Histórico visual de itens bipados
- Fallback para input manual (o mesmo campo atende ambos)

**Resultados:**
- ✅ `scanner_input.py` criado
- ✅ `barcode_handler.py` com validação de duplicidade
- ✅ Integração completa na aba Verificação
- ✅ Testado com fluxo de teclado/scanner USB

---

## 🟡 Prioridade 2 (P2) - Importante

### P2-001: Validação de Estados
**Status:** 🟡 Pendente  
**Dependências:** P1-003  
**Complexidade:** Baixa  
**Descrição:**
- Definir lista de estados válidos: stock, broken, stolen, in repair, old
- Implementar lógica de identificação de estados "ativo"
- Criar regras de negócio para classificação

---

### P2-002: Módulo de Comparação Serial x Base
**Status:** 🟡 Pendente  
**Dependências:** P1-003, P1-005  
**Complexidade:** Média  
**Descrição:**
- Comparar serial lido com base de dados carregada
- Verificar estado do item
- Indicar se requer ajuste (estado "ativo")
- Performance otimizada para busca rápida

---

### P2-003: Interface de Verificação em Tempo Real
**Status:** 🟡 Pendente  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Display de informações do item encontrado
- Indicadores visuais claros (✅ OK, ⚠️ Atenção, ❌ Não encontrado)
- Histórico dos últimos itens verificados
- Contador de progresso

---

### P2-004: Exportação para Excel
**Status:** 🟡 Pendente  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Gerar arquivo Excel com itens que estão como "ativo"
- Incluir colunas: Serialnumber, State atual, Data de verificação
- Download automático do arquivo
- Nomenclatura clara (ex: ajustes_lansweeper_YYYY-MM-DD.xlsx)

---

## 🟢 Prioridade 3 (P3) - Desejável

### P3-001: Relatórios e Estatísticas
**Status:** 🟡 Pendente  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Relatório de itens verificados vs não verificados
- Estatísticas por tipo de estado
- Gráficos de visualização (Streamlit/Recharts)
- Exportar relatório completo

---

### P3-002: Histórico de Verificações
**Status:** 🟡 Pendente  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Salvar histórico de verificações realizadas
- Consultar verificações anteriores
- Comparar múltiplas verificações ao longo do tempo

---

### P3-003: Modo Batch (Verificação em Lote)
**Status:** 🟡 Pendente  
**Dependências:** P2-002  
**Complexidade:** Alta  
**Descrição:**
- Permitir upload de lista de seriais para verificação automática
- Processamento em lote
- Relatório consolidado

---

### P3-004: Testes Automatizados Completos
**Status:** 🟡 Pendente  
**Dependências:** Todos os módulos principais  
**Complexidade:** Alta  
**Descrição:**
- Suite completa de testes unitários
- Testes de integração com arquivos Excel de exemplo
- Testes de performance
- Coverage > 80%

---

### P3-005: Dockerização
**Status:** 🟡 Pendente  
**Dependências:** P1-002  
**Complexidade:** Baixa  
**Descrição:**
- Criar Dockerfile
- Docker Compose para desenvolvimento local
- Facilitação de deploy

---

## 📊 Resumo de Prioridades

| Prioridade | Tarefas | Status |
|------------|---------|--------|
| P1 (Crítico) | 5 | ✅ 4/5 |
| P2 (Importante) | 4 | 🟡 0/4 |
| P3 (Desejável) | 5 | 🟡 0/5 |
| **TOTAL** | **14** | **4/14 (28.6%)** |

---

## 🎯 Próxima Tarefa Recomendada
**P1-005: Integração com Leitor de Código de Barras**

Implementar captura de código de barras (QR Code e Barcode) para leitura de números de série dos equipamentos, com fallback para input manual.
