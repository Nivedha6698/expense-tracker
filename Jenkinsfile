pipeline {
    agent {
        label 'docker'
    }

    triggers {
        githubPush()   // Webhook trigger
    }

    environment {
        IMAGE_NAME = "flask-expense-app"
        DOCKERHUB_REPO = "nivedhajd/flask-expense-tracker"
        CONTAINER_NAME = "flask-expense-app"
        IMAGE_TAG = "v${BUILD_NUMBER}"
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
		stage('Cleanup Test Artifacts') {
            steps {
                sh '''
                echo "Cleaning test containers/images..."

                docker container prune -f || true
                docker image prune -f || true
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
                    # Tagging
                    docker tag $IMAGE_NAME:latest $DOCKERHUB_REPO:latest
                    docker tag $IMAGE_NAME:latest $DOCKERHUB_REPO:v${BUILD_NUMBER}

                    # Pushing
                    docker push $DOCKERHUB_REPO:latest
                    docker push $DOCKERHUB_REPO:v${BUILD_NUMBER}
                    '''
                }
            }
        }
		stage('Stop Existing Container') {
            steps {
                sh '''
                echo "Stopping old container if exists..."

                docker rm -f $CONTAINER_NAME || true
                '''
            }
        }


        stage('Deploy using Docker Compose') {
            steps {
                withCredentials([
                    string(credentialsId: 'db-user', variable: 'DB_USER'),
                    string(credentialsId: 'db-pass', variable: 'DB_PASSWORD'),
                    string(credentialsId: 'db-host', variable: 'DB_HOST'),
                    string(credentialsId: 'db-name', variable: 'DB_NAME'),
                    string(credentialsId: 'jwt-secret', variable: 'JWT_SECRET_KEY'),
					string(credentialsId: 'aws-bucket', variable: 'AWS_BUCKET_NAME'),
					string(credentialsId: 'aws-region', variable: 'AWS_REGION')
					
                ]) {
                    sh '''
                    echo "Deploying application..."

                    export IMAGE_TAG=V${BUILD_NUMBER}
                    export DB_USER=$DB_USER
                    export DB_PASSWORD=$DB_PASSWORD
                    export DB_HOST=$DB_HOST
                    export DB_NAME=$DB_NAME
                    export JWT_SECRET_KEY=$JWT_SECRET_KEY
					export AWS_BUCKET_NAME=$AWS_BUCKET_NAME
					export AWS_REGION=$AWS_REGION

                    docker-compose down || true
                    docker-compose up -d 

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
