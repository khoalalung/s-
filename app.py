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

# def register():
#     global cap
#     cap = st.camera_input("Take a picture")
#     st.write("Hi, let's register your face")
#     while True:
#         if cap is not None:
#             ret, frame = cap.read()
#         else:
#             break
#         ret, frame = cap.read()

#         if not ret:
#             st.warning("Could not read from the camera. Please try again.")
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         st.image(frame, use_column_width=True, channels="RGB")

#         st.write("Vui lòng điền thông tin của bạn")
#         name = st.text_input("Tên")
#         age = st.number_input("Tuổi")
#         gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
#         if not name or not age or not gender:
#             st.write("Vui lòng điền đầy đủ thông tin!")
#             continue
#         st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Đăng ký")
#         image = st.image([])
#         if st.button("Đăng ký"):
#             image.image(frame)
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             face_locations = face_recognition.face_locations(rgb_frame, model="hog")
#             if len(face_locations) > 0:
#                 encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0] 
#                 df = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender], "Encoding": [encoding]})
#                 if os.path.exists("data.csv"):
#                     df.to_csv("data.csv", mode="a", header=False, index=False)
#                 else:
#                     df.to_csv("data.csv", index=False)
#                 st.write("Đăng ký thành công!")
#                 cap.release()
#                 break

#     cap.release()
def register():
    global cap
    cap = st.camera_input("Take a picture")
    st.write("Hi, let's register your face")
    while True:
        if cap is not None:
            ret, frame = cap.read()
        else:
            break
        ret, frame = cap.read()

        if not ret:
            st.warning("Could not read from the camera. Please try again.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")

        st.write("Vui lòng điền thông tin của bạn")
        name = st.text_input("Tên")
        age = st.number_input("Tuổi")
        gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
        if not name or not age or not gender:
            st.write("Vui lòng điền đầy đủ thông tin!")
            continue
        st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Đăng ký")
        image = st.image([])
        if st.button("Đăng ký"):
            image.image(frame)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            if len(face_locations) > 0:
                encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0] 
                df = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender], "Encoding": [encoding]})
                if os.path.exists("data.csv"):
                    df.to_csv("data.csv", mode="a", header=False, index=False)
                else:
                    df.to_csv("data.csv", index=False)
                st.write("Đăng ký thành công!")
                try:
                    cap.release()
                except AttributeError:
                    pass  # Or you could print an error message here
                break
    try:
        cap.release()
    except AttributeError:
        pass  # Or you could print an error message here


    
def recognize():
    registered_users = []
    for filename in os.listdir("registered_users"):
        with open(os.path.join("registered_users", filename), "rb") as f:
            user_data = pickle.load(f)
            registered_users.append(user_data)
    
    # Lấy ảnh từ camera
    st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Nhận diện")
    image = st.image([])

    if st.button("Nhận diện"):
        cap = st.camera_input("Take a picture")
        _, frame = cap.read()
        cap.release()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            st.write("Không tìm thấy khuôn mặt trong ảnh. Vui lòng thử lại.")
        else:
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (100, 100))
                face_img = face_img.reshape(1, -1)
########################################################################################### sử dụng model pickle
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
