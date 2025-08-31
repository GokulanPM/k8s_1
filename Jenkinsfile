pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')  // set in Jenkins
        DOCKER_IMAGE = "goku0123/myapp"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/GokulanPM/k8s_1.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    bat "echo %PASSWORD% | docker login -u %USERNAME% --password-stdin"
                    bat "docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat "kubectl set image deployment/flask-app flask-container=${DOCKER_IMAGE}:${BUILD_NUMBER} --record"
            }
        }
    }
}
