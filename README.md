# AI Web Assistant

## Overview

AI Web Assistant is a modular web application that integrates **Django** and **FastAPI** to create an intelligent web-based assistant. The Django backend manages user authentication, project organization, and administrative logic, while a separate FastAPI microservice handles AI-related operations (such as interacting with language models).

The architecture is designed for scalability and clean separation of responsibilities between web management and AI processing.

---

## Architecture

```
ai_web_assistant/
├── backend/
│   ├── manage.py
│   ├── core/                 # Django core settings and configurations
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                # User management app
│   ├── projects/             # Project organization app
│   ├── assistant/            # AI assistant integration app
│   ├── requirements.txt
│
├── ai_service/               # AI microservice (FastAPI)
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml        # Multi-container configuration
└── README.md                 # Project documentation
```

---

## Components

### 1. Django Backend (`backend/`)

Responsible for managing users, projects, and the administrative panel.

**Key Features:**

* Authentication and user profiles
* Project management and database models
* REST API endpoints for frontend interaction

### 2. FastAPI Microservice (`ai_service/`)

Handles AI logic, model inference, and prompt processing.

**Key Features:**

* `/ask` endpoint to process AI queries
* Interacts with external or local AI models (e.g., OpenAI API)
* Returns structured JSON responses

### 3. Docker Compose

Defines containers for Django, FastAPI, and optionally PostgreSQL/Redis.
This allows isolated development and deployment.

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone git@github.com:AntiochTheGreat/ai-web-assistant.git
cd ai_web_assistant
```

### 2. Set Up Django Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Set Up AI Microservice

```bash
cd ai_service
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 5000
```

### 4. (Optional) Run with Docker Compose

```bash
docker-compose up --build
```

---

## Example Workflow

1. The user logs in through the Django backend.
2. A request is made from the web interface to the Django API.
3. Django forwards AI-related requests to the FastAPI microservice.
4. The AI microservice processes the input (e.g., through OpenAI API) and returns the response.
5. The result is displayed in the user's browser.

---

## Future Roadmap

* Integrate OpenAI, Anthropic, and Mistral APIs.
* Add a vector database for knowledge retrieval (e.g., pgvector or Chroma).
* Develop frontend (React/Vue).
* Enable context-aware conversations and document-based training.

---

## License

MIT License © 2025 Sergey Bakharev
