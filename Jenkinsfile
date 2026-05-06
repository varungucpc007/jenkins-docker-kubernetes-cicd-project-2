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
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: env.GIT_REPO]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                @echo off
                if not exist "app\\Dockerfile" (
                    echo ERROR: app\\Dockerfile not found.
                    exit /b 1
                )

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
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    bat '''
                    @echo off
                    echo Logging into Docker Hub...
                    powershell -NoProfile -NonInteractive -Command "$env:DOCKERHUB_PASS | docker login -u $env:DOCKERHUB_USER --password-stdin; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }"
                    if errorlevel 1 exit /b 1

                    echo Tagging latest...
                    docker tag "%IMAGE_NAME%:%BUILD_NUMBER%" "%IMAGE_NAME%:latest"
                    if errorlevel 1 exit /b 1

                    echo Pushing build tag...
                    docker push "%IMAGE_NAME%:%BUILD_NUMBER%"
                    if errorlevel 1 exit /b 1

                    echo Pushing latest tag...
                    docker push "%IMAGE_NAME%:latest"
                    if errorlevel 1 exit /b 1

                    docker logout >nul 2>&1
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

                    kubectl version --client
                    if errorlevel 1 exit /b 1

                    if not exist "k8s\\deployment.yaml" (
                        echo ERROR: k8s\\deployment.yaml not found.
                        exit /b 1
                    )

                    if not exist "k8s\\service.yaml" (
                        echo ERROR: k8s\\service.yaml not found.
                        exit /b 1
                    )

                    kubectl apply -f "k8s\\deployment.yaml"
                    if errorlevel 1 exit /b 1

                    kubectl apply -f "k8s\\service.yaml"
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

    post {
        always {
            bat '''
            @echo off
            docker logout >nul 2>&1
            exit /b 0
            '''
        }
        success {
            echo "Pipeline completed successfully. Image: ${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
        }
        failure {
            echo 'Pipeline failed. Check the stage log above for the exact command that failed.'
        }
    }
}
