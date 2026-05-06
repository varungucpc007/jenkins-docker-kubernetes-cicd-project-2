pipeline {
    agent any

    environment {
        IMAGE_NAME = "varungucpc007/flask-k8s-app"
        GIT_REPO   = "https://github.com/varungucpc007/jenkins-docker-kubernetes-cicd-project-2.git"
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
                    exit /b 0
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

                    echo Logging into Docker Hub...
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    if errorlevel 1 exit /b 1

                    echo Pushing build tag...
                    docker push %IMAGE_NAME%:%BUILD_NUMBER%
                    if errorlevel 1 exit /b 1

                    echo Tagging latest...
                    docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest
                    if errorlevel 1 exit /b 1

                    echo Pushing latest tag...
                    docker push %IMAGE_NAME%:latest
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
                    variable: 'KUBECONFIG'
                )]) {
                    bat '''
                    @echo off
                    set KUBECONFIG=%KUBECONFIG%

                    kubectl set image deployment/flask-app flask-app=%IMAGE_NAME%:%BUILD_NUMBER%
                    if errorlevel 1 exit /b 1

                    kubectl apply -f k8s\\service.yaml
                    if errorlevel 1 exit /b 1

                    exit /b 0
                    '''
                }
            }
        }
    }
}
