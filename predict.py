import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
model = tf.keras.models.load_model("model/freshscan_model.h5")

# Labels
labels = ["apple", "banana", "potato", "tomato", "unknown"]

def predict_image(image):

    # Resize image
    image = image.resize((128, 128))

    # Convert to array
    image_array = np.array(image) / 255.0

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Prediction
    prediction = model.predict(image_array)

    # Highest probability index
    class_index = np.argmax(prediction)

    # Confidence score
    confidence = np.max(prediction) * 100

    # Low confidence detection
    if confidence < 90:
        return "Unknown / Not Supported", confidence

    return labels[class_index], confidence