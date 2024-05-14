from __future__ import absolute_import
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
        self.detector = YOLO('runs/detect/train2/weights/best.pt')

        

    def detect(self, frame: MatLike) -> dict:

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.detector.predict(img, conf=0.825)

        #{
            # pos: (x1, x2, y1, y2)
            # kpt: [ ... ] keypoints
            # prob: % probability
        #}

        result_dict = {
            'human-no-gun': [],
            'human-w/-gun': [],
        }
        i = results[0].plot()
        cv2_imshow(img=i)
        
    
    # Filter a classified object by confidence
    @staticmethod
    def _filter_by_conf(object, conf_thresh):
        if object.conf < conf_thresh: return False
        return True


    @staticmethod
    def _obb_get_pos(obb):
        pass

detector = ObjDetector()

p = Path(__file__).parent

img = cv2.imread(p/'test4.png')

detector.detect(img)