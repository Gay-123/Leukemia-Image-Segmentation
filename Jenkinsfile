pipeline {
  agent {
    docker {
      image 'gayathri814/leukemia-segmentation:v1.0' // Make sure this image has Python, pip, Git, Docker CLI, etc.
      args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
    }
  }

  environment {
    DOCKER_IMAGE = "gayathri814/leukemia-segmentation"
    IMAGE_TAG = "${BUILD_NUMBER}"
    SONAR_URL = "http://localhost:9000"
    GIT_REPO_NAME = "Leukemia-Image-Segmentation"
    GIT_USER_NAME = "Gay-123"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/Gay-123/Leukemia-Image-Segmentation.git'
      }
    }

    stage('Install Dependencies & Test') {
      steps {
        sh '''
          python3 -m pip install --upgrade pip
          pip install -r requirements.txt
          if [ -d "tests" ]; then
            pytest tests/
          else
            echo "No tests found"
          fi
        '''
      }
    }

stage('Static Code Analysis') {
  steps {
    script {
      // Use this special DNS name that works in Docker containers
      def sonarUrl = 'http://host.docker.internal:9000' 
      
      // Quick health check (no waiting loop needed)
      sh "curl -I --connect-timeout 5 ${sonarUrl} || echo 'SonarQube check skipped'"
      
      // Run analysis directly
      withCredentials([string(credentialsId: 'SONAR_AUTH_TOKEN', variable: 'SONAR_TOKEN'])]) {  // Fixed: Added missing parenthesis
        sh """
          ./sonar-scanner-*/bin/sonar-scanner \
            -Dsonar.host.url=${sonarUrl} \
            -Dsonar.login=${SONAR_TOKEN} \
            -Dsonar.projectKey=Leukemia-Segmentation
        """
      }
    }
  }
}
   stage('Build & Push Docker Image') {
      steps {
        script {
          def image = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
          docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
            image.push()
          }
        }
      }
    }

    stage('Update Kubernetes Manifests and Push') {
      steps {
        withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
          sh '''
            git config user.email "gayathrit726@gmail.com"
            git config user.name "${GIT_USER_NAME}"

            # Replace tag 'final' with current build number
            sed -i "s/final/${IMAGE_TAG}/g" k8s/deployment.yml

            # Commit only if there is a change
            git diff --quiet k8s/deployment.yml || {
              git add k8s/deployment.yml
              git commit -m "Update image tag to ${IMAGE_TAG} in deployment"
              git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git HEAD:main
            }
          '''
        }
      }
    }
  }

  post {
    success {
      echo '✅ Pipeline completed successfully.'
    }
    failure {
      echo '❌ Pipeline failed. Check the logs above.'
    }
  }
}
