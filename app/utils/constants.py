"""
Constantes do domínio de negócio.
"""

# Estados válidos de equipamentos no sistema
VALID_STATES = {
    'stock': '✅ Em estoque - OK',
    'broken': '🔧 Quebrado - OK',
    'stolen': '🚨 Roubado - OK',
    'in repair': '⚙️ Em reparo - OK',
    'old': '📦 Equipamento antigo - OK',
    'active': '⚠️ ATIVO - Requer ajuste no Lansweeper'
}

# Mapa de Emojis para visualização
STATE_EMOJI = {
    'stock': '✅',
    'broken': '🔧',
    'stolen': '🚨',
    'in repair': '⚙️',
    'old': '📦',
    'active': '⚠️'
}

# Lista de estados que NÃO requerem ajuste manual
OK_STATES = ['stock', 'broken', 'stolen', 'in repair', 'old']

# Estado que requer ajuste no Lansweeper
REQUIRES_ADJUSTMENT_STATE = 'active'

# Extensões de arquivo permitidas
ALLOWED_EXTENSIONS = ['.xlsx', '.xls']

# MIME types válidos para validação
VALID_MIME_TYPES = [
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
    'application/vnd.ms-excel'  # .xls
]

# Formato de nomenclatura para arquivos exportados
EXPORT_FILENAME_PATTERN = "ajustes_lansweeper_{date}.xlsx"
