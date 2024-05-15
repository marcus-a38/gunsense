from cv2.typing import MatLike
from ultralytics import YOLO
from pathlib import Path

model = Path(__file__).parents[3]/"runs/detect/train/weights/best.pt"

class ObjectDetector:
    def __init__(self):
        self.detector = YOLO(model)
        
        
    def detect(self, frame: MatLike) -> list[MatLike | None]:

        results = self.detector.predict(frame, conf=0.8, device=0, classes=[2])[0]
        
        boxes = results.boxes.xyxy.tolist()

        copy = frame.copy()
        gunmen = []

        for box in boxes:
            x1, y1, x2, y2 = (int(coord) for coord in box)
            gunmen.append(copy[y1:y2, x1:x2])
        
        return gunmen