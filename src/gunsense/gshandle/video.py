import cv2
from pathlib import Path
from time import sleep

class VideoPlayer:

    def __init__(self, path: Path = None):
        self.path = self.__validate_path(path)


    def start(self, fps, handler):

        # Insanely high FPS will NOT work!
        if 120 <= fps <= 0:
            raise Exception("Provided framerate is too high or low.")

        # Instantiate the video stream
        try:
            player = cv2.VideoCapture(self.path)
        except Exception as e:
            raise Exception("Issue instantiating video player. Details:\n"+e)

        # Grab frame and pass to handler
        while player.isOpened():
            ret, frame = player.read()
            if not ret: break
            handler(frame)
            sleep(fps)

        player.release()


    def __validate_path(self, path: Path):

        # No path provided, assume live feed from device
        if not path:
            self.path = '0'

        # Path provided, check if it's a valid file
        elif path.exists() and path.is_file():
            self.path = str(path)

        else:
            raise Exception("Invalid path provided.")