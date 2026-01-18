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

Se estiveres a usar Ollama localmente, certifica-te que está acessível do container. Podes precisar d
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
























































# Configuração Docker - Projeto Crypto Intelligence (com Frontend Mobile)

Este guia explica como executar o projeto completo usando Docker, incluindo o frontend mobile.

## Estrutura do Projeto

```
projeto/
├── backend/              # API Python (FastAPI)
├── frontend/             # Interface Next.js (Web)
├── frontend-mobile/      # App Mobile (Expo/React Native)
├── Dockerfile.backend    # Dockerfile para o backend
├── Dockerfile.frontend   # Dockerfile para o frontend web
├── Dockerfile.mobile     # Dockerfile para o frontend mobile
├── docker-compose.yml    # Orquestração dos serviços
└── .dockerignore        # Ficheiros a ignorar no build
```

## Pré-requisitos

- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 1.29+)

## Como Usar

### 1. Construir e Iniciar Todos os Containers

```bash
# Construir as imagens e iniciar todos os serviços
docker-compose up --build

# Ou para correr em background (detached mode)
docker-compose up -d --build
```

### 2. Iniciar Apenas Alguns Serviços

```bash
# Apenas backend e frontend web
docker-compose up backend frontend

# Apenas backend e mobile
docker-compose up backend frontend-mobile

# Apenas mobile
docker-compose up frontend-mobile
```

### 3. Aceder às Aplicações

- **Frontend Web**: http://localhost:3000
- **Frontend Mobile (Web)**: http://localhost:19006
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs (Swagger UI)
- **Metro Bundler**: http://localhost:19000

### 4. Parar os Containers

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes (atenção: apaga dados)
docker-compose down -v
```

## Frontend Mobile

### Desenvolvimento Web
O frontend mobile está configurado para correr em modo web dentro do container:
- Acede a http://localhost:19006 no teu browser
- Mudanças no código são refletidas automaticamente (hot-reload)

### Desenvolvimento Nativo (iOS/Android)

Para testar em emuladores ou dispositivos físicos:

1. **Para o container mobile atual**:
```bash
docker-compose stop frontend-mobile
```

2. **Corre localmente na tua máquina**:
```bash
cd frontend-mobile
npm install
npx expo start
```

3. **Conecta ao backend no Docker**:
   - No código, usa `http://localhost:8000` para APIs
   - O Expo permite aceder ao localhost da máquina host

## Comandos Úteis

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs apenas do backend
docker-compose logs -f backend

# Ver logs apenas do frontend web
docker-compose logs -f frontend

# Ver logs apenas do frontend mobile
docker-compose logs -f frontend-mobile

# Reconstruir apenas um serviço
docker-compose up -d --build frontend-mobile

# Entrar no container do backend
docker exec -it crypto-backend /bin/bash

# Entrar no container do frontend web
docker exec -it crypto-frontend /bin/sh

# Entrar no container do frontend mobile
docker exec -it crypto-mobile /bin/sh

# Reiniciar apenas o mobile
docker-compose restart frontend-mobile
```

## Variáveis de Ambiente

### Backend
Cria `backend/.env`:
```env
OPENAI_API_KEY=sua_chave_aqui
OLLAMA_BASE_URL=http://localhost:11434
```

### Frontend Mobile
Cria `frontend-mobile/.env` se necessário:
```env
API_URL=http://backend:8000
```

Depois descomenta no `docker-compose.yml`:
```yaml
env_file:
  - backend/.env
```

## Resolução de Problemas

### Porta já em uso
```bash
# Verifica processos nas portas
lsof -i :3000   # Frontend web
lsof -i :8000   # Backend
lsof -i :19006  # Mobile web

# Mata o processo ou muda as portas no docker-compose.yml
```

### Erro de build do mobile
```bash
# Limpa tudo e reconstrói
docker-compose down -v
docker system prune -a
docker-compose up --build frontend-mobile
```

### Mobile não consegue conectar ao Backend
- Dentro do container: usa `http://backend:8000`
- Do browser (acessando :19006): usa `http://localhost:8000`
- De dispositivo físico: usa o IP da tua máquina (ex: `http://192.168.1.100:8000`)

### Expo não inicia
```bash
# Verifica os logs
docker-compose logs frontend-mobile

# Limpa cache do Expo
docker-compose exec frontend-mobile npx expo start -c
```

## Desenvolvimento vs Produção

### Desenvolvimento (atual)
- Frontend mobile: modo desenvolvimento com hot-reload
- Volumes montados para sincronização de código
- Expo DevTools ativados

### Produção
Para produção do mobile, considera:
1. Build para web estático: `expo export:web`
2. Build nativo: usar EAS Build
3. Servir web build com nginx

## Limitações do Container Mobile

⚠️ **Importante**: O container mobile está otimizado para desenvolvimento web.

**Não suportado no container**:
- Build de apps iOS/Android nativos
- Execução em emuladores iOS/Android
- Conexão com Expo Go em dispositivos físicos

**Recomendação**: Para desenvolvimento nativo, corre o Expo localmente e conecta ao backend no Docker.

## Próximos Passos

- [ ] Adicionar nginx como reverse proxy
- [ ] Configurar volumes persistentes para dados
- [ ] Adicionar CI/CD
- [ ] Optimizar imagens Docker (multi-stage builds)
- [ ] Configurar EAS Build para mobile production
- [ ] Adicionar testes automatizados