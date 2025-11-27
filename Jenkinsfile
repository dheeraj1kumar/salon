pipeline {
    agent any

    stages {
        stage('Code') {
            steps {
                git url: "https://github.com/dheeraj1kumar/salon.git", branch: "main"
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "🛠️ Building Docker image..."
                    docker build -t salon-web-app:latest .
                '''
            }
        }

        stage("Push To DockerHub") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "dockerhub",
                    usernameVariable: "dockerHubUser",
                    passwordVariable: "dockerHubPass"
                )]) {
                    sh '''
                        echo $dockerHubPass | docker login -u $dockerHubUser --password-stdin
                        docker image tag salon-web-app:latest $dockerHubUser/salon-web-app:latest
                        docker push $dockerHubUser/salon-web-app:latest
                    '''
                }
            }
        }

  stage('DB Update') {
    steps {
        echo "🔧 Running Django migrations before deployment..."

        sh '''
            set -e

            if [ ! -f docker-compose.yml ]; then
                echo "❌ docker-compose.yml not found!"
                exit 1
            fi

            echo "📦 Starting DB service..."
            docker-compose up -d db

            echo "⏳ Waiting for PostgreSQL to become ready..."
            sleep 10

            echo "🚀 Running Django migrations inside container..."
            docker-compose run --rm web sh -c "
                python manage.py makemigrations &&
                python manage.py migrate
            "

            echo "✅ Database successfully migrated."
        '''
    }
}


        stage('Deploy') {
            steps {
                sh '''
                    echo "🚀 Deploying application..."
                    docker-compose down
                    docker-compose up -d
                '''
            }
        }
    }

    post {
        always {
            echo "🧹 Cleaning up..."
            sh 'docker image prune -f || true'
        }
    }
}
