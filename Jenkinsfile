pipeline {
  agent {
    docker {
      image 'gayathri814/leukemia-segmentation:v1'
      args '--user root -v /var/run/docker.sock:/var/run/docker.sock --gpus all --add-host=host.docker.internal:host-gateway'
    }
  }

  environment {
    DOCKER_IMAGE = "gayathri814/leukemia-segmentation"
    IMAGE_TAG = "v${BUILD_NUMBER}"
    // Use Docker's special hostname to access host services
    SONAR_URL = "http://host.docker.internal:9000"
  }

  stages {
    stage('Checkout Code') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
          sh """
            git clone https://${GIT_USER}:${GIT_PASS}@github.com/Gay-123/Leukemia-Image-Segmentation.git .
            git checkout main
          """
        }
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
              -Dsonar.exclusions=static/**,templates/** \
              -Dsonar.python.version=3.10
          """
        }
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'docker-cred',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh """
            docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -f Dockerfile .
            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
            docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Update K8s Manifests') {
      when {
        expression { fileExists('k8s/deployment.yml') }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
          sh """
            git config --global user.email "gayathrit726@gmail.com"
            git config --global user.name "Jenkins CI"
            sed -i "s|image:.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|g" k8s/deployment.yml
            git add k8s/deployment.yml
            git commit -m "CI: Update image to ${IMAGE_TAG}" || echo "No changes to commit"
            git push https://${GIT_USER}:${GIT_PASS}@github.com/Gay-123/Leukemia-Image-Segmentation.git HEAD:main
          """
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
