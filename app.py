# import cv2
# import streamlit as st

# def capture_and_register():
#     global cap
#     cap = cv2.VideoCapture(0)
#     st.write("Hi, let's register your face")
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             st.warning("Could not read from the camera")
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         st.image(frame, use_column_width=True, channels="RGB")
#         if st.button("Register"):
#             cv2.imwrite("registered_face.jpg", frame)
#             st.success("Successfully registered your face!")
#             break
#     cap.release()

# def detect():
#     st.write("Face detection")
#     registered_face = cv2.imread("registered_face.jpg")
#     if registered_face is None:
#         st.warning("No registered face found. Please register your face first.")
#         return
#     face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             st.warning("Could not read from the camera")
#             break
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             roi_gray = gray[y:y + h, x:x + w]
#             roi_color = frame[y:y + h, x:x + w]
#             try:
#                 res = cv2.matchTemplate(roi_gray, registered_face, cv2.TM_CCOEFF_NORMED)
#                 if res > 0.8:
#                     st.warning("Unlocked. Face recognized.")
#                 else:
#                     st.warning("Face not recognized.")
#             except:
#                 pass
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         st.image(frame, use_column_width=True, channels="RGB")
#         if st.button("Stop"):
#             break
#     cap.release()

# if __name__ == '__main__':
#     st.title("Face Recognition")
#     st.sidebar.title("Menu")
#     app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Register", "Detect"])

#     if app_mode == "Homepage":
#         st.write("Welcome to Face Recognition")
#         st.write("Please select a mode from the menu.")
#     elif app_mode == "Register":
#         capture_and_register()
#     elif app_mode == "Detect":
#         detect()


# import cv2
# import streamlit as st

# def capture_and_register():
#     global cap
#     cap = st.camera_input("Take a picture")
#     st.write("Hi, let's register your face")
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             st.warning("Could not read from the camera. Please try again.")
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         st.image(frame, use_column_width=True, channels="RGB")
#         if st.button("Register"):
#             try:
#                 cv2.imwrite("registered_face.jpg", frame)
#                 st.success("Successfully registered your face!")
#             except:
#                 st.warning("Could not save the registered face. Please try again.")
#             break
#     cap.release()

# def detect():
#     st.write("Face detection")
#     registered_face = cv2.imread("registered_face.jpg")
#     if registered_face is None:
#         st.warning("No registered face found. Please register your face first.")
#         return
#     face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             st.warning("Could not read from the camera. Please try again.")
#             break
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             roi_gray = gray[y:y + h, x:x + w]
#             roi_color = frame[y:y + h, x:x + w]
#             try:
#                 res = cv2.matchTemplate(roi_gray, registered_face, cv2.TM_CCOEFF_NORMED)
#                 if res > 0.8:
#                     st.warning("Unlocked. Face recognized.")
#                 else:
#                     st.warning("Face not recognized.")
#             except Exception as e:
#                 st.warning("An error occurred while recognizing the face: {}".format(str(e)))
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         st.image(frame, use_column_width=True, channels="RGB")
#         if st.button("Stop"):
#             break
#     cap.release()

# if __name__ == '__main__':
#     st.title("Face Recognition")
#     st.sidebar.title("Menu")
#     app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Register", "Detect"])

#     if app_mode == "Homepage":
#         st.write("Welcome to Face Recognition")
#         st.write("Please select a mode from the menu.")
#     elif app_mode == "Register":
#         capture_and_register()
   
import cv2
import numpy as np
import os
import pickle
import streamlit as st

# Tạo thư mục để lưu ảnh người dùng đăng ký
if not os.path.exists("registered_users"):
    os.makedirs("registered_users")

# Định nghĩa hàm lưu dữ liệu người dùng đăng ký
def save_user_data(name, age, gender, embedding):
    data = {
        "name": name,
        "age": age,
        "gender": gender,
        "embedding": embedding
    }
    with open(f"registered_users/{name}.pkl", "wb") as f:
        pickle.dump(data, f)

# Định nghĩa hàm đăng ký
def register():
    # Lấy ảnh từ camera
    st.write("Vui lòng điền thông tin của bạn")
    name = st.text_input("Tên")
    age = st.number_input("Tuổi")
    gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
    if not name or not age or not gender:
        st.write("Vui lòng điền đầy đủ thông tin!")
        return
    st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Đăng ký")
    image = st.image([])
    if st.button("Đăng ký"):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            # Hiển thị khung hình trên Streamlit
            image.image(frame)
            # Xác định vùng chứa khuôn mặt
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) > 0:
                # Lưu ảnh và nhúng khuôn mặt
                x, y, w, h = faces[0]
                face_image = frame[y:y+h, x:x+w]
                face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                embedding = face_recognition.face_encodings(face_image)[0]
                save_user_data(name, age, gender, embedding)
                st.write("Đăng ký thành công!")
                break
        cap.release()
    
# Định nghĩa hàm nhận diện
def recognize():
    # Đọc dữ liệu người dùng đã đăng ký
    registered_users = []
    for filename in os.listdir("registered_users"):
        with open(os.path.join("registered_users", filename), "rb") as f:
            user_data = pickle.load(f)
            registered_users.append(user_data)
    
    # Lấy ảnh từ camera
    st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Nhận diện")
    image = st.image([])

    if st.button("Nhận diện"):
        cap = cv2.VideoCapture(0)
        _, frame = cap.read()
        cap.release()

        # Đổi màu ảnh từ BGR sang RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Phát hiện khuôn mặt trong ảnh
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            st.write("Không tìm thấy khuôn mặt trong ảnh. Vui lòng thử lại.")
        else:
            # Vẽ hình chữ nhật bao quanh khuôn mặt và hiển thị thông tin người dùng
            for (x,y,w,h) in faces:
                # Vẽ hình chữ nhật bao quanh khuôn mặt
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

                # Nhận diện khuôn mặt
                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (100, 100))
                face_img = face_img.reshape(1, -1)

                # Sử dụng model để dự đoán
                label = model.predict(face_img)[0]
                confidence = model.predict_proba(face_img)[0][label]

                # Hiển thị thông tin người dùng
                if confidence > 0.7:
                    found_user = False
                    for user in registered_users:
                        if user["label"] == label:
                            found_user = True
                            st.write("Xin chào, {}! Tuổi của bạn là {} và giới tính là {}.".format(user["name"], user["age"], user["gender"]))
                            st.write("Tỉ lệ khớp: {:.2f}%".format(confidence * 100))
                            break
                    if not found_user:
                        st.write("Không tìm thấy thông tin người dùng. Vui lòng đăng ký trước khi sử dụng tính năng này.")
                else:
                    st.write("Không tìm thấy thông tin người dùng. Vui lòng đăng ký trước khi sử dụng tính năng này.")
if __name__ == '__main__':
    st.title("Face Recognition")
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Register", "Detect"])

    if app_mode == "Homepage":
        st.write("Welcome to Face Recognition")
        st.write("Please select a mode from the menu.")
    elif app_mode == "Register":
        register()
    elif app_mode == "Detect":
        recognize()
