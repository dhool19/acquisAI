pipeline {
    agent any

    stages {

        stage('Install Backend') {
            steps {
                dir('acquisai-backend') {
                    sh 'python3 -m pip install -r requirements.txt --break-system-packages'
                }
            }
        }

        stage('Install Frontend') {
            steps {
                dir('acquisai-frontend') {
                    sh 'npm install'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('acquisai-frontend') {
                    sh 'npm run build'
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up --build -d'
            }
        }
    }
}