"""
Gerenciador de Histórico de Verificações com SharePoint.

Responsável por salvar e carregar sessões de verificação no SharePoint da Anbima
usando autenticação OAuth Device Code Flow.
"""

import json
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, List, Any, Optional

# Office365 imports comentados - serão usados quando implementar OAuth (P3-007)
# from office365.sharepoint.client_context import ClientContext
# from office365.runtime.auth.authentication_context import AuthenticationContext
# from office365.sharepoint.files.file import File
# from office365.sharepoint.folders.folder import Folder


# Configurações do SharePoint
SITE_URL = "https://anbima.sharepoint.com/sites/Tecnologia"
FOLDER_PATH = "Shared Documents/StockCheck/Sessions"
TIMEZONE_BR = ZoneInfo("America/Sao_Paulo")


def get_sharepoint_client() -> Optional[Any]:
    """
    NOTA: MVP versão 1.0 usa apenas storage local.
    OAuth SharePoint será implementado em P3-007 (versão futura).
    
    Esta função retorna None para forçar uso de fallback local.
    """
    return None


def save_session_to_sharepoint(session_data: Dict[str, Any]) -> Optional[str]:
    """
    Salva sessão de verificação (versão MVP: storage local).
    
    Args:
        session_data: Dados da sessão incluindo items, summary, etc.
        
    Returns:
        session_id se sucesso, None se falha
    """
    try:
        # Usar session_id passado nos dados (fixo durante toda sessão)
        # Se não vier, gera novo timestamp
        session_id = session_data.get('session_id', datetime.now(TIMEZONE_BR).strftime("%Y%m%d_%H%M%S"))
        
        # Adicionar metadados
        full_data = {
            'session_id': session_id,
            'started_at': session_data.get('started_at'),
            'ended_at': datetime.now(TIMEZONE_BR).isoformat(),
            'lansweeper_file': session_data.get('lansweeper_file', 'N/A'),
            'total_scanned': len(session_data.get('items', [])),
            'items': session_data.get('items', [])
        }
        
        # Converter para JSON
        json_content = json.dumps(full_data, ensure_ascii=False, indent=2)
        
        # MVP: Salvar localmente
        _save_local_fallback(session_id, json_content)
        return session_id
        
    except Exception as e:
        st.error(f"❌ Erro ao salvar sessão: {str(e)}")
        return None


def load_session_from_sharepoint(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Carrega sessão específica (versão MVP: storage local).
    
    Args:
        session_id: ID da sessão (formato: YYYYMMDD_HHMMSS)
        
    Returns:
        Dados da sessão ou None se não encontrada
    """
    try:
        return _load_local_fallback(session_id)
    except Exception as e:
        st.error(f"❌ Erro ao carregar sessão {session_id}: {str(e)}")
        return None


def list_sharepoint_sessions() -> List[Dict[str, Any]]:
    """
    Lista todas as sessões disponíveis (versão MVP: storage local).
    
    Returns:
        Lista de dicionários com resumo de cada sessão
    """
    try:
        return _list_local_fallback()
    except Exception as e:
        st.error(f"❌ Erro ao listar sessões: {str(e)}")
        return []


def delete_sharepoint_session(session_id: str) -> bool:
    """
    Deleta sessão (versão MVP: storage local).
    
    Args:
        session_id: ID da sessão a deletar
        
    Returns:
        True se sucesso, False se falha
    """
    try:
        return _delete_local_fallback(session_id)
    except Exception as e:
        st.error(f"❌ Erro ao deletar sessão {session_id}: {str(e)}")
        return False


def get_session_summary(session_id: str) -> Dict[str, Any]:
    """
    Retorna resumo de uma sessão sem carregar todos os items.
    
    Args:
        session_id: ID da sessão
        
    Returns:
        Dicionário com resumo (total, ok, ajuste, not_found, date)
    """
    # Por enquanto, carregar sessão completa
    # TODO: Otimizar para ler apenas metadata
    session_data = load_session_from_sharepoint(session_id)
    
    if session_data:
        return {
            'session_id': session_id,
            'started_at': session_data.get('started_at'),
            'ended_at': session_data.get('ended_at'),
            'total': len(session_data.get('items', [])),
            'username': session_data.get('username', 'N/A'),
        }
    
    return {}


# ============================================================================
# FUNÇÕES DE FALLBACK LOCAIS (quando SharePoint não está disponível)
# ============================================================================

def _save_local_fallback(session_id: str, json_content: str) -> None:
    """Salva arquivo JSON localmente como fallback."""
    import os
    os.makedirs('data/sessions', exist_ok=True)
    with open(f'data/sessions/{session_id}.json', 'w', encoding='utf-8') as f:
        f.write(json_content)


def _load_local_fallback(session_id: str) -> Optional[Dict[str, Any]]:
    """Carrega arquivo JSON local como fallback."""
    try:
        with open(f'data/sessions/{session_id}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def _list_local_fallback() -> List[Dict[str, Any]]:
    """Lista arquivos JSON locais como fallback."""
    import os
    sessions = []
    if os.path.exists('data/sessions'):
        for filename in os.listdir('data/sessions'):
            if filename.endswith('.json'):
                session_id = filename.replace('.json', '')
                summary = get_session_summary(session_id)
                if summary:
                    sessions.append(summary)
    return sessions


def _delete_local_fallback(session_id: str) -> bool:
    """Deleta arquivo JSON local como fallback."""
    import os
    try:
        os.remove(f'data/sessions/{session_id}.json')
        return True
    except FileNotFoundError:
        return False
