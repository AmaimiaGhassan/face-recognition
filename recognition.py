import face_recognition
import os, sys
import cv2
import numpy as np
import math
from PIL import Image
import psycopg2
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import logging

logging.basicConfig(filename='face_recognition.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

conn = psycopg2.connect(
    dbname="faces",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

def fetch_encodings_from_db():
    cursor.execute("SELECT name, encoding FROM face_encodings")
    rows = cursor.fetchall()
    encodings = []
    for row in rows:
        name, encoding_binary = row
        encoding = np.frombuffer(encoding_binary, dtype=np.float64)
        encodings.append((name, encoding))
    return encodings

def send_alert_email():
    gmail_user = 'sender gmail'
    gmail_app_password = 'insert your gmail app code'

    sent_from = gmail_user
    sent_to = "receiver gmail"
    sent_subject = "Alert email !"
    sent_body = f"An unknown person has been detected at {time.strftime('%Y-%m-%d %H:%M:%S')}"
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

def recognize_faces():
    known_face_encodings = []
    known_face_names = []
    last_email_time = 0
    email_interval = 60  # 1 minute

    encodings = fetch_encodings_from_db()
    for name, encoding in encodings:
        known_face_encodings.append(encoding)
        known_face_names.append(name)
        logging.info(f"Loaded encoding for {name}")

    # Open the camera
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = convertToRGB(frame)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])
                    logging.info(f"Match found: {name} with confidence {confidence}")
                else:
                    logging.info("No match found")
            else:
                logging.info("No known faces detected")

            if name == "Unknown":
                current_time = time.time()
                if current_time - last_email_time > email_interval:
                    send_alert_email()
                    last_email_time = current_time
                    logging.info(f"Unknown person detected and email sent at {time.strftime('%Y-%m-%d %H:%M:%S')}")

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()