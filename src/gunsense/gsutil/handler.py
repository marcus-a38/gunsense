from gsobject import ObjectDetector
from gshandle import VideoPlayer
from gshandle import log, video
        

class handle:

    def __call__(self, 
                 video_input: str = None, 
                 fps = 5,
                 cons_thresh = 2,
                 log_frames=True):
        self._log_frames = log_frames
        self._detector = ObjectDetector()
        self._video_feed = VideoPlayer(video_input)
        self._logger = log.LoggedProcess()
        self._video_feed.start(fps, self._handle)
        self._consecutive = 0
        self._cons_thresh = cons_thresh

    @classmethod
    def _handle(self, frame):

        if self._detector.detect(frame):
            self._consecutive += 1

        else:
            self._consecutive = 0


        if not self._gun_detector.detect(frame): return
        if not self._await_aim and self._log_frames: 
            video.logframe(frame) #log POSSIBLE THREAT DETECTED - GUN
        if self._scan_aim: 
            if not self._pose_detector.detect(frame): return
        # log POSSIBLED THREAT DETECTED - AIMING/POINTING SUSPECTED GUN
            if self._log_frames: video.logframe(frame)

    def _report(self):

        pass