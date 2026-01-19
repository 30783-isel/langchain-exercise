from main import app
from utilities.utilities import get_environment_info

class UtilitiesApi:
    
    @app.get("/health")
    async def health():
        """Health check detalhado com informação do ambiente."""
        return {
            "status": "healthy",
            "environment": get_environment_info()
        }


    @app.get("/api/debug/environment")
    async def debug_environment():
        """Endpoint de debug para ver toda a informação do ambiente."""
        return get_environment_info()