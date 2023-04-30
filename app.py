import streamlit as st
import cv2
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces(uploaded_image):
    img = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    
    return pil_img

def main():
    st.title("Face Detection App")
    st.write("Upload an image to detect faces.")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Detecting faces...")
        result_image = detect_faces(image)
        st.image(result_image, caption='Result Image.', use_column_width=True)

if __name__ == '__main__':
    main()
