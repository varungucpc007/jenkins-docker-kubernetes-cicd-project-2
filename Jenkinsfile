pipeline {
    agent any

    environment {
        IMAGE_NAME = 'varungucpc007/flask-k8s-app'
        GIT_REPO   = 'https://github.com/varungucpc007/jenkins-docker-kubernetes-cicd-project-2.git'
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                @echo off
                docker version
                if errorlevel 1 exit /b 1

                docker build -t "%IMAGE_NAME%:%BUILD_NUMBER%" app
                if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                    @echo off
                    echo Logging into Docker Hub...

                    powershell -NoProfile -NonInteractive -Command "$env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin; exit $LASTEXITCODE"
                    if errorlevel 1 exit /b 1

                    docker tag "%IMAGE_NAME%:%BUILD_NUMBER%" "%IMAGE_NAME%:latest"
                    if errorlevel 1 exit /b 1

                    docker push "%IMAGE_NAME%:%BUILD_NUMBER%"
                    if errorlevel 1 exit /b 1

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
                withCredentials([file(
                    credentialsId: 'kubeconfig',
                    variable: 'KUBECONFIG_FILE'
                )]) {
                    bat '''
                    @echo off
                    set "KUBECONFIG=%KUBECONFIG_FILE%"

                    kubectl apply -f k8s\\deployment.yaml
                    if errorlevel 1 exit /b 1

                    kubectl apply -f k8s\\service.yaml
                    if errorlevel 1 exit /b 1

                    kubectl set image deployment/flask-app flask-app="%IMAGE_NAME%:%BUILD_NUMBER%"
                    if errorlevel 1 exit /b 1

                    kubectl rollout status deployment/flask-app --timeout=180s
                    if errorlevel 1 exit /b 1
                    '''
                }
            }
        }
    }
}
