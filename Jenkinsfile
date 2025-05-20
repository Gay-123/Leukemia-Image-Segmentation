pipeline {
  agent {
    docker {
      image 'gayathri814/leukemia-segmentation:v1'  // YOUR PRE-BUILT IMAGE
      args '--user root -v /var/run/docker.sock:/var/run/docker.sock --gpus all'  // GPU access
    }
  }

  environment {
    DOCKER_IMAGE = "gayathri814/leukemia-segmentation"
    IMAGE_TAG = "v${BUILD_NUMBER}"
    SONAR_URL = "http://your-sonarqube-server:9000"  // UPDATE THIS
  }

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main',
            url: 'https://github.com/Gay-123/Leukemia-Image-Segmentation.git',
            credentialsId: 'github-creds'  // ADD YOUR CREDENTIALS ID
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          python -m pytest tests/ --cov=app --cov-report=xml
        '''
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_TOKEN')]) {
          sh """
            sonar-scanner \
              -Dsonar.projectKey=Leukemia-Image-Segmentation \
              -Dsonar.sources=. \
              -Dsonar.host.url=${SONAR_URL} \
              -Dsonar.login=${SONAR_TOKEN} \
              -Dsonar.python.coverage.reportPaths=coverage.xml
          """
        }
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        script {
          // Build using the same pre-built image as base
          sh """
            docker build \
              -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
              -t ${DOCKER_IMAGE}:latest \
              .
          """
          
          // Push with Docker Hub credentials
          withCredentials([usernamePassword(
            credentialsId: 'dockerhub-creds',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh """
              echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
              docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
              docker push ${DOCKER_IMAGE}:latest
            """
          }
        }
      }
    }

    stage('Update K8s Manifests') {
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          sh '''
            git config --global user.email "gayathrit726@gmail.com"
            git config --global user.name "Jenkins CI"
            
            # Update image tag in deployment
            sed -i "s|image:.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|g" k8s/deployment.yml
            
            git add k8s/deployment.yml
            git commit -m "CI: Update image to ${IMAGE_TAG}"
            git push "https://${GITHUB_TOKEN}@github.com/Gay-123/Leukemia-Image-Segmentation.git" HEAD:main
          '''
        }
      }
    }
  }

  post {
    always {
      cleanWs()  // Clean workspace
    }
    success {
      slackSend(color: 'good', message: "✅ Pipeline SUCCESS: ${env.BUILD_URL}")
    }
    failure {
      slackSend(color: 'danger', message: "❌ Pipeline FAILED: ${env.BUILD_URL}")
    }
  }
}
