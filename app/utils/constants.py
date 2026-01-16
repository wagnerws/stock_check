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
    'sold': '💰 Vendido - OK',
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
    'sold': '💰',
    'active': '⚠️'
}

# Lista de estados que NÃO requerem ajuste manual
OK_STATES = ['stock', 'broken', 'stolen', 'in repair', 'old', 'reserved', 'sold']

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
    'vendido': 'sold',
    'ativo': 'active',
    # Inglês → Inglês (idempotência)
    'stock': 'stock',
    'broken': 'broken',
    'stolen': 'stolen',
    'in repair': 'in repair',
    'old': 'old',
    'reserved': 'reserved',
    'sold': 'sold',
    'active': 'active'
}

# Padrões de modelos de notebooks para filtro automático
# Usado para filtrar apenas notebooks da base Lansweeper completa
NOTEBOOK_MODEL_PATTERNS = [
    'latitude',      # Dell Latitude (5400, 5410, 5420, 5440, 5480, 5490, 7300, 7350)
    'dell pro',      # Dell Pro 14 (pc14250)
    'optiplex',      # Dell OptiPlex (7040 e outros modelos)
    'macbook',       # Apple MacBook (Air, Pro)
    'mac14',         # Apple Mac14,2
    'macbookair',    # MacBookAir10,1
    'macbookpro'     # MacBook Pro
]

# Padrões de modelos a EXCLUIR (VMs, equipamentos de rede, etc)
EXCLUDE_MODEL_PATTERNS = [
    'virtual',       # Máquinas virtuais
    'fortinet'       # Fortinet
]

# Sistemas operacionais válidos para notebooks
# Padrões flexíveis para aceitar diferentes formatos no Lansweeper
VALID_OS_PATTERNS = [
    'windows',          # Windows (genérico)
    'microsoft',        # Microsoft Windows
    'win 10',           # Windows 10
    'win 11',           # Windows 11
    'win10',            # Windows10
    'win11',            # Windows11
    'macos',            # macOS
    'mac os',           # Mac OS
    'os x',             # OS X
    'not scanned',      # Equipamentos não escaneados pelo Lansweeper
]

