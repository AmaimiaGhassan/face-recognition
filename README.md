# Face Recognition using opencv and Postresql

This project provides a graphical interface for capturing and recognizing faces using a webcam. It uses OpenCV for video capture, face_recognition for face detection and recognition, and Tkinter for the graphical interface.

## Project Structure


- `main.py`: The main interface for the application.
- `capture.py`: Captures images from the webcam and saves face encodings to a PostgreSQL database.
- `recognition.py`: Recognizes faces from the webcam feed using the saved encodings.

## Requirements

- Python 3.x
- OpenCV
- face_recognition
- Tkinter
- psycopg2
- Pillow

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
   cd YOUR_REPOSITORY_NAME

2. Install the required packages:
   ```sh
   pip install opencv-python face_recognition psycopg2 Pillow

3. Set up the PostgreSQL database:
   - Create a database named `faces`.
   - Create a table named 
```PSQL
face_encodings

 with columns 

name

, 

encoding

, and `location`.
```
## Usage

1. Run the main interface:
   ```sh
   python main.py
   ```

2. Use the "Capture" button to capture a new face and save its encoding to the database.

3. Use the "Enter" button to start the face recognition process.

## Logging

- capture.log: Logs related to the capture process.
- face_recognition.log: Logs related to the face recognition process.

## License

This project is licensed under the MIT License.
```
