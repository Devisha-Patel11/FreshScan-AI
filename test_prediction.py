from PIL import Image
from predict import predict_image

# Test image path
image_path = "dataset/test/apple/apple (1).jpg"

# Open image
image = Image.open(image_path).convert("RGB")

# Predict
label, confidence = predict_image(image)

# Print result
print("Prediction:", label)
print("Confidence:", confidence)