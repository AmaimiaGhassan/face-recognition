import cv2
from tkinter import *
from PIL import Image, ImageTk
import psycopg2
import numpy as np
import face_recognition
import smtplib
import time

def send_notification_email(username):
    gmail_user = 'abidiraoua828@gmail.com'
    gmail_app_password = 'epkx svnd cleh owyw'

    sent_from = gmail_user
    sent_to = "amaimiagha@gmail.com"
    sent_subject = "New user added"
    sent_body = f"A new user is added : {username} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="faces",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Open the camera
video_capture = cv2.VideoCapture(0)

# Function to get the current frame from the video feed
def get_frame():
    ret, frame = video_capture.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA), frame.shape

# Create a window
frame, shape = get_frame()
window = Tk()
window.title("Face capture")
window.geometry(f'{shape[1]}x{shape[0]}')  # Set the window size to the frame size

# Create a canvas for the video feed
canvas = Canvas(window, width=shape[1], height=shape[0])
canvas.pack()

# Global variable to store the image
imgtk = None

# Function to update the video feed
def update_image():
    global imgtk
    frame, _ = get_frame()  # Ignore the shape
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=NW, image=imgtk)
    window.after(1, update_image)

# Create a text field to enter the name of the person
entry = Entry(window)
entry_height = 40
entry.place(x=0, y=shape[0] - entry_height, width=shape[1] - 150, height=entry_height)
# create placeholder
entry.insert(0, 'Enter your name')
# remove placeholder when clicked
entry.bind("<Button-1>", lambda event: entry.delete(0, "end"))
entry.config(font=("Arial", 12))
entry.config(bd=3)

# Create a button to capture an image
btn = Button(window, text="Capture")
btn_width = 150
btn_height = 40
btn.place(x=shape[1] - 150, y=shape[0] - btn_height, width=btn_width, height=btn_height)
btn.config(font=("Arial", 12))
btn.config(bd=3)

# Function to capture an image, extract face encodings, and save them to PostgreSQL
def capture_image():
    frame, _ = get_frame()
    filename = entry.get()
    if not filename:  # If the entry is empty, use a default filename
        filename = 'captured_image'

    # Convert the image to RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if face_encodings:
        # Save the face encodings and locations to the database
        for face_encoding, face_location in zip(face_encodings, face_locations):
            cursor.execute(
                "INSERT INTO face_encodings (name, encoding, location) VALUES (%s, %s, %s)",
                (filename, face_encoding.tobytes(), str(face_location))
            )
        conn.commit()
        print(f"Saved encoding for {filename}")
        send_notification_email(filename)
    else:
        print(f"No face found for {filename}")

# Assign the capture_image function to the button's command
btn.config(command=capture_image)
# Start the video feed
update_image()

# Start the Tkinter event loop
window.mainloop()

# Release the camera and close the database connection when the window is closed
video_capture.release()
cursor.close()
conn.close()