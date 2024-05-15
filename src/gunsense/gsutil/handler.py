import logging
from gshandle import VideoPlayer, GSLogger
from gsobject import ObjectDetector
from time import time


ONE_MIN = 60

class handle:

    def __init__(self, 
                 video_input: str = None, 
                 fps = 2,
                 cons_thresh = 2,
                 log_frames=True):
        self._log_frames = log_frames
        self._detector = ObjectDetector()
        self._video_feed = VideoPlayer(video_input)
        self._logger = GSLogger()
        self._cons_thresh = cons_thresh
        self._last_checkin = time()
        self._last_detection = time()
        self._consecutive = 0

        self._video_feed.start(fps, self._handle)


    def _handle(self, frame, end=False):

        if end: 
            self._logger.close()
            return

        gunmen = self._detector.detect(frame)
        msg = "Potential gunman/men was detected!"

        # Reset the tally if 15 minutes have passed
        if time() - self._last_detection >= ( 15 * ONE_MIN ):
            self._consecutive = 0

        # At least one gunman detected, alert
        if gunmen and len(gunmen) > 0:
            self._logger.warning(msg)
            self._last_checkin = self._last_detection = time()
            self._consecutive += 1

        # No gunman/men
        else:

            if self._consecutive > 0:
                msg = "Previous detection was a potenial false alarm."
                self._logger.info(msg)

            # Perform a routine checkin
            elif time() - self._last_checkin >= ( 5 * ONE_MIN ):
                self._logger.info("Routine check-in: OK")
                self._last_checkin = time()

            # Reset consecutive detection tally
            self._consecutive = 0

        # Met the consecutive threshold and enabled logging
        if self._consecutive >= self._cons_thresh and self._log_frames:

            print(self._consecutive)

            for gunman in gunmen:
                self._logger.critical(msg)
                self._logger.img_log_handle.log(gunman)
            