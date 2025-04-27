pipeline {
    agent {
        docker {
            image 'gayathri814/leukemia-segmentation:final'  // Your custom Docker image
            args '-v /var/run/docker.sock:/var/run/docker.sock'  // Docker socket for Docker-in-Docker usage
        }
    }

    stages {
        stage('Checkout') {
            steps {
                sh 'echo Checkout passed'
                git branch: 'main', url: 'https://github.com/Gay-123/Leukemia-Image-Segmentation.git'
            }
        }

        stage('Build & Test') {
            steps {
                sh 'ls -ltr'  // Listing files to confirm workspace
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt  // Installing dependencies
                    pytest tests/ || echo "No tests yet"  // Running tests (if any)
                '''
            }
        }

        stage('Static Code Analysis') {
            environment {
                SONAR_URL = "http://localhost:9000"  // Replace with your SonarQube URL
            }
            steps {
                withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_AUTH_TOKEN')]) {
                    sh '''
                        pip install sonar-scanner-cli  // Installing SonarQube scanner
                        sonar-scanner \
                            -Dsonar.projectKey=leukemia_segmentation \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN}  // Running static analysis with SonarQube
                    '''
                }
            }
        }

        stage('Build & Push Docker Image') {
            environment {
                DOCKER_IMAGE = "gayathri814/leukemia-segmentation:${BUILD_NUMBER}"  // Dynamic Docker image tag
                REGISTRY_CREDENTIALS = credentials('docker-cred')  // Docker credentials from Jenkins
            }
            steps {
                script {
                    // Build Docker image if not pre-built
                    docker.build("${DOCKER_IMAGE}")  // Build the Docker image first

                    // Pushing the built Docker image to Docker Hub
                    docker.withRegistry('https://index.docker.io/v1/', REGISTRY_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE}").push()  // Push the image to Docker Hub
                    }
                }
            }
        }

        stage('Update Kubernetes manifests') {
            environment {
                GIT_REPO_NAME = "Leukemia-Image-Segmentation"
                GIT_USER_NAME = "Gay-123"
            }
            steps {
                withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        git config user.email "gayathrit726@gmail.com"  // Configuring git user email
                        git config user.name "Gay-123"  // Configuring git user name

                        // Replace the image tag in the Kubernetes deployment file
                        sed -i "s/final/${BUILD_NUMBER}/g" k8s/deployment.yml

                        git add k8s/deployment.yml  // Staging the Kubernetes deployment file
                        git commit -m "Update image tag to ${BUILD_NUMBER} in deployment"  // Committing the changes
                        git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git HEAD:main  // Pushing the changes
                    '''
                }
            }
        }
    }
}
