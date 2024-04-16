import cv2
import numpy as np
from GUI import cvhelpers as cvHelp
from tkinter import *
import mediapipe as mp
width = 640
height = 480
cB = (0, 0, 0)
cW = (255, 255, 255)
npframe = np.zeros([height, width, 3], dtype=np.uint8)
npframe[:, :] = cB

root = Tk()


fps = cvHelp.TrackFPS(.05)
gui = cvHelp.cvGUI(root, width, height)
gui.camStart()
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
def distance(point_1, point_2):
    """Calculate l2-norm between two points"""
    dist = sum([(i - j) * 2 for i, j in zip(point_1, point_2)]) * 0.5
    return dist


def myloop():
    ignore, frame = gui.cam.read()
    npframe[:, :] = cW
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
    cv2.putText(frame, str(int(fps.getFPS())).rjust(3) + str(' FPS'), (0, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0),
                3)
    gui.displayImg(frame)
    #gui.displayNP(npframe)
    root.after(10, myloop)


myloop()
root.mainloop()