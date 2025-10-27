# Docker Workflow Guide: Building and Deploying Docker Images

A comprehensive guide for building, testing, and deploying Docker images for any project.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Creating the Dockerfile](#creating-the-dockerfile)
3. [Building the Docker Image](#building-the-docker-image)
4. [Testing Locally](#testing-locally)
5. [Pushing to Container Registry](#pushing-to-container-registry)
6. [Deploying to Production](#deploying-to-production)
7. [Common Commands Reference](#common-commands-reference)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Docker installed on your machine
- Docker account (for Docker Hub) or access to another container registry
- Your application code ready with dependencies defined

---

## Creating the Dockerfile

### Basic Dockerfile Structure

```dockerfile
# 1. Base Image
FROM python:3.9-slim

# 2. Install System Dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Python Package Manager (if using pipenv/poetry)
RUN pip install pipenv

# 4. Set Working Directory
WORKDIR /app

# 5. Copy Dependency Files First (for better caching)
COPY ["Pipfile", "Pipfile.lock", "./"]
# OR for requirements.txt:
# COPY requirements.txt .

# 6. Install Dependencies
RUN pipenv install --system --deploy
# OR for requirements.txt:
# RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy Application Code
COPY ["predict.py", "model.bin", "./"]

# 8. Expose Port (documentation only, doesn't actually publish)
EXPOSE 9696

# 9. Define Entry Point or Command
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]
# OR use CMD:
# CMD ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]
```

### Dockerfile Best Practices

- **Order layers by frequency of change** (least changing first)
- **Use specific base image versions** (e.g., `python:3.9.24-slim` not `python:latest`)
- **Combine RUN commands** to reduce layers
- **Use `.dockerignore`** file to exclude unnecessary files
- **Don't run as root** in production (use USER directive)
- **Use multi-stage builds** for smaller images

### Common Gunicorn Configuration

```dockerfile
# Basic
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]

# With workers
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "--workers", "4", "predict:app"]

# With timeout
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "--timeout", "120", "predict:app"]
```

**⚠️ Important:** Always quote the bind address or you'll get `ModuleNotFoundError: No module named '0'`

---

## Building the Docker Image

### Basic Build Command

```bash
docker build -t <image-name>:<tag> .
```

### Examples

```bash
# Build with name and default 'latest' tag
docker build -t my-app .

# Build with specific version tag
docker build -t my-app:v1.0 .

# Build with full registry path
docker build -t username/my-app:v1.0 .

# Build with no cache (force rebuild)
docker build --no-cache -t my-app .

# Build with specific Dockerfile
docker build -f Dockerfile.prod -t my-app:prod .
```

### Verify the Image

```bash
# List all images
docker images

# Inspect image details
docker inspect my-app:latest

# View image history/layers
docker history my-app:latest
```

---

## Testing Locally

### Run Container Interactively

```bash
# Basic run with port mapping
docker run -it --rm -p 9696:9696 my-app

# Options explained:
# -it        : Interactive terminal
# --rm       : Remove container after exit
# -p 9696:9696 : Map host port 9696 to container port 9696
```

### Run Container in Background (Detached Mode)

```bash
# Run in background
docker run -d -p 9696:9696 --name my-app-container my-app

# View logs
docker logs my-app-container

# Follow logs in real-time
docker logs -f my-app-container

# Stop container
docker stop my-app-container

# Start container
docker start my-app-container

# Remove container
docker rm my-app-container
```

### Test the Application

```bash
# Test with curl
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Or use your test script
python predict-test.py
```

### Access Running Container

```bash
# Execute bash in running container
docker exec -it my-app-container bash

# Execute specific command
docker exec my-app-container ls -la

# View container processes
docker top my-app-container
```

---

## Pushing to Container Registry

### Docker Hub

```bash
# 1. Login to Docker Hub
docker login

# 2. Tag your image (if not already tagged correctly)
docker tag my-app:latest username/my-app:latest
docker tag my-app:latest username/my-app:v1.0

# 3. Push to Docker Hub
docker push username/my-app:latest
docker push username/my-app:v1.0

# 4. View on Docker Hub
# https://hub.docker.com/r/username/my-app
```

### AWS Elastic Container Registry (ECR)

```bash
# 1. Authenticate to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.us-east-1.amazonaws.com

# 2. Create repository (first time only)
aws ecr create-repository --repository-name my-app

# 3. Tag image
docker tag my-app:latest \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

# 4. Push to ECR
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
```

### Azure Container Registry (ACR)

```bash
# 1. Login to ACR
az acr login --name myregistry

# 2. Tag image
docker tag my-app:latest myregistry.azurecr.io/my-app:latest

# 3. Push to ACR
docker push myregistry.azurecr.io/my-app:latest
```

### Google Container Registry (GCR)

```bash
# 1. Configure Docker to use gcloud as credential helper
gcloud auth configure-docker

# 2. Tag image
docker tag my-app:latest gcr.io/project-id/my-app:latest

# 3. Push to GCR
docker push gcr.io/project-id/my-app:latest
```

### GitHub Container Registry (GHCR)

```bash
# 1. Create Personal Access Token (PAT) with write:packages scope
# 2. Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# 3. Tag image
docker tag my-app:latest ghcr.io/username/my-app:latest

# 4. Push to GHCR
docker push ghcr.io/username/my-app:latest
```

---

## Deploying to Production

### Option 1: Simple VM/Server Deployment

```bash
# 1. SSH into your server
ssh user@your-server.com

# 2. Pull the image
docker pull username/my-app:latest

# 3. Stop and remove old container (if exists)
docker stop my-app-container
docker rm my-app-container

# 4. Run new container
docker run -d \
  --name my-app-container \
  -p 80:9696 \
  --restart unless-stopped \
  username/my-app:latest

# 5. Verify it's running
docker ps
curl http://localhost/predict
```

### Option 2: Docker Compose (Multi-Container)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    image: username/my-app:latest
    ports:
      - "80:9696"
    restart: unless-stopped
    environment:
      - ENV=production
    volumes:
      - ./data:/app/data
```

Deploy:

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: AWS ECS (Elastic Container Service)

```bash
# 1. Create task definition (JSON file)
# 2. Create ECS cluster
aws ecs create-cluster --cluster-name my-cluster

# 3. Create service
aws ecs create-service \
  --cluster my-cluster \
  --service-name my-app-service \
  --task-definition my-app:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

### Option 4: Kubernetes (K8s)

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: username/my-app:latest
        ports:
        - containerPort: 9696
```

Deploy:

```bash
kubectl apply -f deployment.yaml
kubectl expose deployment my-app --type=LoadBalancer --port=80 --target-port=9696
```

### Option 5: Cloud Run (Google Cloud)

```bash
# Deploy directly from image
gcloud run deploy my-app \
  --image gcr.io/project-id/my-app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 6: Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name my-app \
  --image myregistry.azurecr.io/my-app:latest \
  --dns-name-label my-app-unique \
  --ports 9696
```

### Option 7: Heroku

```bash
# Login to Heroku Container Registry
heroku container:login

# Tag and push
docker tag my-app:latest registry.heroku.com/my-app-name/web
docker push registry.heroku.com/my-app-name/web

# Release
heroku container:release web -a my-app-name
```

---

## Common Commands Reference

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi my-app:latest

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a

# Save image to tar file
docker save my-app:latest > my-app.tar

# Load image from tar file
docker load < my-app.tar
```

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop <container-id>

# Start container
docker start <container-id>

# Restart container
docker restart <container-id>

# Remove container
docker rm <container-id>

# Remove all stopped containers
docker container prune

# View container resource usage
docker stats
```

### Logs and Debugging

```bash
# View logs
docker logs <container-id>

# Follow logs
docker logs -f <container-id>

# View last N lines
docker logs --tail 100 <container-id>

# Execute command in running container
docker exec -it <container-id> bash

# Inspect container
docker inspect <container-id>

# View container processes
docker top <container-id>
```

### Network Management

```bash
# List networks
docker network ls

# Create network
docker network create my-network

# Connect container to network
docker network connect my-network <container-id>

# Inspect network
docker network inspect my-network
```

### Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create my-volume

# Remove volume
docker volume rm my-volume

# Remove unused volumes
docker volume prune
```

### System Cleanup

```bash
# Remove all stopped containers, unused networks, dangling images
docker system prune

# Remove everything (including unused images)
docker system prune -a

# View disk usage
docker system df
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. `ModuleNotFoundError: No module named '0'`
**Problem:** Gunicorn command parsing error

**Solution:** Quote the bind address
```dockerfile
# Wrong
ENTRYPOINT ["gunicorn", "--bind", 0.0.0.0:9696, "predict:app"]

# Correct
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]
```

#### 2. Port Already in Use
**Problem:** Port conflict on host

**Solution:** 
```bash
# Check what's using the port
sudo lsof -i :9696

# Use a different host port
docker run -p 8080:9696 my-app
```

#### 3. Permission Denied
**Problem:** Running as wrong user or missing permissions

**Solution:** Add user in Dockerfile
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

#### 4. Container Exits Immediately
**Problem:** Application crashes or wrong command

**Solution:** Check logs
```bash
docker logs <container-id>
docker run -it my-app bash  # Debug interactively
```

#### 5. Cannot Connect to Application
**Problem:** Port not exposed or firewall blocking

**Solution:**
```bash
# Check if container is listening
docker exec <container-id> netstat -tulpn

# Check if port is mapped correctly
docker ps

# Test from inside container
docker exec <container-id> curl localhost:9696
```

#### 6. Image Too Large
**Problem:** Bloated Docker image

**Solution:**
- Use slim/alpine base images
- Use multi-stage builds
- Add `.dockerignore` file
- Combine RUN commands
- Clean up in same layer

```dockerfile
# Multi-stage build example
FROM python:3.9 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]
```

#### 7. Build Cache Issues
**Problem:** Not picking up latest changes

**Solution:**
```bash
# Rebuild without cache
docker build --no-cache -t my-app .
```

#### 8. Cannot Push to Registry
**Problem:** Authentication or permission issues

**Solution:**
```bash
# Re-login
docker logout
docker login

# Check image tag format
docker tag my-app username/my-app:latest
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

---

## Quick Reference Checklist

- [ ] Create Dockerfile with proper base image
- [ ] Add all necessary dependencies
- [ ] Copy application code
- [ ] Expose necessary ports
- [ ] Define ENTRYPOINT or CMD
- [ ] Build image: `docker build -t name:tag .`
- [ ] Test locally: `docker run -it --rm -p port:port name:tag`
- [ ] Tag for registry: `docker tag name:tag registry/name:tag`
- [ ] Push to registry: `docker push registry/name:tag`
- [ ] Deploy to production
- [ ] Monitor and maintain

---

**Last Updated:** October 26, 2025
