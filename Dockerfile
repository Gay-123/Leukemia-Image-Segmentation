# Base image with PyTorch + CUDA + essential tools
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Install system dependencies (OpenCV + Docker CLI + utilities)
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    libgl1 \
    libglib2.0-0 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose v2 (modern syntax)
RUN mkdir -p ~/.docker/cli-plugins/ && \
    curl -SL https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose && \
    chmod +x ~/.docker/cli-plugins/docker-compose

# Install PyTorch (CU117) explicitly to pin and cache this layer
RUN pip install torch==2.0.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

# Set work directory
WORKDIR /app

# Layer caching trick: copy only requirements first
COPY requirements.txt .  
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the main app file first for caching
COPY app.py . 

# Then copy the rest of the codebase
COPY . .

# Check Docker and Python version
RUN docker --version && python --version

# Health check
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:5000/health || exit 1

# Entrypoint with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "app:app"]
