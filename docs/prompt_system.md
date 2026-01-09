# System Prompt - Agent Configuration

## 📁 Diretórios e Arquivos de Controle

### Diretório de Artefatos
Todos os arquivos de acompanhamento de tarefas devem ser criados em:
```
C:\Users\leona\.gemini\antigravity\brain\<session-id>
```

### Arquivos Obrigatórios em PT-BR
Os seguintes arquivos **DEVEM** ser criados em **Português Brasileiro (PT-BR)**:
- `task.md` - Lista de tarefas e checklist
- `implementation_plan.md` - Plano de implementação detalhado
- `walkthrough.md` - Documentação do que foi realizado

### Arquivos de Contexto
O agente **DEVE** fazer a leitura dos seguintes arquivos no início de cada sessão:
- `docs/persona.md` - Perfil e expertise do desenvolvedor
- `docs/historico.md` - Histórico de tudo que foi feito no projeto
- `docs/backlog.md` - Backlog de tarefas priorizadas (passo a passo completo)
- `config.md` - Configurações do projeto e ponto de retomada
- `aprendizado.md` - Aprendizados e lições obtidas

> [!IMPORTANT]
> O arquivo `docs/backlog.md` contém o **passo a passo completo** de todas as tarefas do projeto, organizado por prioridade (P1, P2, P3). Este arquivo deve ser consultado regularmente e atualizado conforme o progresso do desenvolvimento.

---

## 🔄 Fluxo de Trabalho Obrigatório

### 1. Gestão de Backlog
- **SEMPRE** crie novas atividades no `docs/backlog.md`
- Classifique cada tarefa por prioridade: **P1 (Alta)**, **P2 (Média)**, **P3 (Baixa)**
- Mantenha o backlog atualizado conforme tarefas são iniciadas/concluídas
- O backlog deve conter o passo a passo detalhado de cada tarefa com suas dependências

### 2. Registro de Histórico
- **SEMPRE** registre no `historico.md` tudo que foi feito
- Inclua: data, tarefa realizada, arquivos modificados/criados, resultados
- Mantenha formato cronológico reverso (mais recente primeiro)

### 3. Documentação de Aprendizados
- **SEMPRE** registre no `aprendizado.md` os aprendizados obtidos
- Inclua: problemas encontrados, soluções aplicadas, boas práticas descobertas
- Documente anti-padrões identificados e como evitá-los

---

## 🎯 Comandos Especiais

### **"plan"**
Cria um `implementation_plan.md` detalhado **em PT-BR** para a tarefa atual.
- Deve incluir: objetivo, análise, mudanças propostas, plano de verificação
- Solicitar aprovação do usuário antes de executar

### **"next task"**
Inicia automaticamente a próxima tarefa do backlog:
1. Ler `docs/backlog.md`
2. Identificar tarefas com **Prioridade 1 (P1)** que estão pendentes
3. Criar `task.md` para a tarefa selecionada
4. Gerar `implementation_plan.md` em PT-BR
5. Solicitar aprovação para prosseguir

### **"continue"**
Retoma o trabalho do ponto onde parou:
1. Ler `config.md`
2. Localizar seção "Resume Point" ou "Ponto de Retomada"
3. Retomar o raciocínio e continuar a execução

### **"audit"**
Inicia o **Protocolo de Segurança e Qualidade**:
1. Ler `config.md` (seções "Security & OpSec" e "Lessons Learned")
2. Escanear arquivos recentes em busca de:
   - **Secrets hardcoded** (API Keys, Senhas, Tokens)
   - **Anti-padrões conhecidos** (ex: `print()` em loop, `time.sleep()` bloqueante)
   - **Imports não utilizados** ou caminhos quebrados
3. Listar vulnerabilidades potenciais ou bugs com prioridade:
   - **CRITICAL** - Requer correção imediata
   - **HIGH** - Deve ser corrigido antes de deploy
   - **MEDIUM** - Melhorias recomendadas
   - **LOW** - Otimizações opcionais

### **"cleanup"**
Inicia o **Protocolo de Organização**:
1. Identificar arquivos temporários para remoção:
   - `.log`, `debug_*.png`, `__pycache__`, `.pyc`, etc.
2. Verificar arquivos soltos na raiz que deveriam estar em `/scripts`, `/docs`, `/tests`
3. Verificar formatação e indentação dos arquivos modificados recentemente
4. Sugerir atualizações na documentação (`historico.md`, `config.md`) se estiverem desatualizadas

### **"save"**
Executa o **Protocolo de Fechamento de Sessão** imediatamente:
1. Atualizar `docs/historico.md` com todas as ações realizadas na sessão
2. Atualizar `aprendizado.md` com novos conhecimentos adquiridos
3. Atualizar `config.md` com "Resume Point" atual
4. Atualizar `docs/backlog.md` marcando tarefas concluídas
5. Criar resumo da sessão para próxima retomada

---

## 💻 Diretrizes de Código

### Idioma
- **Código**: Sempre em **inglês** (variáveis, funções, classes, métodos)
- **Strings**: Podem ser em **PT-BR** quando apropriado (mensagens ao usuário, logs)
- **Comentários**: Podem ser em **PT-BR** para melhor compreensão

### Exemplo
```python
# Função para validar email do usuário
def validate_email(email):
    """
    Valida o formato do email fornecido.
    
    Args:
        email (str): Email a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        print("Email inválido")  # String em PT-BR
        return False
    
    print("Email válido")  # String em PT-BR
    return True
```

---

## 📋 Checklist Inicial de Sessão

Ao iniciar uma nova sessão, o agente deve:
- [ ] Ler `docs/persona.md` para entender o perfil do desenvolvedor
- [ ] Ler `docs/historico.md` para contexto do que já foi feito
- [ ] Ler `docs/backlog.md` para conhecer tarefas pendentes (passo a passo completo)
- [ ] Ler `config.md` para configurações e ponto de retomada
- [ ] Ler `aprendizado.md` para conhecer lições aprendidas
- [ ] Verificar se há "Resume Point" em `config.md`
- [ ] Confirmar com usuário sobre qual tarefa trabalhar

---

## 🎨 Princípios de Desenvolvimento

Baseado na leitura de `persona.md`, sempre seguir:
1. **Segurança em primeiro lugar** - Nunca expor credenciais ou dados sensíveis
2. **Código limpo e organizado** - Seguir padrões de nomenclatura e estrutura
3. **Tratamento de erros** - Sempre validar inputs e tratar exceções
4. **Documentação clara** - Comentários úteis e documentação completa
5. **Testes automatizados** - Validar funcionalidades com testes apropriados
6. **Performance** - Escrever código eficiente e escalável

---

**Última atualização**: 2026-01-08
