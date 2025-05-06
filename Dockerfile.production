# Stage 1: Use a pre-built PyTorch image to avoid installing torch
FROM pytorch/pytorch:latest as builder

WORKDIR /app

# Copy the application code (requirements.txt and app.py)
COPY requirements.txt requirements.txt
COPY . .

# Install other dependencies from requirements.txt (excluding torch)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=300 --retries=5 -r requirements.txt

# Stage 2: Use Distroless for minimal runtime
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /app /app

# Set Python path for dependencies
ENV PYTHONPATH=/app

# Expose the port your app will run on
EXPOSE 5000

# Run the application using the Python interpreter
CMD ["/usr/bin/python3", "app.py"]
