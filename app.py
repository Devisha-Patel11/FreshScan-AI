import streamlit as st
from PIL import Image
from predict import predict_image

st.set_page_config(page_title="FreshScan AI",page_icon="🍎",layout="wide")

st.markdown("""
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
.main-title{font-size:42px;font-weight:800;}
.card{padding:20px;border-radius:15px;background-color:#111827;margin-top:15px;}
.result-text{font-size:24px;font-weight:700;}
</style>
""",unsafe_allow_html=True)



st.markdown('<div class="main-title">🍎 FreshScan AI</div>',unsafe_allow_html=True)
st.write("AI-powered Fresh & Rotten Fruit/Vegetable Detection System")

st.sidebar.title("Project Info")

st.sidebar.write("""
Supported:
- Apple
- Banana
- Mango
- Potato
- Tomato

Detects:
- Fresh
- Rotten
- Unknown
""")

st.sidebar.info("Upload a clear image containing a single fruit or vegetable for best results.")

# Upload or Camera
input_method = st.radio("Choose Input Method",["Upload Image","Use Camera"])

if input_method == "Upload Image":
    uploaded_file = st.file_uploader(
        "Upload Fruit or Vegetable Image",
        type=["jpg","jpeg","png"]
    )
else:
    uploaded_file = st.camera_input(
        "Capture Fruit or Vegetable Image"
    )

def format_label(label):
    if "Unknown" in label or label == "unknown":
        return "Unknown / Not Supported"
    return label.replace("Fresh","Fresh ").replace("Rotten","Rotten ")

def recommendation(label):
    if "Fresh" in label:
        return "This item looks fresh and usable."
    elif "Rotten" in label:
        return "This item looks rotten. Avoid using it."
    return "This image is not supported or confidence is low."

def get_item_name(label):
    label = label.replace("Fresh","").replace("Rotten","").replace(" ","")
    return label.lower()

def nutrition_info(label):

    item = get_item_name(label)

    data = {

        "apple":{
            "Calories":"About 52 kcal per 100g",
            "Vitamins":"Vitamin C, Vitamin K",
            "Benefits":"Good for digestion and heart health",
            "Storage Tips":"Store in a cool place or refrigerator"
        },

        "banana":{
            "Calories":"About 89 kcal per 100g",
            "Vitamins":"Vitamin B6, Vitamin C",
            "Benefits":"Good source of energy and potassium",
            "Storage Tips":"Store at room temperature away from direct sunlight"
        },

        "mango":{
            "Calories":"About 60 kcal per 100g",
            "Vitamins":"Vitamin A, Vitamin C",
            "Benefits":"Good for immunity and skin health",
            "Storage Tips":"Keep unripe mangoes at room temperature"
        },

        "potato":{
            "Calories":"About 77 kcal per 100g",
            "Vitamins":"Vitamin C, Vitamin B6",
            "Benefits":"Good source of carbohydrates and potassium",
            "Storage Tips":"Store in a cool dark place"
        },

        "tomato":{
            "Calories":"About 18 kcal per 100g",
            "Vitamins":"Vitamin C, Vitamin K",
            "Benefits":"Contains lycopene and supports heart health",
            "Storage Tips":"Store at room temperature"
        }
    }

    if item in data and "Unknown" not in label:

        st.markdown("### Nutrition Information")

        for key,value in data[item].items():
            st.write(f"{key}: {value}")

if uploaded_file is not None:

    col1,col2 = st.columns([1,1])

    with col1:

        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    with col2:

        st.markdown("### Prediction Result")

        if st.button("Predict"):

            label,confidence = predict_image(image)

            pretty_label = format_label(label)

            st.markdown('<div class="card">',unsafe_allow_html=True)

            if "Unknown" in pretty_label:

                st.error(f"Result: {pretty_label}")

            elif "Fresh" in pretty_label:

                st.success(f"Result: {pretty_label}")

            else:

                st.error(f"Result: {pretty_label}")

            st.info(f"Confidence: {confidence:.2f}%")

            st.progress(int(confidence))

            st.write(recommendation(label))

            if "Unknown" not in pretty_label:

                nutrition_info(label)

                if confidence >= 90:
                    st.success("Quality Score: Excellent")

                elif confidence >= 75:
                    st.info("Quality Score: Good")

                elif confidence >= 50:
                    st.warning("Quality Score: Average")

                else:
                    st.error("Quality Score: Poor")

            st.markdown('</div>',unsafe_allow_html=True)

else:

    st.info("Please upload or capture an image to start prediction.")