# Microservices App

A learning project demonstrating a microservices architecture with two independent FastAPI services, each backed by its own PostgreSQL database, containerized with Docker and deployed to Kubernetes (Minikube).

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

Each service owns its own database — a core principle of microservices architecture. Services communicate with their respective databases via Kubernetes Service Discovery (DNS-based service names, no hardcoded IPs).

## Tech Stack

- **Language:** Python 3.14
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL 16
- **Containerization:** Docker
- **Orchestration:** Kubernetes (via Minikube)

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
- **Deployment** — runs the containerized application
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

## What This Project Demonstrates

- Designing and running independent, loosely-coupled microservices
- Each service owning its own database (database-per-service pattern)
- Containerizing Python applications with multi-layer Docker builds
- Managing sensitive configuration with Kubernetes Secrets
- Ensuring data persistence with PersistentVolumeClaims
- Internal service discovery via Kubernetes DNS
- Deploying and orchestrating a multi-service application on Kubernetes

## Author

Uğur Berk Bozoğlu — [GitHub](https://github.com/Ugur-B-B)
