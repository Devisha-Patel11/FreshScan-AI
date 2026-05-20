import streamlit as st
from PIL import Image
from predict import predict_image

st.set_page_config(
    page_title="FreshScan AI",
    page_icon="🍎",
    layout="centered"
)

st.title("🍎 FreshScan AI")
st.caption("Fruit & Vegetable Recognition System using Deep Learning")

st.sidebar.title("About Project")
st.sidebar.write("""
FreshScan AI identifies fruits and vegetables from uploaded images.

Supported classes:
- Apple
- Banana
- Potato
- Tomato
- Unknown
""")

st.sidebar.warning("Tip: Upload a clear single-object image for better result.")

uploaded_file = st.file_uploader(
    "Upload Fruit or Vegetable Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Predict"):
        label, confidence = predict_image(image)

        st.subheader("Prediction Result")

        if label == "unknown" or "Unknown" in label:
            st.error("Result: Unknown / Not Supported")
            st.warning(f"Confidence: {confidence:.2f}%")
            st.write("Please upload only supported fruits/vegetables.")
        else:
            st.success(f"Result: {label.capitalize()}")
            st.info(f"Confidence: {confidence:.2f}%")

            if confidence >= 90:
                st.write(" High confidence prediction")
            elif confidence >= 70:
                st.write(" Medium confidence prediction")
            else:
                st.write(" Low confidence prediction")
else:
    st.info("Please upload an image to start prediction.")