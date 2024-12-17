# backend/app/ml/classifier.py

import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from PIL import Image
import io

# Load the pre-trained MobileNetV2 model
MODEL_PATH = "app/ml/model/mobilenet_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

def classify_image(image_bytes: bytes) -> str:
    """
    Classify an image using the pre-trained MobileNetV2 model.
    """
    # Load the image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))  # Resize to 224x224 (required by MobileNet)

    # Preprocess the image
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = preprocess_input(image_array)  # Normalize to match model requirements
    image_array = tf.expand_dims(image_array, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(image_array)
    decoded = decode_predictions(predictions, top=1)[0]  # Get top-1 result
    label, confidence = decoded[0][1], decoded[0][2]

    # Return the label and confidence
    return f"{label} ({confidence:.2f})"
