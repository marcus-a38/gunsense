import cv2
from pathlib import Path
from time import time
from cv2.typing import MatLike
from typing import Callable

class VideoPlayer:

    def __init__(self, path: str):
        self.path = self.__validate_path(path)


    def start(self, fps: int, handler: Callable[[MatLike, bool], None]):

        self.path = 'src/gunsense/test.mp4'

        # Instantiate the video stream
        try:
            player = cv2.VideoCapture(self.path)
        except Exception as e:
            raise Exception("Issue instantiating video player. Details:\n"+e)
        
        

        if fps is not None:
            valid_fps = fps < 60 and fps >= 0.5
            assert valid_fps, f"Provided framerate `{fps}` is too high or low."
            player.set(cv2.CAP_PROP_FPS, fps)
        else:
            player.set(cv2.CAP_PROP_FPS, 1)

        # Grab frame and pass to handler
        while True:
            # Limit the framerate
            ret, frame = player.read()
            if not ret: break
            handler(frame)

        
        handler(frame=None, end=True)
        player.release()


    def __validate_path(self, path: str):

        print(path)

        # Assume live feed from device
        if path is None:
            self.path = 0

        else:
            _path = Path(path)
            
            if _path.exists() and _path.is_file():
                self.path = _path
            else:
                raise Exception("Invalid video file path provided.")