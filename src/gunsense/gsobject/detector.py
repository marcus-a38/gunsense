import cv2
from cv2.typing import MatLike
from ultralytics import YOLO
from pathlib import Path

# For visualization purposes
def cv2_imshow(**kwargs):

    for window, img in kwargs.items():
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.imshow(window, img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

class ObjectDetector:
    def __init__(self):
        self.detector = YOLO(r'C:\Users\thor1\gunsense\runs\detect\train\weights\best.pt')
        
        
    def detect(self, frame: MatLike) -> list[MatLike | None]:

        results = self.detector.predict(frame, conf=0.8, device=0, classes=[2])[0]
        
        boxes = results.boxes.xyxy.tolist()

        copy = frame.copy()
        gunmen = []

        for box in boxes:
            x1, y1, x2, y2 = (int(coord) for coord in box)
            gunmen.append(copy[y1:y2, x1:x2])
        
        return gunmen
    
    # Filter a classified object by confidence
    @staticmethod
    def _filter_by_conf(object, conf_thresh):
        if object.conf < conf_thresh: return False
        return True


    @staticmethod
    def _obb_get_pos(obb):
        pass