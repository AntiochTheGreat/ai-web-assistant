# AI Web Assistant

AI Web Assistant is a modular full-stack project consisting of:

-   **Backend (Django + DRF)** --- authentication, projects, dialogs,
    messages.
-   **AI Microservice (FastAPI)** --- handles AI assistant responses.
-   **PostgreSQL (Docker)** --- main database.

The system organizes information by projects, stores dialog histories,
and processes user prompts via a local microservice.

------------------------------------------------------------------------

## Features

### 🔐 Authentication

-   JWT-based (SimpleJWT)
-   Obtain access & refresh tokens

### 📁 Projects

-   Create/manage projects
-   All dialogs belong to a project

### 💬 Dialog System

-   Unlimited dialogs inside each project
-   Messages with roles: `user` / `assistant`
-   Filtering by dialog
-   Historical context support

### 🤖 AI Microservice

-   FastAPI + Uvicorn
-   `/ask` endpoint for processing a prompt
-   `/health` endpoint for alive-checks
-   Uses local echo logic (can be replaced with OpenAI, LLMs, etc.)

------------------------------------------------------------------------

## Project Structure

    ai_web_assistant/
    ├── backend/                  # Django backend
    │   ├── manage.py
    │   ├── core/                 # Settings, URLs
    │   ├── users/                # Auth, JWT
    │   ├── projects/             # Project model + API
    │   ├── assistant/            # Dialogs, messages, AI requests
    │   └── .env
    ├── ai_service/               # FastAPI microservice
    │   ├── main.py
    │   ├── requirements.txt
    │   └── .env
    └── docker-compose.yml        # (future)

------------------------------------------------------------------------

## Backend (Django) Setup

### 1. Install dependencies

``` bash
pip install -r backend/requirements.txt
```

### 2. Environment variables

Create `backend/.env`:

    DJANGO_SECRET_KEY=change-me
    DJANGO_DEBUG=1
    DJANGO_ALLOWED_HOSTS=*

    DJANGO_DB=postgres
    POSTGRES_DB=aiwa
    POSTGRES_USER=aiwa
    POSTGRES_PASSWORD=aiwa
    POSTGRES_HOST=127.0.0.1
    POSTGRES_PORT=5432

    AI_SERVICE_URL=http://127.0.0.1:5005000

### 3. Apply migrations

``` bash
cd backend
python manage.py migrate
```

### 4. Create superuser

``` bash
python manage.py createsuperuser
```

### 5. Run backend server

``` bash
python manage.py runserver
```

Swagger docs available at:

    http://127.0.0.1:8000/api/docs/

------------------------------------------------------------------------

## AI Microservice Setup (FastAPI)

### 1. Install dependencies

``` bash
pip install -r ai_service/requirements.txt
```

### 2. Run the microservice

``` bash
uvicorn main:app --host 127.0.0.1 --port 5000 --reload
```

### 3. Health check

``` bash
GET http://127.0.0.1:5000/health
```

Expected:

``` json
{"status": "ok"}
```

------------------------------------------------------------------------

## PostgreSQL Setup (Docker)

### Start PostgreSQL

``` bash
docker run --name aiwa-postgres ^
  -e POSTGRES_DB=aiwa ^
  -e POSTGRES_USER=aiwa ^
  -e POSTGRES_PASSWORD=aiwa ^
  -p 5432:5432 ^
  -d postgres:16
```

### Manage container

``` bash
docker stop aiwa-postgres
docker start aiwa-postgres
docker ps
```

------------------------------------------------------------------------

## API Overview

### Authentication

-   `POST /api/users/token/` --- get access/refresh tokens\
-   `POST /api/users/token/refresh/`

### Projects

-   `GET/POST /api/projects/`
-   User-only access by owner permission

### Dialogs

-   `GET/POST /api/assistant/dialogs/`
-   `GET /api/assistant/dialogs/{id}/messages/`

### Messages

-   `GET /api/assistant/messages/?dialog=<id>` --- filter messages by
    dialog

### Assistant

-   `POST /api/assistant/ask/` --- send prompt to AI microservice

Request body:

``` json
{
  "project_id": 1,
  "prompt": "Hello!",
  "dialog_id": 3
}
```

Response example:

``` json
{
  "answer": "[echo] You said: Hello!",
  "dialog_id": 3,
  "project_id": 1
}
```

------------------------------------------------------------------------

## Future Improvements

-   Docker Compose for full-stack start
    (`backend + ai_service + postgres`)
-   Real LLM integration (OpenAI, Ollama, DeepSeek, etc.)
-   Frontend (React / Next.js)
-   Token usage statistics
-   Rich chat UI and context tools

------------------------------------------------------------------------

## License

MIT License
