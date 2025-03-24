from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import cv2
import torch
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import uuid
from ultralytics import YOLO  # Import YOLOv8

app = Flask(__name__)

# Define paths
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
MODEL_PATH = 'models/best.pt'  # Your trained YOLOv8 model

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Load the YOLOv8 model
model = YOLO(MODEL_PATH)

def perform_segmentation(image_path):
    """Uses YOLOv8 to perform image segmentation and overlay bounding boxes."""
    img = cv2.imread(image_path)
    if img is None:
        return None, None  # Return None if image loading fails

    # Perform segmentation
    results = model(image_path, conf=0.25, task="segment")

    # Draw bounding boxes
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get box coordinates
            conf = box.conf[0].item()  # Confidence score
            label = f"cell {conf:.2f}"
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Extract the segmented mask from the results
        mask = result.masks.data.cpu().numpy() if result.masks is not None else None
        if mask is not None and len(mask) > 0:
            mask = (mask[0] * 255).astype("uint8")  # Convert to binary mask
            mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]))  # Resize to match image

            # Save segmented mask
            mask_filename = f"mask_{uuid.uuid4().hex[:8]}.png"
            mask_filepath = os.path.join(PROCESSED_FOLDER, mask_filename)
            cv2.imwrite(mask_filepath, mask_resized)

            # Save image with bounding boxes
            bbox_filename = f"bbox_{uuid.uuid4().hex[:8]}.png"
            bbox_filepath = os.path.join(PROCESSED_FOLDER, bbox_filename)
            cv2.imwrite(bbox_filepath, img)

            return bbox_filepath, mask_filepath  # Return both processed images

    return None, None  # If no segmentation mask is found

def overlay_mask(original_path, mask_path):
    """Overlays the segmentation mask onto the original image."""
    original = cv2.imread(original_path)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # Convert mask to color (e.g., red) for overlay
    mask_colored = np.zeros_like(original)
    mask_colored[:, :, 0] = mask  # Red channel

    # Blend the images
    overlayed = cv2.addWeighted(original, 0.7, mask_colored, 0.3, 0)

    # Save the output
    overlayed_filename = f"overlay_{uuid.uuid4().hex[:8]}.png"
    overlayed_path = os.path.join(PROCESSED_FOLDER, overlayed_filename)
    Image.fromarray(overlayed).save(overlayed_path)

    return overlayed_filename  # Return just the filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/segment', methods=['POST'])
def segment():
    if 'image' not in request.files:
        print("🚨 No image file provided in request!")
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        print("🚨 Empty filename received!")
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        print(f"✅ Image received: {file_path}")

        # Perform segmentation using YOLOv8
        original_path, mask_path = perform_segmentation(file_path)
        if mask_path is None:
            print("🚨 Segmentation failed: No mask detected")
            return jsonify({'error': 'Segmentation failed or no mask detected'}), 500
        
        print(f"✅ Segmentation successful! Mask saved at: {mask_path}")

        # Overlay mask on original image
        overlayed_filename = overlay_mask(original_path, mask_path)
        overlayed_image_url = f'http://127.0.0.1:5000/static/processed/{overlayed_filename}'
        print(f"✅ Overlayed image generated: {overlayed_image_url}")

        return jsonify({
            'message': 'Segmentation successful!',
            'overlayed_image': overlayed_image_url
       })

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
