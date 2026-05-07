pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    parameters {
        string(name: 'GIT_REPO', defaultValue: 'https://github.com/varungucpc007/jenkins-docker-kubernetes-cicd-project-2.git', description: 'Git repository URL')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch to build')
        string(name: 'IMAGE_NAME', defaultValue: 'varungucpc007/flask-k8s-app', description: 'Docker image name')
        string(name: 'APP_DIR', defaultValue: 'app', description: 'Folder containing Dockerfile')
        string(name: 'K8S_DIR', defaultValue: 'k8s', description: 'Folder containing Kubernetes YAML files')
        string(name: 'DEPLOYMENT_NAME', defaultValue: 'flask-app', description: 'Kubernetes deployment name')
        string(name: 'CONTAINER_NAME', defaultValue: 'flask-app', description: 'Kubernetes container name')
        string(name: 'KUBE_NAMESPACE', defaultValue: 'default', description: 'Kubernetes namespace')
        string(name: 'DOCKER_CREDENTIALS_ID', defaultValue: 'dockerhub-creds', description: 'Jenkins Docker Hub credential ID')
        string(name: 'KUBECONFIG_CREDENTIALS_ID', defaultValue: 'kubeconfig', description: 'Jenkins kubeconfig secret file credential ID')
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

                echo Building image %IMAGE_NAME%:%IMAGE_TAG% ...
                docker build -t "%IMAGE_NAME%:%IMAGE_TAG%" "%APP_DIR%"
                if errorlevel 1 exit /b 1

                docker tag "%IMAGE_NAME%:%IMAGE_TAG%" "%IMAGE_NAME%:latest"
                if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${params.DOCKER_CREDENTIALS_ID}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                    @echo off
                    setlocal

                    echo Logging into Docker registry...
                    powershell -NoProfile -NonInteractive -Command "$env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin; exit $LASTEXITCODE"
                    if errorlevel 1 exit /b 1

                    echo Pushing image %IMAGE_NAME%:%IMAGE_TAG% ...
                    docker push "%IMAGE_NAME%:%IMAGE_TAG%"
                    if errorlevel 1 exit /b 1

                    echo Pushing image %IMAGE_NAME%:latest ...
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
                    credentialsId: "${params.KUBECONFIG_CREDENTIALS_ID}",
                    variable: 'KUBECONFIG_FILE'
                )]) {
                    bat '''
                    @echo off
                    setlocal
                    set "KUBECONFIG=%KUBECONFIG_FILE%"

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

                    echo Applying Kubernetes manifests...
                    kubectl apply -n "%KUBE_NAMESPACE%" -f "%K8S_DIR%\\deployment.yaml"
                    if errorlevel 1 exit /b 1

                    kubectl apply -n "%KUBE_NAMESPACE%" -f "%K8S_DIR%\\service.yaml"
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
            echo "SUCCESS: ${params.IMAGE_NAME}:${env.IMAGE_TAG} deployed to namespace ${params.KUBE_NAMESPACE}"
        }
        failure {
            echo 'FAILED: open the failed stage logs in Jenkins to see the exact command error.'
        }
    }
}
