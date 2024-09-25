pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Fetch credentials from Jenkins
    }
    stages {
        stage('Checkout SCM') {
            steps {
                // Checkout the repository
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
                script {
                    // Logging into Docker Hub using access token as password
                    bat """
                    echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin
                    """
                }
            }
        }
        stage('Build and push Docker image') {
            steps {
                script {
                    // Build the Docker image and push to Docker Hub
                    bat """
                    docker build -t wajidali05/my-app:latest .
                    docker push wajidali05/my-app:latest
                    """
                }
            }
        }
        stage('Pull and run Docker container') {
            steps {
                script {
                    // Pull and run the Docker container
                    bat """
                    docker pull wajidali05/my-app:latest
                    docker run -d -p 8080:80 wajidali05/my-app:latest
                    """
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
