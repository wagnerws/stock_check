"""
Configurações centralizadas da aplicação Stock Check.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da aplicação Streamlit
PAGE_TITLE = "Stock Check"
PAGE_ICON = "📦"

# Configurações de upload de arquivos
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Colunas obrigatórias do Excel do Lansweeper
REQUIRED_COLUMNS = ["Serialnumber", "State", "Name", "lastuser"]

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configurações de log
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
