# Microservices Authentication with Traefik

A microservices architecture demonstrating JWT-based authentication using Flask services and Traefik as a reverse proxy. The project includes both Docker Compose and Kubernetes deployment configurations.

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Traefik   │───▶│ Auth Service│───▶│ App Service │
│             │    │ (Gateway)   │    │ (JWT Gen)   │    │ (Business)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

- **Traefik**: Reverse proxy with ForwardAuth middleware
- **Auth Service**: Generates JWT tokens based on request headers
- **App Service**: Validates JWT tokens and serves protected endpoints

## Project Structure

```
.
├── app/                    # Main application service
│   ├── app.py             # Flask app with protected endpoints
│   ├── Dockerfile         # Container definition
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
├── auth/                  # Authentication service
│   ├── auth.py           # JWT token generation
│   ├── Dockerfile        # Container definition
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables
├── traefik/              # Traefik configuration
│   ├── traefik.yaml     # Main Traefik config
│   └── dynamic.yaml     # Dynamic routing rules
├── k8s/                 # Kubernetes manifests
│   ├── namespace.yaml
│   ├── auth-k8s/       # Auth service K8s configs
│   ├── app-k8s/        # App service K8s configs
│   └── ingress/        # Ingress configuration
└── docker-compose.yml  # Docker Compose setup
```

## Quick Start with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- Ports 80, 8081, and 443 available

### 1. Clone and Setup
```bash
git clone <repository-url>
cd k8s
```

### 2. Configure Environment Variables
Create or update the `.env` files:

**auth/.env**:
```env
JWT_SECRET_KEY=your_secure_jwt_secret_key_here
PORT=5000
```

**app/.env**:
```env
JWT_SECRET_KEY=your_secure_jwt_secret_key_here
PORT=5001
```

### 3. Start Services
```bash
docker-compose up --build
```

### 4. Test the Application
```bash
# Test without authentication (should work due to ForwardAuth)
curl -H "name: testuser" http://localhost/hello

# Check Traefik dashboard
open http://localhost:8081
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured
- Docker registry access (for custom images)

### 1. Fix Configuration Issues

First, update the Kubernetes configurations to resolve naming conflicts:

**k8s/auth-k8s/configmap.yaml**:
````yaml
# filepath: k8s/auth-k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: auth-config  # Changed from app-config
  namespace: auth-app
data:
  PORT: "5000"