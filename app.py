
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

# def capture_images(id_, credentials):
#     face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     cam = cv2.VideoCapture(0)
#     sample_num = 0
#     image_count = 0
#     while True:
#         ret, img = cam.read()
#         if not ret:
#             print('Failed to capture image')
#             break
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
#         if not os.path.exists('dataset'):
#             os.makedirs('dataset')

#         for (x, y, w, h) in faces:
#             sample_num += 1
#             if sample_num % 5 == 0:
#                 image_count += 1
#                 image_filename = f'dataset/User.{id_}.{image_count}.jpg'
#                 cv2.imwrite(image_filename, gray[y:y+h, x:x+w])
#                 cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

#                 try:
#                     service = build(API_NAME, API_VERSION, credentials=credentials)
#                     file_metadata = {'name': os.path.basename(image_filename)}
#                     media = MediaFileUpload(image_filename, resumable=True)
#                     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#                     print(f'File ID: {file.get("id")}')
#                     os.remove(image_filename)
#                 except HttpError as error:
#                     print(f'An error occurred: {error}')
#                     file = None

#         cv2.imshow('image', img)
#         if cv2.waitKey(1) == ord('q'):
#             break
#         if image_count >= 40:
#             break
#     cam.release()
#     cv2.destroyAllWindows()
# def main():
#     st.title("Capture and upload face images")
#     credentials = get_credentials()
#     with sqlite3.connect(DATABASE) as conn:
#         create_table(conn)
#         id_ = st.text_input("Enter ID:")
#         name = st.text_input("Enter name:")
#         age = st.text_input("Enter age:")
#         gender = st.text_input("Enter gender:")
        
#         if id_ and name and age and gender:
#             insert_or_update_record(conn, id_, name, age, gender)
#         if st.button("Capture Images"):
#             capture_images(id_, credentials)
#             st.success("Images captured and uploaded successfully!")
# if __name__ == '__main__':
#     try:
#         main()
#     except Exception as e:
#         print(e)
#         cv2.destroyAllWindows()
def upload_to_drive(file_path, credentials):
    try:
        service = build(API_NAME, API_VERSION, credentials=credentials)
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        print(f'File ID: {file_id}')
    return file_id
    except HttpError as error:
        print(f'An error occurred: {error}')
    return None

def main():
    conn = sqlite3.connect(DATABASE)
    create_table(conn)
    st.set_page_config(page_title='Face Recognition App', layout='wide')

    st.title('Face Recognition App')

    menu = ['Add Person', 'Recognize Faces']
    choice = st.sidebar.selectbox('Select an option', menu)

    if choice == 'Add Person':
        id_ = st.text_input('Enter ID')
        name = st.text_input('Enter Name')
        age = st.number_input('Enter Age')
        gender = st.selectbox('Select Gender', ['Male', 'Female'])

        if st.button('Add Person'):
            if not id_ or not name or not age or not gender:
                st.error('Please fill in all the fields')
            else:
                insert_or_update_record(conn, id_, name, age, gender)
                st.success('Person added successfully')

    elif choice == 'Recognize Faces':
        if st.button('Start Camera'):
            if not os.path.exists('dataset'):
                os.makedirs('dataset')

            id_ = st.text_input('Enter ID')
            name = st.text_input('Enter Name')
            if not id_ or not name:
                st.error('Please fill in both ID and Name')
                st.stop()

            credentials = get_credentials()
            if not credentials:
                st.error('Failed to get Google Drive credentials. Please check your secrets.toml file')
                st.stop()

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
                for (x,y,w,h) in faces:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                    sample_num += 1
                    cv2.imwrite(f'dataset/User.{id_}.{sample_num}.jpg', gray[y:y+h,x:x+w])
                    cv2.imshow('Camera Feed', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sample_num >= 30:
                    st.write('30 samples captured successfully')
                    break

            cam.release()
            cv2.destroyAllWindows()

            dataset_path = 'dataset'
            zip_path = f'{name}.zip'
            zip_files(dataset_path, zip_path)
            file_id = upload_to_drive(zip_path, credentials)
            if file_id:
                st.success('Images uploaded to Google Drive successfully')
                os.remove(zip_path)
                shutil.rmtree(dataset_path)
            else:
                st.error('Failed to upload images to Google Drive')
                st.stop()

    conn.close()
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        cv2.destroyAllWindows()
