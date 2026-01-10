# Aprendizados do Projeto Stock Check

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
