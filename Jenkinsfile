pipeline {
    agent any
    
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        
        stage('Debug Docker') {
            steps {
                bat 'docker --version'
                bat 'docker info'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo Docker User: %DOCKER_USER%'
                    // Do not echo the password
                }
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
                    bat '''
                        echo Attempting to log in to Docker Hub
                        docker login -u %DOCKER_USER% --password %DOCKER_PASS%
                        if %ERRORLEVEL% NEQ 0 (
                            echo Docker login failed
                            exit /b 1
                        )
                    '''
                }
            }
        }
        
        stage('Build and push Docker image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat 'docker build -t %DOCKER_USER%/my-app:latest .'
                        bat 'docker push %DOCKER_USER%/my-app:latest'
                    }
                }
            }
        }
        
        stage('Pull and run Docker container') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat 'docker pull %DOCKER_USER%/my-app:latest'
                        bat 'docker run -d -p 8080:80 %DOCKER_USER%/my-app:latest'
                    }
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
