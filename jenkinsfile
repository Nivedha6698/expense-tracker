pipeline {
    agent {
        label 'docker-slave'
    }

    triggers {
        githubPush()   // Webhook trigger
    }

    environment {
        IMAGE_NAME = "flask-expense-app"
        DOCKERHUB_REPO = "your-dockerhub-username/flask-expense-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'feature/add-expense',
                    url: 'https://github.com/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Tests (SQLite Memory)') {
            steps {
                sh '''
                docker run --rm \
                    -e APP_ENV=test \
                    $IMAGE_NAME pytest
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker tag $IMAGE_NAME $DOCKERHUB_REPO:latest
                    docker push $DOCKERHUB_REPO:latest
                    '''
                }
            }
        }

        stage('Deploy using Docker Compose') {
            steps {
                withCredentials([
                    string(credentialsId: 'db-user', variable: 'DB_USER'),
                    string(credentialsId: 'db-pass', variable: 'DB_PASSWORD'),
                    string(credentialsId: 'db-host', variable: 'DB_HOST'),
                    string(credentialsId: 'db-name', variable: 'DB_NAME'),
                    string(credentialsId: 'jwt-secret', variable: 'JWT_SECRET_KEY')
                ]) {
                    sh '''
                    echo "Deploying application..."

                    export DB_USER=$DB_USER
                    export DB_PASSWORD=$DB_PASSWORD
                    export DB_HOST=$DB_HOST
                    export DB_NAME=$DB_NAME
                    export JWT_SECRET_KEY=$JWT_SECRET_KEY

                    docker-compose down || true
                    docker-compose up -d --build

                    docker ps
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build, Test & Deployment successful!"
        }
        failure {
            echo "❌ Pipeline failed. Deployment skipped."
        }
    }
}
