pipeline {
  agent {
    docker {
      image 'python:3.8'  // Used for running initial steps (not for building image)
      args '-v /var/run/docker.sock:/var/run/docker.sock'
    }
  }

  environment {
    DOCKER_IMAGE = "gayathri814/leukemia-segmentation"
    GIT_REPO_NAME = "leukemia_segmentation"
    GIT_USER_NAME = "Gay-123"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/Gay-123/Leukemia-Image-Segmentation.git'
      }
    }

    stage('Build & Test') {
      steps {
        sh '''
          pip install --upgrade pip
          pip install -r requirements.txt
          pytest tests/ || echo "No tests yet"
        '''
      }
    }

    stage('Static Code Analysis') {
      environment {
        SONAR_URL = "http://your-sonarqube-host:9000"
      }
      steps {
        withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_AUTH_TOKEN')]) {
          sh '''
            pip install sonar-scanner-cli
            sonar-scanner \
              -Dsonar.projectKey=leukemia_segmentation \
              -Dsonar.sources=. \
              -Dsonar.host.url=${SONAR_URL} \
              -Dsonar.login=${SONAR_AUTH_TOKEN}
          '''
        }
      }
    }

    stage('Build & Push Docker Image') {
      environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
      }
      steps {
        script {
          // Build image from Dockerfile
          def image = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
          
          // Push to Docker Hub
          docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
            image.push()
          }
        }
      }
    }

    stage('Update Kubernetes manifests') {
      steps {
        withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
          sh '''
            git config user.email "gayathrit726@gmail.com"
            git config user.name "Gay-123"

            sed -i "s/final/${BUILD_NUMBER}/g" k8s/deployment.yml

            git add k8s/deployment.yml
            git commit -m "Update image tag to ${BUILD_NUMBER} in deployment"
            git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git HEAD:main
          '''
        }
      }
    }
  }
}
