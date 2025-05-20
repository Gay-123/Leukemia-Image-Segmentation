pipeline {
  agent {
    docker {
      image 'docker:20.10-dind'  // Official Docker image with Docker installed
      args '--privileged --user root -v /var/run/docker.sock:/var/run/docker.sock --gpus all --add-host=host.docker.internal:host-gateway'
      reuseNode true
    }
  }

  environment {
    DOCKER_IMAGE = "gayathri814/leukemia-segmentation"
    IMAGE_TAG = "v${BUILD_NUMBER}"
    SONAR_URL = "http://host.docker.internal:9000"
  }

  stages {
    stage('Checkout Code') {
      steps {
        script {
          // First try with credentials, fallback to anonymous if credentials not found
          try {
            checkout([
              $class: 'GitSCM',
              branches: [[name: 'main']],
              extensions: [],
              userRemoteConfigs: [[
                url: 'https://github.com/Gay-123/Leukemia-Image-Segmentation.git',
                credentialsId: 'github'
              ]]
            ])
          } catch (Exception e) {
            echo "Failed to checkout with credentials, trying anonymously"
            checkout scm
          }
        }
      }
    }

    stage('Setup Environment') {
      steps {
        sh '''
          # Install required tools
          apk add --no-cache python3 py3-pip git curl unzip openjdk11-jre
          
          # Install SonarScanner using the official method for Alpine
          wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856.zip
          unzip sonar-scanner-cli-4.8.0.2856.zip
          rm sonar-scanner-cli-4.8.0.2856.zip
          mv sonar-scanner-4.8.0.2856 /opt/sonar-scanner
          ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner
          
          # Verify installations
          docker --version
          sonar-scanner --version
        '''
      }
    }
    
    stage('SonarQube Analysis') {
      steps {
        withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_TOKEN')]) {
          sh """
            export SONAR_SCANNER_OPTS="-Xmx512m"
            sonar-scanner \
              -Dsonar.projectKey=Leukemia-Image-Segmentation \
              -Dsonar.sources=. \
              -Dsonar.host.url=${SONAR_URL} \
              -Dsonar.login=${SONAR_TOKEN} \
              -Dsonar.exclusions=static/**,templates/**,models/leukemiaSegmentation.py \
              -Dsonar.python.version=3.10
          """
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
          sh """
            # Build Docker image
            docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -f Dockerfile .
            
            # Login to Docker Hub
            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
            
            # Push image
            docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Update K8s Deployment with New Image Tag') {
      when {
        expression { fileExists("k8's/deployment.yml") }
      }
      steps {
        script {
          // Use the same image name and tag from environment variables
          withCredentials([
            usernamePassword(
              credentialsId: 'github-userpass', 
              usernameVariable: 'GIT_USER',
              passwordVariable: 'GIT_PASS'
            )
          ]) {
            sh """
              # Configure Git
              git config --global user.email "gayathrit726@gmail.com"
              git config --global user.name "Jenkins CI"

              # Update the Deployment YAML with the new image tag
              sed -i "s|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|g" k8s/deployment.yml

              # Commit and push changes
              git add k8s/deployment.yml
              git commit -m "CI: Updated image tag to ${IMAGE_TAG}" || echo "No changes to commit"
              git push https://${GIT_USER}:${GIT_PASS}@github.com/Gay-123/Leukemia-Image-Segmentation.git HEAD:main
            """
          }
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
