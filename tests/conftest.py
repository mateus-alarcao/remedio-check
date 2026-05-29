"""
conftest.py — Configuração global do pytest.

Adiciona o diretório src/ ao sys.path para que os testes possam
importar os módulos da aplicação sem necessidade de instalação de pacote.
"""

import os
import sys

# Adiciona src/ ao path de importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
