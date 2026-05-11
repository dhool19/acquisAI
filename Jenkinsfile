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
                withCredentials([
                    string(credentialsId: 'openai-api-key', variable: 'OPENAI_API_KEY'),
                    string(credentialsId: 'vite-api-url', variable: 'VITE_API_URL')
                ]) {
                    sh '''
                        cat > acquisai-backend/.env <<EOF
OPENAI_API_KEY=$OPENAI_API_KEY
EOF
                    '''

                    sh '''
                        cat > acquisai-frontend/.env <<EOF
VITE_API_URL=$VITE_API_URL
EOF
                    '''

                    sh 'docker compose down'
                    sh 'docker compose up --build -d'
                }
            }
        }
    }
}