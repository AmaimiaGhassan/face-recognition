import tkinter as tk
from tkinter import PhotoImage
import subprocess
from recognition import recognize_faces

def run_capture():
    subprocess.run(["python", "capture.py"])

def run_recognition():
    recognize_faces()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Face Recognition Interface")
    window.geometry("600x400")

    # Load the background image
    bg_image = PhotoImage(file="background1.png")  # Replace with your image file path

    # Create a canvas and set the background image
    canvas = tk.Canvas(window, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(300, 0, image=bg_image, anchor="n")

    # Create a frame for the buttons
    frame = tk.Frame(window, bg="#f0f0f0")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Capture button
    capture_button = tk.Button(frame, text="Capture", command=run_capture, bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=10)
    capture_button.pack(side="left", padx=10, pady=10)

    # Enter button
    enter_button = tk.Button(frame, text="Enter", command=run_recognition, bg="#2196F3", fg="white", font=("Arial", 12), padx=20, pady=10)
    enter_button.pack(side="left", padx=10, pady=10)

    window.mainloop()