
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'scniranjan/aws-devops-cicd'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'GitHub source code downloaded'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest -f docker/Dockerfile .'
            }
        }

        stage('Test Application') {
            steps {
                bat 'docker rm -f aws-devops-ci-test 2>NUL || exit /B 0'

                bat 'docker run -d --name aws-devops-ci-test -p 5001:5000 %IMAGE_NAME%:%BUILD_NUMBER%'

                bat 'timeout /t 5 /nobreak >NUL'

                bat '''powershell -NoProfile -Command "$r = Invoke-RestMethod http://localhost:5001/health; if ($r.status -ne 'Healthy') { exit 1 }"'''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat 'echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USER% --password-stdin'

                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'

                    bat 'docker push %IMAGE_NAME%:latest'

                    bat 'docker logout'
                }
            }
        }
    }

    post {
        always {
            bat 'docker rm -f aws-devops-ci-test 2>NUL || exit /B 0'
        }

        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed. Check console output.'
        }
    }
}
