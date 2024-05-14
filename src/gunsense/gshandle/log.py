import logging
import logging.handlers as loghandlers
from datetime import datetime
from enum import Enum
from cv2 import imwrite
from cv2.typing import MatLike
from functools import partial, partialmethod 
from pathlib import Path
import os, sys
from ultralytics.engine.results import Results


def validate_path(path: Path, expected_file, create_notfound):
    if path.exists():
        return True
    else:
        if create_notfound:
            path.touch()


class GsFileLog(loghandlers.RotatingFileHandler):

    def __init__(self, path):
        super().__init__(
            filename=path,
            mode='w',
            maxBytes=0,
            backupCount=5
        )
        

class GsStdoutLog(logging.StreamHandler):

    def __init__(self):
        super().__init__(sys.stdout)


class GsImgLog():
    
    def __init__(self, path: Path, discard_old=True, use_jpeg=False):
        self.path = path
        self.use_jpeg = use_jpeg
        self.recent = None
        if discard_old: self._discard_old()


    def _discard_old(self):
        # Remove all log-like files in this path
        for file in self.path.glob('*.log.*'):
            file.unlink(True)


    def log(self, results: Results):

        img = results[0].plot()
        if self.use_jpeg:
            ext = '.jpeg'
            

        # Get the current directory, change to img log path
        before = os.curdir()
        os.chdir(self.path)

        # Write img to log directory with current timestamp as filename 
        name = self._get_stamp() + ".png"
        imwrite(name, img)
        self.recent = self.path / name

        # Return to original directory
        os.chdir(before)

    
    def undo(self):
        self.recent.unlink(True)


    @staticmethod
    def _get_stamp():
        return datetime.now().strftime("%Y-%m-%d %H%M%S")


class GSMasterLogger(logging.Logger):

    class Concern(Enum):
        GS_MODERATE    =   7
        GS_HEIGHTENED  =   8
        GS_CRITICAL    =   9


    def __init__(self, log_path: Path = None):

        if not log_path: self.log_path = Path('')


    def _set_levels(self):
        logging.addLevelName(self.Concern.GS_MODERATE, "GS_MODERATE")
        logging.addLevelName(self.Concern.GS_HEIGHTENED, "GS_HEIGHTENED")
        logging.addLevelName(self.Concern.GS_CRITICAL, "GS_CRITICAL")
        logging.Logger.gsmoderate = partialmethod(
            logging.Logger.log, logging.GS_MODERATE
        )
        logging.Logger.gsheightened = partialmethod(
            logging.Logger.log, logging.GS_HEIGHTENED
        )
        logging.Logger.gscritical = partialmethod(
            logging.Logger.log, logging.GS_CRITICAL
        )
        logging.trace = partial(logging.log, logging.GS_MODERATE)
        logging.trace = partial(logging.log, logging.GS_HEIGHTENED)
        logging.trace = partial(logging.log, logging.GS_CRITICAL)


    def new_file_logger(self, path):
        logger = GsFileLog(path)
        self.handlers.append(logger)


    def new_img_logger(self, path):
        logger = GsImgLog
        self.handlers.append(logger)


    def toggle_stdout(self):
        pass


    def _acquire(self):
        pass