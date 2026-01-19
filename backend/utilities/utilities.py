import os
import platform
from pathlib import Path
from backend.config.llm_config import llm_config

class Utilities:
    
# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

    def is_running_in_docker() -> bool:
        """Deteta se o código está a correr dentro de um container Docker."""
        if Path("/.dockerenv").exists():
            return True
        
        try:
            with open("/proc/1/cgroup", "rt") as f:
                content = f.read()
                if "docker" in content or "containerd" in content:
                    return True
        except Exception:
            pass
        
        if os.getenv("DOCKER_CONTAINER") == "true":
            return True
        
        hostname = platform.node()
        if len(hostname) == 12 and all(c in "0123456789abcdef" for c in hostname):
            return True
        
        return False


    def get_environment_info(self) -> dict:
        """Retorna informação detalhada sobre o ambiente de execução."""
        return {
            "running_in_docker": self.is_running_in_docker(),
            "platform": platform.system(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "ollama_url": llm_config.ollama_url,
            "default_llm": llm_config.default_model,
            "has_openai_key": bool(llm_config.openai_api_key),
            "dockerenv_exists": Path("/.dockerenv").exists(),
    }