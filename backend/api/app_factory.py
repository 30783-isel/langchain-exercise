from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class FastAPIAppFactory:
    @staticmethod
    def create_app() -> FastAPI:
        app = FastAPI(
            title="LangChain Llama3 Exercise API",
            description="API for LangChain and Llama3 integration exercise",
            version="1.0.0",
        )
        
        app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://frontend:3000",
            "http://localhost:19006",
            "http://localhost:8081",
            "*"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

        return app