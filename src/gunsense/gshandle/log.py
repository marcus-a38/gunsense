import logging
import logging.handlers as loghandlers
from datetime import datetime
from cv2 import imwrite
from cv2.typing import MatLike
from pathlib import Path
import os

DEFAULT_LOG_DIR = Path(__file__).parent / 'log'
DEFAULT_LOG_PATH = DEFAULT_LOG_DIR / 'gs.log'
ONE_MEGABYTE = 1_000_000

if not DEFAULT_LOG_DIR.exists(): DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)
if not DEFAULT_LOG_PATH.exists(): DEFAULT_LOG_PATH.touch()
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

class GSFileHandler(loghandlers.RotatingFileHandler):

    def __init__(self, path = DEFAULT_LOG_PATH):
        super().__init__(
            filename=path,
            mode='w',
            maxBytes=ONE_MEGABYTE,
            backupCount=5
        )

class GSImgHandler():
    
    def __init__(self, path = DEFAULT_LOG_DIR, use_jpeg=False):
        self.path = path
        self.use_jpeg = use_jpeg
        self.recent = None


    def log(self, img: MatLike):

        ext = '.png'
        if self.use_jpeg:
            ext = '.jpeg'
            
        # Get the current directory, change to img log path
        before = os.curdir
        os.chdir(fr"{str(self.path)}")

        # Write img to log directory with current timestamp as filename 
        name = self._get_stamp() + ext
        imwrite(name, img)
        self.recent = self.path / name

        # Return to original directory
        os.chdir(before)

    
    def undo(self):
        self.recent.unlink(True)


    @staticmethod
    def _get_stamp():
        return datetime.now().strftime("%Y-%m-%d %H%M%S")


class GSLogger(logging.Logger):

    def __init__(self, log_dir = DEFAULT_LOG_DIR):

        self.log_dir = log_dir
        self.file_log_handle = None
        self.img_log_handle = None
        super().__init__(__name__, level=logging.INFO)
        self._acquire()


    def new_file_logger(self):

        path = self.log_dir/'gs.log'

        logging.basicConfig(filename=path, level=logging.INFO)

        if self.file_log_handle: self.file_log_handle.close()

        formatting = logging.Formatter(
            '%(asctime)s | %(levelname)s: %(message)s'
        )
        self.file_log_handle = GSFileHandler(path)
        self.file_log_handle.formatter = formatting
        self.addHandler(self.file_log_handle)


    def new_img_logger(self):
        self.img_log_handle = GSImgHandler(self.log_dir)


    def close(self):
        self.file_log_handle.close()


    def _acquire(self):
        self.setLevel(logging.INFO)
        self.new_file_logger()
        self.new_img_logger()