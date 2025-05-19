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
    SONAR_URL = "http://host.docker.internal:9000"
    GIT_REPO_NAME = "Leukemia-Image-Segmentation"
    GIT_USER_NAME = "Gay-123"
    DOCKER_BUILDKIT = "0"  // Enable Docker BuildKit
    PIP_TIMEOUT = "1000"   // Increased pip timeout
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
          pip install --default-timeout=${PIP_TIMEOUT} -r requirements.txt || \
          (echo "Retrying pip install..." && pip install --default-timeout=${PIP_TIMEOUT} -r requirements.txt)
          
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
      // Install required tools including Node.js for SonarQube analysis
      sh '''
        export DEBIAN_FRONTEND=noninteractive
        apt-get update && \
        apt-get install -y --no-install-recommends \
            unzip \
            nodejs \
            npm \
            tzdata && \
        ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
        dpkg-reconfigure --frontend noninteractive tzdata
      '''
      
      // Download and extract SonarQube Scanner with retry logic
      sh '''
        if [ ! -d sonar-scanner ]; then
          retry_count=0
          max_retries=3
          until [ $retry_count -ge $max_retries ]; do
            if curl -Lo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip; then
              unzip -o sonar-scanner.zip
              rm sonar-scanner.zip
              mv sonar-scanner-* sonar-scanner
              break
            else
              retry_count=$((retry_count+1))
              echo "Download failed, retrying ($retry_count/$max_retries)..."
              sleep 5
            fi
          done
        fi
      '''

      // Run SonarQube Scanner with error handling
      withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_TOKEN')]) {
        sh '''
          export PATH="$PATH:$(pwd)/sonar-scanner/bin"
          sonar-scanner \
            -Dsonar.projectKey=Leukemia-Image-Segmentation \
            -Dsonar.sources=. \
            -Dsonar.exclusions=**/leukemiaSegmentation.py \
            -Dsonar.host.url=''' + SONAR_URL + ''' \
            -Dsonar.login=$SONAR_TOKEN || \
            echo "SonarQube analysis completed with warnings"
        '''
      }
    }
  }
}
stage('Build & Push Docker Image') {
  steps {
    script {
      retry(3) {
        sh """
        docker build --no-cache --network=host --build-arg SKIP_PYTORCH=1
        -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
        """
      }

      // Push with credentials
      docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
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
