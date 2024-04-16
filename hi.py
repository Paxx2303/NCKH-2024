import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from GUI import cvhelpers as cvHelp
import mediapipe as mp
def get_mediapipe_app(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
):
    """Initialize and return Mediapipe FaceMesh Solution Graph object"""
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=max_num_faces,
        refine_landmarks=refine_landmarks,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    return face_mesh
fps = cvHelp.TrackFPS(0.5)
class MainPage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller

        # Background image
        self.background_image = Image.open("page1.png")
        self.background_image = self.background_image.resize((320, 570))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        background_label = ttk.Label(self, image=self.background_photo)
        background_label.image = self.background_photo
        background_label.place(relwidth=1, relheight=1)

        # Start button
        start_button = ttk.Button(self, text="Start", command=self.start_application)
        start_button.place(relx=0.5, rely=0.9, anchor="center")

    def start_application(self):
        self.controller.show_frame(Page2)

class Page2(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller

        # Your code for Page2
        self.cv_frame = ttk.Frame(self)  # Create a frame to hold the OpenCV window
        self.cv_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Back button
        back_button = ttk.Button(self, text="Back", command=self.go_to_page1)
        back_button.place(relx=0.45, rely=0)

        # Start OpenCV loop
        self.start_opencv_loop()

    def go_to_page1(self):
        self.controller.show_frame(MainPage)

    def start_opencv_loop(self):
        # Function to run OpenCV loop
        fps = cvHelp.TrackFPS(.05)
        gui = cvHelp.cvGUI(self.cv_frame, 640, 480)  # Pass cv_frame instead of root
        gui.camStart()

        def myloop():
            ignore, frame = gui.cam.read()
            chosen_left_eye_idxs = [362, 385, 387, 263, 373, 380]
            chosen_right_eye_idxs = [33, 160, 158, 133, 153, 144]
            mouth_idxs = [191, 82, 312, 310, 13, 81, 95, 87, 317, 318, 14, 178]
            face = mp.solutions.face_mesh.FaceMesh()
            face = get_mediapipe_app()
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face.process(imgRGB)
            imgH, imgW, _ = frame.shape
            if results:
                for facelm in results.multi_face_landmarks:
                    for id, lm in enumerate(facelm.landmark):
                        ih, iw, ic = frame.shape
                        x, y = int(lm.x * iw), int(lm.y * ih)
                        if id in chosen_left_eye_idxs or id in chosen_right_eye_idxs:
                            cv2.circle(frame, (x, y), 1, (0, 255, 0), 1)
                        elif id in mouth_idxs:
                            cv2.circle(frame , (x, y), 1, (233, 255, 0), 1)
            cv2.putText(frame, str(int(fps.getFPS())).rjust(3) + str(' FPS'), (0, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 100, 0),
                        3)
            gui.displayImg(frame)
            self.controller.after(10, myloop)

        myloop()

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Multi-page Application")
        self.geometry("320x570")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
