## 🧠 Leukemia Cell Segmentation

This project uses a YOLOv8 model to segment leukemia cells from microscopic images. The model is deployed through a Flask web app, allowing users to upload images and receive segmented results. The project also incorporates a CI/CD pipeline with tools like Jenkins, Docker, SonarQube, Kubernetes, and ArgoCD to automate the development and deployment processes.


## 🔧 Project Components

- 🧠 **YOLOv8 segmentation model** for detecting leukemia cells in images.
- 🌐 **Flask web app** to serve the model and handle inference requests.
- 🐳 **Docker** for containerization and environment consistency.
- 🔄 **Jenkins CI/CD pipeline** to automate the build, test, and deployment process.
- 🔍 **SonarQube** for static code analysis, ensuring high code quality.
- 🚀 **Kubernetes** for managing containerized applications.
- 💻 **ArgoCD** for continuous deployment and automated syncing with GitHub.

---

## 📊 Dataset

The dataset used for training the YOLOv8 model consists of microscopic images of leukemia cells, specifically focusing on segmentation for accurate diagnosis. The images have been preprocessed, including resizing and normalization, for optimal model training.

- 🔗 **[View Dataset on Roboflow](https://universe.roboflow.com/suman-computer-vision/leukemia-riajh/dataset/1)**
- 🧾 **License**: CC BY 4.0
- 📦 **Classes**: 1 (cell)
- 🔢 **Number of Images**: 506

---

## 🌐 Flask API for Model Inference

A minimal Flask-based API is integrated to serve the YOLOv8 segmentation model. Users can clone the repository and run the app locally to perform inference on leukemia cell images.

- 📥 **Accepts input images** for processing
- 🧠 **Applies the trained YOLOv8 model** for segmentation
- 📤 **Returns the output** with highlighted leukemia cells

### How to Run the Flask Web App Locally

# 1️⃣ Clone the repository
```bash
git clone https://github.com/Gay-123/Leukemia-Image-Segmentation
cd Leukemia-Image-Segmentation
```
# 2️⃣ Build and run the Flask app
```bash
docker build -t leukemia-app .
docker run -p 5000:5000 leukemia-app
```
👉 Now open http://localhost:5000 in your browser.

---

### **🚀 CI/CD Pipeline**

The CI/CD pipeline is the heart of this project, automating everything from code integration to Kubernetes deployment using Jenkins, SonarQube, DockerHub, and ArgoCD.

##Pipeline Stages:

## **1.✅ Build Trigger**
The pipeline is triggered automatically on every commit to the repository.

## **2.🐳 Docker Image Build**
Jenkins uses a custom agent (gayathri814/jenkins-agent) to build the Docker image using the Dockerfile. The image is tagged as leukemia-app:<BUILD_TAG>.

## **3.🔍 Code Quality Check**
SonarQube scans the code for bugs, vulnerabilities, and code smells. Folders like static/, templates/, and .pt files are excluded to reduce noise.

## **4.📦 Push to DockerHub**
If the code passes SonarQube’s quality checks, the Docker image is pushed to DockerHub with the tag:
👉 docker.io/gayathri814/leukemia-app:<BUILD_TAG>

## **5.🚀 Kubernetes Deployment (CD)**
ArgoCD continuously syncs with GitHub. The updated image tag in `deployment.yml` is picked up and deployed automatically to the Kubernetes cluster.

---

✅ Tools Used

| Tool           |        Purpose                        |
| -------------- |---------------------------------------|
| **Jenkins**    |        CI Automation                  |
| **Docker**     |        Containerization               |
| **SonarQube**  |        Code Quality & Static Analysis |
| **DockerHub**  |        Image Registry                 |
| **ArgoCD**     |        GitOps Continuous Delivery     |
| **Kubernetes** |        App Deployment and Scaling     |


---
### **🛠️ Tools Setup**

### **1. Jenkins Setup**

# *To set up Jenkins for the CI/CD pipeline:*

## **1.Install Jenkins:**
If Jenkins is not installed yet, you can run it via Docker:

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```
## **2.Access Jenkins:**
After running the above command, Jenkins will be accessible at http://localhost:8080.

## **3.Unlock Jenkins:**
On the first access, Jenkins will ask for an unlock key. Get the key by running the following command:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
## **4.Install Suggested Plugins:**
Once unlocked, Jenkins will prompt you to install the recommended plugins. Proceed with that option.

## **5.Set Up Jenkins Agent:**
In your Jenkins setup, you can create an agent (such as gayathri814/jenkins-agent) to run your Docker image builds as part of the pipeline.


### **2. SonarQube Setup**
SonarQube is deployed via Docker:

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube
```
You can access it at http://localhost:9000.

### **3. ArgoCD Setup**

ArgoCD is installed using the [OperatorHub.io](https://operatorhub.io/). Once installed, it continuously syncs with GitHub and automates the deployment to Kubernetes.

---
### 🎉 Conclusion
This project demonstrates an end-to-end pipeline for leukemia cell segmentation using the latest technologies like YOLOv8, Flask, Docker, Jenkins, SonarQube, Kubernetes, and ArgoCD. The integration of CI/CD ensures that the model is continuously tested, built, and deployed with ease, providing a robust solution for real-time leukemia cell detection.

---
