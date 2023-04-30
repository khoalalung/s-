# import streamlit as st
# import cv2
# from PIL import Image

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# def detect_faces(uploaded_image):
#     img = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
#     faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     pil_img = Image.fromarray(img)
    
#     return pil_img

# def main():
#     st.title("Face Detection App")
#     st.write("Upload an image to detect faces.")
#     uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
#     if uploaded_image is not None:
#         image = Image.open(uploaded_image)
#         st.image(image, caption='Uploaded Image.', use_column_width=True)
#         st.write("")
#         st.write("Detecting faces...")
#         result_image = detect_faces(image)
#         st.image(result_image, caption='Result Image.', use_column_width=True)

# if __name__ == '__main__':
#     main()
import cv2
import sqlite3
import os
import streamlit as st
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

DATABASE = 'data.db'
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_NAME = 'drive'
API_VERSION = 'v3'

def get_credentials():
    creds = None
    if st.secrets["google"]["auth_type"] == "service":
        creds = Credentials.from_service_account_info(st.secrets["google"])
    elif st.secrets["google"]["auth_type"] == "user":
        if "google_credentials" not in st.session_state:
            st.session_state["google_credentials"] = Credentials.from_authorized_user_info(info=st.secrets["google"], scopes=SCOPES)
        creds = st.session_state["google_credentials"]
        try:
            creds.refresh(Request())
        except RefreshError:
            st.error("Failed to refresh access token. Please logout and login again.")
            st.stop()
    else:
        st.error("Invalid auth_type in secrets.toml. Use 'user' or 'service'.")
        st.stop()
    return creds

def create_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS people (
            ID INT PRIMARY KEY NOT NULL,
            name TEXT,
            age INT,
            gender TEXT
        )
    ''')

def is_record_exist(conn, id_):
    cursor = conn.execute('SELECT * FROM people WHERE ID = ?', (id_,))
    return cursor.fetchone() is not None

def insert_or_update_record(conn, id_, name, age, gender):
    if is_record_exist(conn, id_):
        query = 'UPDATE people SET name = ?, age = ?, gender = ? WHERE ID = ?'
    else:
        query = 'INSERT INTO people (ID, name, age, gender) VALUES (?, ?, ?, ?)'

    conn.execute(query, (id_, name, age, gender))
    conn.commit()

def capture_images(id_, credentials):
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    sample_num = 0
    image_count = 0
    while True:
        ret, img = cam.read()
        if not ret:
            print('Failed to capture image')
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        if not os.path.exists('dataset'):
            os.makedirs('dataset')

        for (x, y, w, h) in faces:
            sample_num += 1
            if sample_num % 5 == 0:
                image_count += 1
                image_filename = f'dataset/User.{id_}.{image_count}.jpg'
                cv2.imwrite(image_filename, gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                try:
                    service = build(API_NAME, API_VERSION, credentials=credentials)
                    file_metadata = {'name': os.path.basename(image_filename)}
                    media = MediaFileUpload(image_filename, resumable=True)
                    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                    print(f'File ID: {file.get("id")}')
                    os.remove(image_filename)
                except HttpError as error:
                    print(f'An error occurred: {error}')
                    file = None

    cv2.imshow('image', img)
    if cv2.waitKey(1) == ord('q'):
        break
    if image_count >= 40:
        break
cam.release()
cv2.destroyAllWindows()
