# Configuração Docker - Projeto Crypto Intelligence

Este guia explica como executar o projeto usando Docker.

## Estrutura do Projeto

```
projeto/
├── backend/           # API Python (FastAPI)
├── frontend/          # Interface Next.js
├── Dockerfile.backend # Dockerfile para o backend
├── Dockerfile.frontend # Dockerfile para o frontend
├── docker-compose.yml # Orquestração dos serviços
└── requirements.txt   # Dependências Python
```

## Pré-requisitos

- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 1.29+)

## Como Usar

### 1. Preparar o Projeto

Primeiro, coloca os ficheiros Docker na raiz do teu projeto:

```bash
# Copia os ficheiros para a raiz do projeto
cp Dockerfile.backend ./
cp Dockerfile.frontend ./
cp docker-compose.yml ./
cp requirements.txt backend/
```

### 2. Construir e Iniciar os Containers

```bash
# Construir as imagens e iniciar os serviços
docker-compose up --build

# Ou para correr em background (detached mode)
docker-compose up -d --build
```

### 3. Aceder às Aplicações

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs (Swagger UI)

### 4. Parar os Containers

```bash
# Parar os serviços
docker-compose down

# Parar e remover volumes (atenção: apaga dados)
docker-compose down -v
```

## Comandos Úteis

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs apenas do backend
docker-compose logs -f backend

# Ver logs apenas do frontend
docker-compose logs -f frontend

# Reconstruir apenas um serviço
docker-compose up -d --build backend

# Entrar no container do backend
docker exec -it crypto-backend /bin/bash

# Entrar no container do frontend
docker exec -it crypto-frontend /bin/sh
```

## Notas Importantes

### Variáveis de Ambiente

Se precisares de configurar variáveis de ambiente (como API keys), cria um ficheiro `.env` em cada pasta:

**backend/.env:**
```
OPENAI_API_KEY=sua_chave_aqui
OLLAMA_BASE_URL=http://localhost:11434
```

Depois descomenta a linha no `docker-compose.yml`:
```yaml
env_file:
  - backend/.env
```

### Desenvolvimento vs Produção

Os Dockerfiles atuais estão configurados para produção. Para desenvolvimento com hot-reload:

1. **Backend**: Modifica o CMD no Dockerfile.backend:
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

2. **Frontend**: Modifica o CMD no Dockerfile.frontend:
```dockerfile
CMD ["npm", "run", "dev"]
```

E adiciona volumes no docker-compose.yml para sincronizar o código:
```yaml
services:
  backend:
    volumes:
      - ./backend:/app
  
  frontend:
    volumes:
      - ./frontend:/app
      - /app/node_modules
```

### Ollama

Se estiveres a usar Ollama localmente, certifica-te que está acessível do container. Podes precisar de:

1. Configurar o Ollama para aceitar conexões externas
2. Usar o IP do host em vez de `localhost`
3. Ou adicionar o Ollama como serviço no docker-compose

## Resolução de Problemas

### Porta já em uso
```bash
# Verifica que processos estão a usar as portas
lsof -i :3000
lsof -i :8000

# Mata o processo ou muda as portas no docker-compose.yml
```

### Erro de build
```bash
# Limpa tudo e reconstrói
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Frontend não consegue conectar ao Backend
- Verifica que o URL no frontend está a apontar para `http://backend:8000` dentro dos containers
- Ou usa `http://localhost:8000` se estiveres a testar do browser

## Próximos Passos

- [ ] Adicionar nginx como reverse proxy
- [ ] Configurar volumes persistentes para dados
- [ ] Adicionar CI/CD
- [ ] Optimizar imagens Docker (multi-stage builds)
