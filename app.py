import cv2
import os
import streamlit as st
import face_recognition


def register():
    # Create a folder to store registered information if it does not exist
    if not os.path.exists("registered"):
        os.makedirs("registered")

    # Get the name, age, and gender of the person
    name = st.text_input("Name:")
    age = st.text_input("Age:")
    gender = st.selectbox("Gender:", ("Male", "Female"))

    # Load the default camera
    cap = cv2.VideoCapture(0)

    # Create a window for the camera view
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

    # Start capturing frames from the camera
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Show the frame in the window
        cv2.imshow("Camera", frame)

        # Wait for a key press event
        key = cv2.waitKey(1) & 0xFF

        # If the 'c' key is pressed, capture the frame and save it to disk
        if key == ord("c"):
            # Create a filename for the captured image
            filename = f"{name}_{age}_{gender}.jpg"

            # Save the captured image to the 'registered' folder
            cv2.imwrite(os.path.join("registered", filename), frame)

            # Release the camera and close the window
            cap.release()
            cv2.destroyAllWindows()

            # Print a message to the user
            st.write("Registration done!")
            break

        # If the 'q' key is pressed, exit the program
        elif key == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break


# Create a streamlit app
def app():
    st.title("Face Recognition App")

    # Add a button to start the registration process
    if st.button("Register"):
        # Call the 'register' function
        register()
