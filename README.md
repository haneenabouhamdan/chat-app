# Chat App

A simple real-time chat backend built with **FastAPI**, **PostgreSQL**, and **Docker**.

---

## 📖 Overview

This project provides a backend service for a chat application, supporting user authentication, message handling, and real-time capabilities using WebSockets.

---

## ✅ Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

Optional (for development):

- [Python 3.11+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/) or `pip` for dependency management

---

## 🚀 Quick Start

Clone the repository and start the project:

```bash
git clone https://github.com/haneenabouhamdan/chat-app.git
cd chat-app/backend
docker-compose up --build
```

Once the containers are running, you can access:

- **API Base URL:** [http://localhost:8000](http://localhost:8000)
- **Swagger Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Environment Variables

Make sure to configure environment variables (usually in a `.env` file inside `backend/`) for your app to connect to the database properly.

Example `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

These are loaded automatically by the backend during startup.

---

## 🛠️ Useful Commands

**Run database migrations:**

```bash
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"
docker-compose exec backend alembic upgrade head
```

**Create a new migration manually:**

```bash
docker-compose exec backend alembic revision -m "Add new changes"
```

**Apply migrations:**

```bash
docker-compose exec backend alembic upgrade head
```

---

## 🛑 Shutdown

To stop and remove all running containers, networks, and volumes:

```bash
docker-compose down
```

---

## 📢 Notes

- This project uses **alembic** for database migrations.
- Swagger UI is enabled by default for easy API exploration.
- Adjust `docker-compose.yml` and `.env` as needed for production deployments.
