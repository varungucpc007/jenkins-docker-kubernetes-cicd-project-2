# Jenkins Docker Kubernetes CI/CD Project

This project builds a Flask application Docker image, pushes it to Docker Hub, and deploys it to Kubernetes using a Jenkins pipeline.

The pipeline is designed for a Windows Jenkins agent because it uses `bat` commands.

## Project Flow

```text
GitHub Repository
      |
      v
Jenkins Checkout
      |
      v
Docker Image Build
      |
      v
Docker Hub Push
      |
      v
Kubernetes Deployment
      |
      v
Live Flask Website
```

## Required Tools

Install these on the Jenkins machine:

- Jenkins
- Git
- Docker Desktop
- Kubernetes, either Docker Desktop Kubernetes or Minikube
- kubectl

Check Docker:

```powershell
docker version
```

Check Kubernetes:

```powershell
kubectl get nodes
```

If Kubernetes is not running, start it first.

For Minikube:

```powershell
minikube start
kubectl config use-context minikube
kubectl get nodes
```

For Docker Desktop Kubernetes:

```powershell
kubectl config use-context docker-desktop
kubectl get nodes
```

## Expected Repository Structure

```text
.
├── Jenkinsfile
├── app
│   ├── Dockerfile
│   └── application files
└── k8s
    ├── deployment.yaml
    └── service.yaml
```

## Jenkins Pipeline Parameters

After the Jenkinsfile is committed, Jenkins will show **Build with Parameters**.

Use these values:

| Parameter | Value |
|---|---|
| `GIT_REPO` | `https://github.com/varungucpc007/jenkins-docker-kubernetes-cicd-project-2.git` |
| `GIT_BRANCH` | `main` |
| `IMAGE_NAME` | `varungucpc007/flask-k8s-app` |
| `APP_DIR` | `app` |
| `K8S_DIR` | `k8s` |
| `DEPLOYMENT_NAME` | `flask-app` |
| `CONTAINER_NAME` | `flask-app` |
| `KUBE_NAMESPACE` | `default` |
| `KUBECONFIG_PATH` | `C:\Users\varun\.kube\config` |
| `KUBECTL_VALIDATE` | `false` |
| `DOCKER_USERNAME` | `varungucpc007` |
| `DOCKER_PASSWORD` | Docker Hub access token |

Do not paste your normal Docker password. Use a Docker Hub access token.

## Create Docker Hub Access Token

1. Open Docker Hub.
2. Go to **Account Settings**.
3. Open **Personal access tokens**.
4. Create a new token.
5. Give permission: `Read, Write`.
6. Copy the token immediately.
7. Use this token as the Jenkins `DOCKER_PASSWORD` parameter.

If a token was shown in a screenshot or shared anywhere, delete it and create a new token.

## Jenkinsfile

The Jenkins pipeline performs these stages:

1. Checkout source code from GitHub.
2. Build Docker image from the `app` folder.
3. Tag the image with both the Jenkins build number and `latest`.
4. Login to Docker Hub.
5. Push both image tags to Docker Hub.
6. Deploy Kubernetes YAML files.
7. Update the Kubernetes deployment image.
8. Wait for the Kubernetes rollout to finish.

## Kubernetes Deployment Requirements

The deployment name and container name must match the Jenkins parameters:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app
          image: varungucpc007/flask-k8s-app:latest
          ports:
            - containerPort: 5000
```

The important values are:

```text
deployment name: flask-app
container name: flask-app
label: app=flask-app
containerPort: 5000
```

## Kubernetes Service Example

Use a NodePort service to open the website from the browser:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
      nodePort: 30080
```

Apply manually if needed:

```powershell
kubectl apply -f k8s\service.yaml
```

## Run Jenkins Pipeline

1. Open Jenkins.
2. Open the pipeline job.
3. Click **Build with Parameters**.
4. Enter Docker username and Docker access token.
5. Keep the remaining values as default unless your project paths are different.
6. Click **Build**.

Expected successful stages:

```text
Checkout
Build Docker Image
Push Docker Image
Deploy to Kubernetes
```

## Verify Deployment

After Jenkins finishes successfully, run:

```powershell
kubectl get pods
kubectl get deployment
kubectl get svc
```

Check rollout:

```powershell
kubectl rollout status deployment/flask-app
```

Check running pods:

```powershell
kubectl get pods -l app=flask-app
```

## Open Website Live

### Option 1: Port Forward

This is the fastest way:

```powershell
kubectl port-forward deployment/flask-app 5000:5000
```

Open in browser:

```text
http://localhost:5000
```

Keep the terminal open while using the website.

### Option 2: NodePort

If the service uses `nodePort: 30080`, open:

```text
http://localhost:30080
```

For Minikube, use:

```powershell
minikube service flask-app-service --url
```

Open the URL printed by Minikube.

## Troubleshooting

### Docker Login Failed

Cause:

```text
docker login returned exit code 1
```

Fix:

- Create a new Docker Hub access token.
- Use permission `Read, Write`.
- Pass it in Jenkins as `DOCKER_PASSWORD`.
- Make sure `DOCKER_USERNAME` is `varungucpc007`.

### Docker Push Failed

Cause:

```text
denied: requested access to the resource is denied
```

Fix:

- Make sure the image name starts with your Docker Hub username:

```text
varungucpc007/flask-k8s-app
```

- Make sure Docker token has write permission.

### Kubeconfig Path Empty

Cause:

```text
ERROR: kubeconfig not found at
```

Fix:

Set:

```text
KUBECONFIG_PATH = C:\Users\varun\.kube\config
```

The Jenkinsfile also includes a fallback for this path.

### Kubernetes API Not Reachable

Cause:

```text
dial tcp 127.0.0.1:xxxxx: connectex: No connection could be made
```

Fix:

Start Kubernetes first:

```powershell
minikube start
kubectl get nodes
```

or enable Kubernetes in Docker Desktop.

### Deployment Fails During Rollout

Check pod logs:

```powershell
kubectl get pods
kubectl logs <pod-name>
```

Describe the pod:

```powershell
kubectl describe pod <pod-name>
```

Common causes:

- Flask app is not listening on `0.0.0.0`.
- Wrong container port.
- Docker image was not pushed correctly.
- Kubernetes deployment container name does not match `flask-app`.

## Important Notes

- Do not commit Docker tokens to GitHub.
- Do not share Docker tokens in screenshots.
- If a Docker token is exposed, revoke it immediately.
- Jenkins must run on the same machine where Docker and Kubernetes are available.
- For this project, the Jenkins agent must support Windows `bat` commands.

## Final Live URL

Use one of these after successful deployment:

```text
http://localhost:5000
```

or:

```text
http://localhost:30080
```

