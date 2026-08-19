# Microservices App

[![CI](https://github.com/Ugur-B-B/microservices-app/actions/workflows/ci.yml/badge.svg)](https://github.com/Ugur-B-B/microservices-app/actions/workflows/ci.yml)

A learning project demonstrating a microservices architecture with two independent FastAPI services, each backed by its own PostgreSQL database, containerized with Docker, deployed to Kubernetes (Minikube), and wired up with a full CI/CD pipeline via GitHub Actions.

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   user-service   │         │ product-service  │
│    (FastAPI)     │         │    (FastAPI)     │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         ▼                            ▼
┌─────────────────┐         ┌─────────────────┐
│  user-postgres   │         │ product-postgres │
│   (PostgreSQL)    │         │   (PostgreSQL)    │
└─────────────────┘         └─────────────────┘
```

Each service owns its own database — a core principle of microservices architecture. Services communicate with their respective databases via Kubernetes Service Discovery (DNS-based service names, no hardcoded IPs). Database connection strings are read from the `DATABASE_URL` environment variable, so the same code runs unmodified both locally and inside Kubernetes.

## Tech Stack

- **Language:** Python 3.14
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL 16
- **Testing:** Pytest, FastAPI TestClient
- **Containerization:** Docker
- **Orchestration:** Kubernetes (via Minikube)
- **CI/CD:** GitHub Actions

## CI/CD Pipeline

Every push to `main` triggers a GitHub Actions workflow with three jobs:

1. **test-user-service** — spins up a temporary PostgreSQL container, installs dependencies, and runs the `user-service` test suite with Pytest.
2. **test-product-service** — same as above, for `product-service`. Runs in parallel with job 1.
3. **build-and-push** — runs only if both test jobs succeed. Builds Docker images for both services and pushes them to Docker Hub, tagged `latest`.

This guarantees that no broken image is ever published — an image only reaches Docker Hub after its service's tests pass.

## Services

### user-service
Manages users. Endpoints:
- `GET /users` — list all users
- `POST /users` — create a new user
- `GET /users/{user_id}` — get a single user

### product-service
Manages products and stock. Endpoints:
- `GET /products` — list all products
- `POST /products` — create a new product
- `GET /products/{product_id}` — get a single product
- `PATCH /products/{product_id}/reduce-stock` — reduce stock on order

## Kubernetes Resources

Each service is deployed with:
- **Deployment** — runs the containerized application, with `DATABASE_URL` injected via `env`
- **Service** (`ClusterIP`) — enables internal service-to-service communication by name
- **Secret** — stores database credentials (not committed to git, see `k8s/*.example.yaml`)
- **PersistentVolumeClaim** — ensures database data survives pod restarts

## Running Locally

### Prerequisites
- Docker
- Minikube
- kubectl

### 1. Start Minikube
```bash
minikube start
```

### 2. Build images inside Minikube's Docker environment
```bash
eval $(minikube docker-env)

cd user-service
docker build -t user-service:latest .

cd ../product-service
docker build -t product-service:latest .
```

### 3. Create your Secrets
Copy the example Secret files and fill in your own credentials:
```bash
cp k8s/user-postgres-secret.example.yaml k8s/user-postgres-secret.yaml
cp k8s/product-postgres-secret.example.yaml k8s/product-postgres-secret.yaml
```
Edit both files with your desired username/password.

### 4. Deploy to Kubernetes
```bash
kubectl apply -f k8s/
```

### 5. Verify pods are running
```bash
kubectl get pods
```

### 6. Access the services
```bash
kubectl port-forward service/user-service 8000:8000
kubectl port-forward service/product-service 8001:8001
```
Then visit `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8001/docs` for interactive Swagger documentation.

## Running Tests Locally

Each service has its own test suite using Pytest and FastAPI's `TestClient`:

```bash
cd user-service
source venv/bin/activate
pip install -r requirements.txt
pytest
```

Repeat for `product-service`. Tests connect to `localhost` by default, so make sure the corresponding PostgreSQL container is running (or set `DATABASE_URL` to point elsewhere).

## What This Project Demonstrates

- Designing and running independent, loosely-coupled microservices
- Each service owning its own database (database-per-service pattern)
- Writing automated tests with Pytest and FastAPI's TestClient
- Containerizing Python applications with multi-layer Docker builds
- Managing sensitive configuration with Kubernetes Secrets
- Ensuring data persistence with PersistentVolumeClaims
- Internal service discovery via Kubernetes DNS
- Environment-aware configuration (same code, different environments)
- Building a CI/CD pipeline with GitHub Actions: automated testing, conditional Docker builds, and registry publishing

## Author

Uğur Berk Bozoğlu — [GitHub](https://github.com/Ugur-B-B)
