
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Medicine Expiry Alert System'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t mersineelakantam/medicine-expiry-alert:%BUILD_NUMBER% -t mersineelakantam/medicine-expiry-alert:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    bat 'echo %DOCKERHUB_TOKEN%| docker login -u %DOCKERHUB_USER% --password-stdin'
                    bat 'docker push mersineelakantam/medicine-expiry-alert:%BUILD_NUMBER%'
                    bat 'docker push mersineelakantam/medicine-expiry-alert:latest'
                    bat 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl set image deployment/medicine-app medicine-app=mersineelakantam/medicine-expiry-alert:%BUILD_NUMBER%'
                bat 'kubectl rollout status deployment/medicine-app --timeout=120s'
            }
        }
    }

    post {
        success {
            echo 'CI/CD completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
