pipeline {
    agent {
        label 'docker-slave'
    }

    environment {
        IMAGE_NAME = "flask-expense-app-dev"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'dev',
                    url: 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Run Tests (SQLite - APP_ENV=test)') {
            steps {
                sh '''
                echo "Running tests with SQLite..."

                docker build -t $IMAGE_NAME:test .

                docker run --rm \
                    -e APP_ENV=test \
                    $IMAGE_NAME:test pytest
                '''
            }
        }

        stage('Build Docker Image (Dev)') {
            steps {
                sh '''
                echo "Building Docker image..."

                docker build -t $IMAGE_NAME:latest .
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Dev Pipeline Successful (Build + Test Passed)"
        }
        failure {
            echo "❌ Dev Pipeline Failed - Fix before merging to main"
        }
    }
}