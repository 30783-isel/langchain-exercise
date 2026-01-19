"""
Módulo agents

Exporta agentes disponíveis para uso externo
"""

from agents.crypto_agent import CryptoAgent, create_crypto_agent

__all__ = [
    "CryptoAgent",
    "create_crypto_agent",
]