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
**Status:** ✅ Concluída
**Data Conclusão:** 09/01/2026
**Dependências:** P1-003
**Complexidade:** Baixa
**Descrição:**
- Definir lista de estados válidos: stock, broken, stolen, in repair, old
- Implementar lógica de identificação de estados "ativo"
- Criar regras de negócio para classificação

**Resultados:**
- ✅ `app/services/validator.py` implementado
- ✅ Testes unitários 100% passing (`tests/unit/test_validator.py`)
- ✅ Validação centralizada via constantes

---

### P2-002: Módulo de Comparação Serial x Base
**Status:** ✅ Concluída  
**Data Conclusão:** 09/01/2026  
**Dependências:** P1-003, P1-005  
**Complexidade:** Média  
**Descrição:**
- Comparar serial lido com base de dados carregada
- Verificar estado do item
- Indicar se requer ajuste (estado "ativo")
- Performance otimizada para busca rápida

---

### P2-003: Interface de Verificação em Tempo Real
**Status:** ✅ Concluída  
**Data Conclusão:** 09/01/2026  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Display de métricas de sessão (Total, OK, Ajuste)
- Indicadores visuais aprimorados (Cards coloridos)
- Histórico simplificado
- Layout otimizado para operação em lote

---

### P2-004: Exportação para Excel
**Status:** ✅ Concluída  
**Data Conclusão:** 09/01/2026  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Gerar arquivo Excel com itens que estão como "ativo"
- Incluir colunas: Serialnumber, State atual, Data de verificação
- Download automático do arquivo
- Nomenclatura: `ajustar_lansweeper.xlsx` e `verificacao_stock_{data}.xlsx`

---

## 🟢 Prioridade 3 (P3) - Desejável

### P3-001: Relatórios e Estatísticas
**Status:** ✅ Concluída  
**Data Conclusão:** 09/01/2026  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Relatório de itens verificados vs não verificados
- Estatísticas por tipo de estado
- Gráficos de visualização (Streamlit/Recharts)
- Exportar relatório completo

**Resultados:**
- ✅ Dashboard completo com barra de progresso
- ✅ Métricas de topo (Total, Verificados, Pendentes, Ajustes)
- ✅ Gráfico de barras com distribuição de estados
- ✅ Tabelas resumidas
- ✅ Testes unitários de lógica (100% pass)


---

### P3-002: Histórico de Verificações
**Status:** ✅ Concluída  
**Data Conclusão:** 10/01/2026  
**Dependências:** P2-002  
**Complexidade:** Média  
**Descrição:**
- Salvar histórico de verificações realizadas
- Consultar verificações anteriores
- Comparar múltiplas verificações ao longo do tempo

**Resultados:**
- ✅ Sistema de histórico com storage local JSON
- ✅ Nova aba "📜 Histórico" na aplicação
- ✅ Auto-save após cada scan
- ✅ Bloqueio de compliance (acesso apenas após upload base)
- ✅ Listagem, visualização, exportação e deleção de sessões

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

### P3-007: Integração com SharePoint da Anbima
**Status:** 🟡 Pendente  
**Dependências:** P3-002  
**Complexidade:** Alta  
**Descrição:**
- Implementar OAuth Device Code Flow para autenticação Azure AD
- Upload automático de relatórios PDF para SharePoint
- Download e listagem de sessões históricas do SharePoint
- Sincronização bidirecional (local ↔ SharePoint)
- Sistema de fallback offline (storage local quando SharePoint indisponível)
- Estrutura de pastas por ano/mês no SharePoint
- Log de auditoria para compliance

**Informações Necessárias:**
- URL do SharePoint da Anbima
- Site/Biblioteca de documentos alvo
- Tenant ID e Client ID (Azure AD App Registration)
- Permissões de acesso ao SharePoint

---

### P3-008: Migração de Relatórios Excel para PDF
**Status:** ✅ Concluída  
**Data Conclusão:** 12/01/2026  
**Dependências:** P2-004  
**Complexidade:** Média  
**Descrição:**
- Implementar geração de PDF com reportlab ou weasyprint
- Template profissional com logo Anbima
- Três tipos de relatório:
  1. Relatório de Verificação Completa (sessão atual)
  2. Lista de Ajustes Necessários (itens "active")
  3. Relatório de Sessão Histórica
- Metadados de compliance (timestamp, session ID, usuário, hash SHA256)
- Substituir todos os exports Excel por PDF
- Botões de download atualizados na UI

**Resultados:**
- ✅ Serviço `pdf_generator.py` criado com reportlab 4.4.7
- ✅ Três tipos de relatório implementados
- ✅ Hash SHA256 para verificação de integridade
- ✅ Metadados completos (timestamp Brasília, session ID, versão)
- ✅ Botões PDF na aba Verificação
- ✅ Estilização profissional com cores corporativas #003366
- ✅ Versão atualizada para 0.6.0

**Benefícios de Compliance:**
- Documentos imutáveis (não editáveis como Excel)
- Hash SHA256 para verificação de integridade
- Metadados rastreáveis
- Formato apropriado para auditoria

---

## 📊 Resumo de Prioridades

| Prioridade | Tarefas | Status |
|------------|---------|--------|
| P1 (Crítico) | 5 | ✅ 5/5 |
| P2 (Importante) | 4 | ✅ 4/4 |
| P3 (Desejável) | 8 | ✅ 3/8 |
| **TOTAL** | **17** | **12/17 (70.6%)** |

---

## 🎯 Próxima Tarefa Recomendada
**P3-007: Integração com SharePoint da Anbima**

Implementar OAuth Device Code Flow e upload automático de PDFs para SharePoint, com sistema de fallback offline.

**Aguardando informações do usuário:**
- URL do SharePoint da Anbima
- Tenant ID e Client ID (Azure AD App Registration)
- Site/Biblioteca de documentos alvo
- Logo Anbima (PNG/SVG)

---

## ⏸️ Tarefas em Standby

### P3-009: Persistência Automática da Base Lansweeper
**Status:** ⏸️ Em Standby (por solicitação do usuário - 12/01/2026)
**Dependências:** P1-004
**Complexidade:** Baixa

**Descrição:**
- Salvar automaticamente a última base Lansweeper uploadada
- Carregar automaticamente ao abrir a aplicação
- Evita necessidade de upload repetido

**Benefícios:**
- Melhor UX - não precisa fazer upload toda vez
- Usa sempre a base mais recente
- Notificação clara de qual base está sendo usada

**Implementação Sugerida:**
- Salvar em `data/last_base.xlsx` + metadata JSON
- Auto-load na inicialização
- Botão para forçar novo upload se necessário
