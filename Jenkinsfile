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

        stage('Deploy') {
            steps {
                sh '''
                    echo "🚀 Deploying application..."
                    kubernetesDeploy(configs: "deploymentservice.yml", kubeconfigId: "kubernetes")
                '''
            }
        }
    }

    post {
        always {
            node {
                echo "🧹 Cleaning up..."
                sh 'docker image prune -f || true'
            }
        }
    }
}
