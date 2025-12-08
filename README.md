# Agent Programmatic Integration Testing (APIT)

## Overview
**APIT** is an advanced automated integration testing platform powered by AI Agents. It leverages Large Language Models (LLMs) to intelligently generate, execute, and evaluate API test scenarios. The system is designed with a scalable microservices architecture to handle complex testing workflows.

## Architecture
The project is organized into several independent microservices:

*   **Frontend (`/frontend`)**: A Django-based web interface for users to manage projects, view test results, and configure settings.
*   **Agent Service (`/agent-service`)**: A FastAPI service that acts as the core "brain", orchestrating agent workflows (likely using LangGraph) to perform testing tasks.
*   **LLM Service (`/llm-service`)**: A dedicated service for handling interactions with various Large Language Models (GPT, Claude, Gemini, etc.).
*   **Gateway Service (`/gateway-service`)**: An API Gateway to route requests to the appropriate backend services.
*   **Data Collection (`/data-collection`)**: Responsible for gathering logs and testing data.
*   **Document Service (`/document-service`)**: Manages project documentation and related resources.
*   **Eval LLM (`/eval-llm`)**: Tools and services for evaluating the performance and accuracy of the LLMs used.

## Tech Stack
*   **Programming Language**: Python
*   **Web Frameworks**: Django (Frontend), FastAPI (Microservices)
*   **Database**: PostgreSQL
*   **Containerization**: Docker, Docker Compose
*   **Package Management**: `uv` (Recommended), `pip`
*   **AI Orchestration**: LangGraph

## Getting Started

### Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
*   Python 3.10 or higher.
*   [uv](https://github.com/astral-sh/uv) (Optional, for faster dependency management).

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd API-Testing
    ```

2.  **Environment Configuration:**
    Navigate to each service directory (e.g., `frontend`, `agent-service`) and create a `.env` file based on the provided `.env.example` or `.env.template`.

3.  **Run with Docker Compose:**
    You can use the provided scripts to start the entire system:

    *   **Start all services:**
        ```bash
        ./run_all.sh
        # or manually: docker compose up -d --build
        ```

    *   **Stop all services:**
        ```bash
        ./stop_all.sh
        # or manually: docker compose down
        ```

## Project Structure
```text
API-Testing/
├── agent-service/      # Core AI Agent logic (FastAPI)
├── data-collection/    # Data gathering module
├── document-service/   # Documentation management
├── eval-llm/           # LLM evaluation tools
├── frontend/           # Web Interface (Django)
├── gateway-service/    # API Gateway
├── llm-service/        # LLM Interface layer
├── run_all.sh          # Script to start the project
├── stop_all.sh         # Script to stop the project
└── README.md           # Project documentation
```

---
*This project is a Work In Progress (WIP).*