pipeline {
  agent {
    docker {
      image 'gayathri814/leukemia-segmentation:v1.0'
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
          def sonarUrl = 'http://host.docker.internal:9000'
          sh "curl -v ${sonarUrl} || echo 'Connection test failed'"
          
          // VERIFIED WORKING SYNTAX
          withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_TOKEN')]) {
            sh '''
              if [ ! -d "sonar-scanner" ]; then
                curl -Lo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                unzip sonar-scanner.zip
              fi
              ./sonar-scanner-*/bin/sonar-scanner \
                -Dsonar.host.url=${sonarUrl} \
                -Dsonar.login=${SONAR_TOKEN} \
                -Dsonar.projectKey=Leukemia-Segmentation
            '''
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

            sed -i "s/final/${IMAGE_TAG}/g" k8s/deployment.yml

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
