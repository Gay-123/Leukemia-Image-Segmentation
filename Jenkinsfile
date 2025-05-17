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
    withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_AUTH_TOKEN')]) {
      sh '''
        # Install missing dependencies (unzip + file)
        apt-get update && apt-get install -y unzip file || echo "Warning: apt-get failed (non-fatal)"

        # Download SonarQube Scanner (verified URL)
        curl -Lo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip

        # Basic file check (since 'file' command may not be available)
        if [ -f sonar-scanner.zip ]; then
          echo "SonarQube Scanner downloaded successfully."
          ls -lh sonar-scanner.zip
        else
          echo "Error: Failed to download sonar-scanner.zip"
          exit 1
        fi

        # Unzip and run SonarQube Scanner
        unzip sonar-scanner.zip || { echo "Unzip failed"; exit 1; }
        export PATH=$PATH:$PWD/sonar-scanner-*/bin
        sonar-scanner \
          -Dsonar.projectKey=Leukemia-Segmentation \
          -Dsonar.sources=. \
          -Dsonar.host.url=${SONAR_URL} \
          -Dsonar.login=${SONAR_AUTH_TOKEN}
      '''
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
