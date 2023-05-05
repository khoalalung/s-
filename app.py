import streamlit as st
import cv2
import numpy as np
import os

# Phần 1: Chụp hình và ghi thông tin

def capture_and_register():
    # Khởi tạo camera
    cap = cv2.VideoCapture(0)
    
    # Lấy hình ảnh từ camera
    ret, frame = cap.read()
    
    # Hiển thị hình ảnh
    st.image(frame, channels="BGR")
    
    # Nhập thông tin người dùng
    name = st.text_input("Name:")
    age = st.number_input("Age:")
    gender = st.selectbox("Gender:", ["Male", "Female"])
    
    # Nếu thông tin không đầy đủ, yêu cầu nhập lại
    if name == "" or age == 0 or gender == "":
        st.warning("Please fill in all required information.")
        return
    
    # Tạo thư mục để lưu thông tin
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Lưu thông tin vào file
    filename = f"data/{name}.txt"
    with open(filename, "w") as f:
        f.write(f"Name: {name}\n")
        f.write(f"Age: {age}\n")
        f.write(f"Gender: {gender}\n")
    st.success("Registration done!")

# Phần 2: Nhận diện khuôn mặt và hiển thị thông tin

def detect_face():
    # Khởi tạo camera
    cap = cv2.VideoCapture(0)
    
    # Đọc mô hình nhận diện khuôn mặt và phân loại giới tính
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    age_net = cv2.dnn.readNetFromCaffe("age.prototxt", "age.caffemodel")
    gender_net = cv2.dnn.readNetFromCaffe("gender.prototxt", "gender.caffemodel")
    
    while True:
        # Lấy hình ảnh từ camera
        ret, frame = cap.read()
        
        # Nhận diện khuôn mặt
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        # Hiển thị các khuôn mặt được nhận diện
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
             # Xác định vị trí khuôn mặt
            face_roi = frame[y:y+h, x:x+w]

            # Đưa khuôn mặt qua mô hình để phân loại giới tính
            blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()

            # Đưa khuôn mặt qua mô hình để phân loại độ tuổi
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_preds[0].dot(np.arange(0, 101).reshape(101, 1)).flatten()[0]

            # Xác định giới tính dựa trên kết quả phân loại
            gender = "Male" if gender_preds[0][0] > 0.5 else "Female"

            # Hiển thị thông tin khuôn mặt
            st.write(f"Age: {int(age)}")
            st.write(f"Gender: {gender}")
            confidence = np.max(gender_preds)
            st.write(f"Confidence: {confidence}")

            # Hiển thị hình ảnh
            st.image(frame, channels="BGR")

            # Kiểm tra người dùng có muốn dừng chương trình hay không
            if st.button("Stop"):
                cap.release()
                cv2.destroyAllWindows()
                return

# Chạy chương trình
if st.button("Register"):
    capture_and_register()
if st.button("Detect"):
    detect_face()

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
