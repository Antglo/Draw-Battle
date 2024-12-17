# backend/app/ml/classifier.py

import tensorflow as tf
from PIL import Image
import io

# Load a pre-trained model (e.g., MobileNet for prototyping)
MODEL_PATH = "app/ml/model/mobilenet_model.h5"  # Replace with your custom model path
model = tf.keras.models.load_model(MODEL_PATH)

# Define labels for the model's output
LABELS = ["sword", "shield", "arrow", "other"]  # Customize based on your model

def classify_image(image_bytes: bytes) -> str:
    # Load the image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))  # Resize for MobileNet compatibility

    # Preprocess the image
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = image_array / 255.0  # Normalize to [0, 1]

    # Make a prediction
    predictions = model.predict(image_array)
    predicted_label = LABELS[predictions.argmax()]
    return predicted_label
