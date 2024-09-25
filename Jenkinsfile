pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout repository') {
            steps {
                checkout scm
            }
        }

        stage('Set up Docker Buildx') {
            steps {
                sh '''
                    # Install Docker Buildx plugin
                    docker buildx install
                    docker buildx create --use
                '''
            }
        }

        stage('Log in to Docker Hub') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                '''
            }
        }

        stage('Build and push Docker image') {
            steps {
                sh '''
                    docker buildx build --push --file Dockerfile --tag $DOCKERHUB_CREDENTIALS_USR/house-price-predictor:latest .
                '''
            }
        }

        stage('Pull and run Docker container') {
            steps {
                sh '''
                    docker pull $DOCKERHUB_CREDENTIALS_USR/house-price-predictor:latest
                    docker run -d -p 5000:5000 $DOCKERHUB_CREDENTIALS_USR/house-price-predictor:latest
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
