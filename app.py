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


import cv2
import streamlit as st

def capture_and_register():
    global cap
    cap = st.camera_input("Take a picture")
    st.write("Hi, let's register your face")
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not read from the camera. Please try again.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")
        if st.button("Register"):
            try:
                cv2.imwrite("registered_face.jpg", frame)
                st.success("Successfully registered your face!")
            except:
                st.warning("Could not save the registered face. Please try again.")
            break
    cap.release()

def detect():
    st.write("Face detection")
    registered_face = cv2.imread("registered_face.jpg")
    if registered_face is None:
        st.warning("No registered face found. Please register your face first.")
        return
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not read from the camera. Please try again.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            try:
                res = cv2.matchTemplate(roi_gray, registered_face, cv2.TM_CCOEFF_NORMED)
                if res > 0.8:
                    st.warning("Unlocked. Face recognized.")
                else:
                    st.warning("Face not recognized.")
            except Exception as e:
                st.warning("An error occurred while recognizing the face: {}".format(str(e)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")
        if st.button("Stop"):
            break
    cap.release()

if __name__ == '__main__':
    st.title("Face Recognition")
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Register", "Detect"])

    if app_mode == "Homepage":
        st.write("Welcome to Face Recognition")
        st.write("Please select a mode from the menu.")
    elif app_mode == "Register":
        capture_and_register()
   

# import cv2

# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# def capture_and_register():
#     name = input("Enter your name: ")
#     age = input("Enter your age: ")
#     gender = input("Enter your gender: ")
#     print("Look at the camera and wait for the capture...")
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = faceCascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30),
#         )
#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = frame[y:y+h, x:x+w]
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         cv2.imshow('Capture and Register', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()
#     if len(name) == 0 or len(age) == 0 or len(gender) == 0:
#         print("Please enter your name, age, and gender!")
#         capture_and_register()
#     else:
#         print("User registered successfully!")
        

# def detect():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = faceCascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30),
#         )
#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = frame[y:y+h, x:x+w]
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
#             # Create a text string with user info and similarity percentage
#             text = "Name: {}, Age: {}, Gender: {}".format(name, age, gender)
#             similarity_percentage = 95 # Placeholder for similarity percentage
#             similarity_text = "Similarity: {}%".format(similarity_percentage)
            
#             # Display the text string and similarity percentage on the frame
#             cv2.putText(frame, text, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#             cv2.putText(frame, similarity_text, (x, y+h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#         cv2.imshow('Face Detection', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()


# while True:
#     print("Welcome to the face recognition system!")
#     print("1. Capture and Register")
#     print("2. Detect")
#     print("3. Quit")
#     choice = input("Enter your choice (1/2/3): ")
#     if choice == '1':
#         capture_and_register()
#     elif choice == '2':
#         name = input("Enter your name: ")
#         age = input("Enter your age
