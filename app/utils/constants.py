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
    'reserved': '🔖 Reservado - OK',
    'active': '⚠️ ATIVO - Requer ajuste no Lansweeper'
}

# Mapa de Emojis para visualização
STATE_EMOJI = {
    'stock': '✅',
    'broken': '🔧',
    'stolen': '🚨',
    'in repair': '⚙️',
    'old': '📦',
    'reserved': '🔖',
    'active': '⚠️'
}

# Lista de estados que NÃO requerem ajuste manual
OK_STATES = ['stock', 'broken', 'stolen', 'in repair', 'old', 'reserved']

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

# Mapeamento de normalização PT-BR → EN
# Permite que o Excel tenha estados em português
STATE_NORMALIZATION = {
    # Português → Inglês
    'estoque': 'stock',
    'quebrado': 'broken',
    'roubado': 'stolen',
    'em reparo': 'in repair',
    'antigo': 'old',
    'reservado': 'reserved',
    'ativo': 'active',
    # Inglês → Inglês (idempotência)
    'stock': 'stock',
    'broken': 'broken',
    'stolen': 'stolen',
    'in repair': 'in repair',
    'old': 'old',
    'reserved': 'reserved',
    'active': 'active'
}

# Padrões de modelos de notebooks para filtro automático
# Usado para filtrar apenas notebooks da base Lansweeper completa
NOTEBOOK_MODEL_PATTERNS = [
    'latitude',      # Dell Latitude (5400, 5410, 5420, 5440, 5480, 5490, 7300)
    'macbook',       # Apple MacBook
    'mac',           # Apple Mac (M1, M2)
    'precision',     # Dell Precision (workstation notebooks)
    'xps',           # Dell XPS
    'pro ultra',     # Dell Pro Ultra
    'inspiron',      # Dell Inspiron (se houver)
    'vostro'         # Dell Vostro (se houver)
]
