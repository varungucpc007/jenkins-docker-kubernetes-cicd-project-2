pipeline {
    agent any

    environment {
        IMAGE_NAME = "varungucpc007/flask-k8s-app"
        GIT_REPO = "https://github.com/varungucpc007/jenkins-docker-kubernetes-cicd-project-2.git"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    bat '''
                    @echo off
                    docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .
                    if errorlevel 1 exit /b 1
                    '''
                }
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

                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    if errorlevel 1 exit /b 1

                    docker push %IMAGE_NAME%:%BUILD_NUMBER%
                    if errorlevel 1 exit /b 1

                    docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest
                    if errorlevel 1 exit /b 1

                    docker push %IMAGE_NAME%:latest
                    if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(
                    credentialsId: 'kubeconfig',
                    variable: 'KUBECONFIG'
                )]) {
                    bat '''
                    @echo off
                    set KUBECONFIG=%KUBECONFIG%

                    kubectl set image deployment/flask-app flask-app=%IMAGE_NAME%:%BUILD_NUMBER%
                    if errorlevel 1 exit /b 1

                    kubectl apply -f k8s\\service.yaml
                    if errorlevel 1 exit /b 1
                    '''
                }
            }
        }
    }
}
