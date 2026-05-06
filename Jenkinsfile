pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "munishd005/cicd-web-app"
        IMAGE_TAG  = "build-${BUILD_NUMBER}"
        GIT_USER   = "Munishd24"
        GIT_EMAIL  = "munishd1234@gmail.com"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push Image') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                        set -e
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Update K8S Manifest') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh """
                        set -e

                        git config user.name "${GIT_USER}"
                        git config user.email "${GIT_EMAIL}"

                        git fetch origin
                        git checkout main
                        git reset --hard origin/main

                        sed -i 's|image:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|' k8s/deployment.yml

                        git add k8s/deployment.yml

                        git diff --cached --quiet || git commit -m "Updated image to ${IMAGE_TAG}"

                        git push https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/Munishd24/Multi-Branch-Production.git main
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully"
        }

        failure {
            echo "Pipeline failed"
        }
    }
}
