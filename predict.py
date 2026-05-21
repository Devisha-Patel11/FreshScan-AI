import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
model = tf.keras.models.load_model("model/freshscan_model.h5")

# Labels
labels = [
    "FreshApple",
    "FreshBanana",
    "FreshMango",
    "FreshPotato",
    "FreshTomato",
    "RottenApple",
    "RottenBanana",
    "RottenMango",
    "RottenPotato",
    "RottenTomato",
    "unknown"
]

def predict_image(image):

    # Convert image to RGB
    image = image.convert("RGB")

    # Resize image
    image = image.resize((128,128))

    # Convert image to numpy array
    image_array = np.array(image,dtype=np.float32)

    # Normalize image
    image_array = image_array / 255.0

    # Add batch dimension
    image_array = np.expand_dims(image_array,axis=0)

    # Prediction
    prediction = model.predict(image_array,verbose=0)

    # Predicted class index
    class_index = np.argmax(prediction)

    # Confidence score
    confidence = float(np.max(prediction) * 100)

    # Predicted label
    predicted_label = labels[class_index]

    # Low confidence detection
    if confidence < 65:
        return "Unknown / Low Confidence",confidence

    # Unknown class handling
    if predicted_label == "unknown":
        return "Unknown / Not Supported",confidence

    return predicted_label,confidence