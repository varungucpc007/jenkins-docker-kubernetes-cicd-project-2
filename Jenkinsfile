pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    parameters {
        string(name: 'GIT_REPO', defaultValue: 'https://github.com/varungucpc007/jenkins-docker-kubernetes-cicd-project-2.git', description: 'Git repository URL')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch')
        string(name: 'IMAGE_NAME', defaultValue: 'varungucpc007/flask-k8s-app', description: 'Docker image name')
        string(name: 'APP_DIR', defaultValue: 'app', description: 'Folder containing Dockerfile')
        string(name: 'K8S_DIR', defaultValue: 'k8s', description: 'Folder containing Kubernetes YAML files')
        string(name: 'DEPLOYMENT_NAME', defaultValue: 'flask-app', description: 'Kubernetes deployment name')
        string(name: 'CONTAINER_NAME', defaultValue: 'flask-app', description: 'Kubernetes container name')
        string(name: 'KUBE_NAMESPACE', defaultValue: 'default', description: 'Kubernetes namespace')
        string(name: 'KUBECONFIG_PATH', defaultValue: 'C:\\Users\\varun\\.kube\\config', description: 'Live kubeconfig path on Jenkins Windows machine')
        booleanParam(name: 'KUBECTL_VALIDATE', defaultValue: false, description: 'Validate Kubernetes YAML against cluster OpenAPI schema')
        string(name: 'DOCKER_USERNAME', defaultValue: 'varungucpc007', description: 'Docker Hub username')
        password(name: 'DOCKER_PASSWORD', defaultValue: 'dckr_pat_GEGWJBgd_ptD5hmekEn2UrY7BwY', description: 'Docker Hub access token')
    }

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                git branch: "${params.GIT_BRANCH}", url: "${params.GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                @echo off
                setlocal

                if not exist "%APP_DIR%\\Dockerfile" (
                    echo ERROR: %APP_DIR%\\Dockerfile not found.
                    exit /b 1
                )

                docker version
                if errorlevel 1 exit /b 1

                echo Building Docker image %IMAGE_NAME%:%IMAGE_TAG%
                docker build -t "%IMAGE_NAME%:%IMAGE_TAG%" "%APP_DIR%"
                if errorlevel 1 exit /b 1

                docker tag "%IMAGE_NAME%:%IMAGE_TAG%" "%IMAGE_NAME%:latest"
                if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withEnv([
                    "DOCKER_USER=${params.DOCKER_USERNAME}",
                    "DOCKER_PASS=${params.DOCKER_PASSWORD}"
                ]) {
                    bat '''
                    @echo off
                    setlocal

                    if "%DOCKER_USER%"=="" (
                        echo ERROR: DOCKER_USERNAME parameter is empty.
                        exit /b 1
                    )

                    if "%DOCKER_PASS%"=="" (
                        echo ERROR: DOCKER_PASSWORD parameter is empty. Use Docker Hub access token here.
                        exit /b 1
                    )

                    echo Logging into Docker Hub as %DOCKER_USER%
                    powershell -NoProfile -NonInteractive -Command "$env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin; exit $LASTEXITCODE"
                    if errorlevel 1 exit /b 1

                    echo Pushing Docker image %IMAGE_NAME%:%IMAGE_TAG%
                    docker push "%IMAGE_NAME%:%IMAGE_TAG%"
                    if errorlevel 1 exit /b 1

                    echo Pushing Docker image %IMAGE_NAME%:latest
                    docker push "%IMAGE_NAME%:latest"
                    if errorlevel 1 exit /b 1

                    docker logout
                    exit /b 0
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                @echo off
                setlocal
                set "KUBECONFIG=%KUBECONFIG_PATH%"

                if not exist "%KUBECONFIG%" (
                    echo ERROR: kubeconfig not found at %KUBECONFIG%
                    echo Fix KUBECONFIG_PATH or start/create your Kubernetes cluster first.
                    exit /b 1
                )

                if not exist "%K8S_DIR%\\deployment.yaml" (
                    echo ERROR: %K8S_DIR%\\deployment.yaml not found.
                    exit /b 1
                )

                if not exist "%K8S_DIR%\\service.yaml" (
                    echo ERROR: %K8S_DIR%\\service.yaml not found.
                    exit /b 1
                )

                kubectl version --client
                if errorlevel 1 exit /b 1

                echo Current Kubernetes context:
                kubectl config current-context
                if errorlevel 1 exit /b 1

                echo Checking Kubernetes cluster connection...
                kubectl cluster-info
                if errorlevel 1 (
                    echo ERROR: Kubernetes API server is not reachable.
                    echo Your kubeconfig points to a local cluster that is not running or has a changed port.
                    echo Start Docker Desktop Kubernetes or run: minikube start
                    exit /b 1
                )

                kubectl get namespace "%KUBE_NAMESPACE%" >nul 2>&1
                if errorlevel 1 (
                    echo Creating namespace %KUBE_NAMESPACE%
                    kubectl create namespace "%KUBE_NAMESPACE%"
                    if errorlevel 1 exit /b 1
                )

                set "VALIDATE_ARG=--validate=false"
                if /I "%KUBECTL_VALIDATE%"=="true" set "VALIDATE_ARG=--validate=true"

                echo Applying Kubernetes manifests...
                kubectl apply %VALIDATE_ARG% -n "%KUBE_NAMESPACE%" -f "%K8S_DIR%\\deployment.yaml"
                if errorlevel 1 exit /b 1

                kubectl apply %VALIDATE_ARG% -n "%KUBE_NAMESPACE%" -f "%K8S_DIR%\\service.yaml"
                if errorlevel 1 exit /b 1

                echo Updating deployment image...
                kubectl set image -n "%KUBE_NAMESPACE%" "deployment/%DEPLOYMENT_NAME%" "%CONTAINER_NAME%=%IMAGE_NAME%:%IMAGE_TAG%"
                if errorlevel 1 exit /b 1

                echo Waiting for rollout...
                kubectl rollout status -n "%KUBE_NAMESPACE%" "deployment/%DEPLOYMENT_NAME%" --timeout=180s
                if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    post {
        always {
            bat '''
            @echo off
            docker logout >nul 2>&1
            exit /b 0
            '''
        }
    }
}
