pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m unittest discover -s tests -p "test_*.py"'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -f dockerfile -t task-alarm-reminder:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker stop task-alarm-app || exit 0'
                bat 'docker rm task-alarm-app || exit 0'
                bat 'docker run -d -p 5000:5000 --name task-alarm-app task-alarm-reminder:latest'
            }
        }
    }

    post {
        success {
            echo 'Task Alarm application deployed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}