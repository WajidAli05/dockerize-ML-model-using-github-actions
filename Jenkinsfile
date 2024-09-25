pipeline {
    agent any
    
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        
        stage('Set up Docker Buildx') {
            steps {
                bat 'docker buildx install'
                bat 'docker buildx create --use'
            }
        }
        
        stage('Log in to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                }
            }
        }
        
        stage('Build and push Docker image') {
            steps {
                script {
                    bat 'docker build -t wajidali05/my-app:latest .'
                    bat 'docker push wajidali05/my-app:latest'
                }
            }
        }
        
        stage('Pull and run Docker container') {
            steps {
                script {
                    bat 'docker pull wajidali05/my-app:latest'
                    bat 'docker run -d -p 8080:80 wajidali05/my-app:latest'
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            echo 'The pipeline failed. Check the logs for details.'
        }
    }
}