import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.saving import register_keras_serializable
from tensorflow.keras.applications.efficientnet import preprocess_input
import io

# Page configuration
st.set_page_config(page_title="Brain Tumor Classification", layout="wide")

# Load Classification Model
@st.cache_resource
def load_classification_model():
    return tf.keras.models.load_model("model.keras")




classification_model = load_classification_model()

# Class labels and descriptions
labels = ["Class 0: Glioma Tumor", "Class 1: No Tumor", "Class 2: Meningioma Tumor", "Class 3: Pituitary Tumor"]
descriptions = {
    "Class 0: Glioma Tumor": "A glioma is a type of tumor that occurs in the brain and spinal cord. It's one of the most common types of brain tumors.",
    "Class 1: No Tumor": "No signs of a tumor were detected in the uploaded image.",
    "Class 2: Meningioma Tumor": "A meningioma is a tumor that forms on membranes covering the brain and spinal cord just inside the skull.",
    "Class 3: Pituitary Tumor": "A pituitary tumor is an abnormal growth in the pituitary gland. Most of these tumors are benign."
}

# Streamlit UI
st.title("Brain Tumor Classification")
st.write("Upload an MRI image, and the application will classify it into one of the classes.")

uploaded_file = st.file_uploader("Upload an MRI Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded MRI Image", use_container_width=False)

    # ---- Classification ----
    st.subheader("Step 1: Classification")
    st.write("Classifying the image...")
    
    # Preprocess the image for classification
    image_resized = image.resize((150, 150)) 
    image_array = np.array(image_resized)
    image_array = preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Make prediction
    predictions = classification_model.predict(image_array)
    
    predicted_class = np.argmax(predictions)
    confidence = predictions[0][predicted_class] * 100
    # Glioma -95% 
    # Display classification result
    st.write(f"**Predicted Class:** {labels[predicted_class]}")
    st.write(f"**Confidence:** {confidence:.2f}%")
    st.write(descriptions[labels[predicted_class]])
