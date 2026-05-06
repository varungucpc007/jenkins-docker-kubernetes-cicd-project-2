pipeline {
    agent any

    environment {
        IMAGE_NAME = "varungucpc007/flask-k8s-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/varungucpc007/jenkins-docker-kubernetes-cicd-project-2.git'
            }
        }

        stage('Build Docker Image') {
    steps {
        dir('app') {
            bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
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
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE_NAME:$BUILD_NUMBER
                    docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest
                    docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                    sed -i "s|varungucpc007/flask-k8s-app:latest|$IMAGE_NAME:$BUILD_NUMBER|g" k8s/deployment.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    '''
                }
            }
        }
    }
}
