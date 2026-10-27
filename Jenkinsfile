
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Medicine Expiry Alert System - CI/CD'
                echo 'Code checked out from GitHub'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker --version'
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
    }

    post {
        success {
            echo 'Docker image built and pushed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output.'
        }
    }
}
