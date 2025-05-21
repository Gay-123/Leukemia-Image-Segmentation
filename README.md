# 🧠 Leukemia Cell Segmentation

This project segments leukemia cells from microscopic images using a YOLOv8 model, deployed via a Flask web app. What truly powers this project is the **CI/CD pipeline**, crafted with **Jenkins**, **Docker**, **SonarQube**, **Kubernetes**, and **ArgoCD** for streamlined automation and deployment.

---

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
- 🔢 **Number of Images**: [Add number of images]

---

## 🌐 Flask API for Model Inference

A minimal Flask-based API is integrated to serve the YOLOv8 segmentation model. Users can clone the repository and run the app locally to perform inference on leukemia cell images.

- 📥 **Accepts input images** for processing
- 🧠 **Applies the trained YOLOv8 model** for segmentation
- 📤 **Returns the output** with highlighted leukemia cells

### How to Run the Flask Web App Locally

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Gay-123/Leukemia-Image-Segmentation
cd Leukemia-Image-Segmentation
```
# 2️⃣ Build and run the Flask app
```bash
docker build -t leukemia-app .
docker run -p 5000:5000 leukemia-app
```
👉 Now open http://localhost:5000 in your browser.


🚀 CI/CD Pipeline
The CI/CD pipeline is the heart of this project, automating everything from code integration to Kubernetes deployment using Jenkins, SonarQube, DockerHub, and ArgoCD.

Pipeline Stages:
✅ Build Trigger
The pipeline is triggered automatically on every commit to the repository.

🐳 Docker Image Build
Jenkins uses a custom agent (gayathri814/jenkins-agent) to build the Docker image using the Dockerfile. The image is tagged as leukemia-app:<BUILD_TAG>.

🔍 Code Quality Check
SonarQube scans the code for bugs, vulnerabilities, and code smells. Folders like static/, templates/, and .pt files are excluded to reduce noise.

📦 Push to DockerHub
If the code passes SonarQube’s quality checks, the Docker image is pushed to DockerHub with the tag:
👉 docker.io/gayathri814/leukemia-app:<BUILD_TAG>

Kubernetes Deployment (CD)
ArgoCD continuously syncs with GitHub. The updated image tag in deployment.yml is picked up and deployed automatically to the Kubernetes cluster.
---

✅ Tools Used

| Tool           | Purpose                        |
| -------------- | ------------------------------ |
| **Jenkins**    | CI Automation                  |
| **Docker**     | Containerization               |
| **SonarQube**  | Code Quality & Static Analysis |
| **DockerHub**  | Image Registry                 |
| **ArgoCD**     | GitOps Continuous Delivery     |
| **Kubernetes** | App Deployment and Scaling     |


---
🛠️ Tools Setup
1. SonarQube Setup
SonarQube is deployed via Docker:

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube
```
You can access it at http://localhost:9000.

###ArgoCD Setup
ArgoCD is installed using the [OperatorHub.io](https://operatorhub.io/). Once installed, it continuously syncs with GitHub and automates the deployment to Kubernetes.

---
📝 License
This project is licensed under the MIT License. See the LICENSE file for more details.

---



