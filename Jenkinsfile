pipeline {
    agent {
        docker {
            image 'docker:20.10-dind'
            args '--privileged --user root -v /var/run/docker.sock:/var/run/docker.sock --gpus all --add-host=host.docker.internal:host-gateway -e DOCKER_TLS_CERTDIR=""'
            reuseNode true
        }
    }

    environment {
        DOCKER_IMAGE = "gayathri814/leukemia-segmentation"
        IMAGE_TAG = "v${BUILD_NUMBER}"
        SONAR_URL = "http://host.docker.internal:9000"
        GITHUB_REPO = "Leukemia-Image-Segmentation"
        GITHUB_USER = "Gay-123"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        url: "https://github.com/${env.GITHUB_USER}/${env.GITHUB_REPO}.git",
                        credentialsId: 'github'
                    ]]
                ])
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    apk add --no-cache python3 py3-pip git curl unzip openjdk11-jre
                    wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856.zip
                    unzip sonar-scanner-cli-4.8.0.2856.zip
                    rm sonar-scanner-cli-4.8.0.2856.zip
                    mv sonar-scanner-4.8.0.2856 /opt/sonar-scanner
                    ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=Leukemia-Image-Segmentation \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=$SONAR_URL \
                            -Dsonar.login=$SONAR_TOKEN \
                            -Dsonar.exclusions=static/**,templates/**,models/leukemiaSegmentation.py
                    '''
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                    '''
                }
            }
        }
        
stage('Update Deployment') {
    when {
        expression { fileExists("k8s/deployment.yml") }
    }
    environment {
        GIT_REPO_NAME = "Leukemia-Image-Segmentation"
        GIT_USER_NAME = "Gay-123"
    }
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'github_cred',
            usernameVariable: 'GIT_USER',
            passwordVariable: 'GITHUB_TOKEN'
        )]) {
            sh '''
                # Install git in the container (if not present)
                apk add --no-cache git || apt-get update && apt-get install -y git || yum install -y git
                
                # Configure git
                git config --global user.email "gayathrit726@gmail.com"
                git config --global user.name "Gayathri T"
                
                # Update deployment file
                sed -i "s|image: gayathri814/leukemia-segmentation:.*|image: gayathri814/leukemia-segmentation:v${BUILD_NUMBER}|g" k8s/deployment.yml
                
                # Commit and push changes
                git add k8s/deployment.yml
                git commit -m "Update image to version ${BUILD_NUMBER}" || echo "No changes to commit"
                git push https://${GIT_USER}:${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git HEAD:main
            '''
        }
    }
}    post {
        always {
            cleanWs()
        }
    }
}
