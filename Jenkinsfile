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
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_CREDENTIALS_USR',
                    passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW']]) {
                    
                    // Increase the timeout for this command
                    timeout(time: 5, unit: 'MINUTES') {
                        bat "echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin"
                    }
                }
            }
        }

        stage('Build and push Docker image') {
            steps {
                bat 'docker buildx build --push --tag wajidali05/my-image:latest .'
            }
        }

        stage('Pull and run Docker container') {
            steps {
                bat 'docker run -d --name my-container wajidali05/my-image:latest'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
