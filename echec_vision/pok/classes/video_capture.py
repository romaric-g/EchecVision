import cv2
import queue
import threading
import time

# bufferless VideoCapture


class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


class VideoTimeSimultation:

    is_started = False
    image_index = -1

    def __init__(self, name, frame_rate):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        self.frame_rate = frame_rate
        self.frame_time = 1 / frame_rate

    def start(self):
        self.is_started = True
        self.start_time = time.time()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def isOpened(self):
        return self.is_started

    def release(self):
        self.is_started = False
        self.image_index = -1

    def _time_to_index(self):
        return self.image_index * self.frame_time

    def _time_from_start(self):
        current_time = time.time()
        return current_time - self.start_time

    def _read_next_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            raise Exception("no_frame")

        if not self.q.empty():
            try:
                self.q.get_nowait()   # discard previous (unprocessed) frame
            except queue.Empty:
                pass

        self.image_index = self.image_index + 1
        self.q.put(frame)

    def _reader(self):
        while True:
            time_remain = self._time_from_start() - self._time_to_index()

            frame_remain = time_remain / self.frame_time

            if frame_remain < 1:
                continue

            try:
                self._read_next_frame()
            except:
                break

    def read(self):
        if self.q.empty():
            return False, None
        return True, self.q.get()


class VideoCaptureImageSimulation:

    def __init__(self, path, extension='png', first_idx=1):
        self.path = path
        self.idx = first_idx - 1
        self.extension = extension

    def read(self):

        self.idx = self.idx + 1

        image_path = self.path + str(self.idx) + '.' + self.extension

        return cv2.imread(image_path)
