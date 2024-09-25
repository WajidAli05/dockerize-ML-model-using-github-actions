pipeline {
    agent any
    
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        
        stage('Debug Environment') {
            steps {
                bat 'echo PATH: %PATH%'
                bat 'echo JAVA_HOME: %JAVA_HOME%'
                bat 'java -version'
                bat 'echo Jenkins workspace: %WORKSPACE%'
            }
        }
        
        stage('Debug Docker') {
            steps {
                bat 'docker --version'
                bat 'docker info'
                bat 'echo Docker config location: %USERPROFILE%\\.docker\\config.json'
                bat 'if exist %USERPROFILE%\\.docker\\config.json (echo Docker config exists) else (echo Docker config not found)'
            }
        }
        
        stage('Set up Docker Buildx') {
            steps {
                bat 'docker buildx install || echo Docker buildx already installed'
                bat 'docker buildx create --use || echo Docker buildx already set up'
            }
        }
        
        stage('Log in to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        echo Attempting to log in as %DOCKER_USER%
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin || (echo Docker login failed && exit /b 1)
                    '''
                }
            }
        }
        
        stage('Build and push Docker image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat 'docker build -t %DOCKER_USER%/my-app:latest .'
                        bat 'docker push %DOCKER_USER%/my-app:latest || (echo Docker push failed && exit /b 1)'
                    }
                }
            }
        }
        
        stage('Pull and run Docker container') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat 'docker pull %DOCKER_USER%/my-app:latest'
                        bat 'docker run -d -p 8080:80 %DOCKER_USER%/my-app:latest || (echo Docker run failed && exit /b 1)'
                    }
                }
            }
        }
    }
    
    post {
        always {
            bat 'docker logout || echo "No previous session to log out from."'
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'The pipeline failed. Please check the logs for details.'
        }
    }
}
