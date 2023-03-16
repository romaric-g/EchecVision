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



class VideoCaptureImageSimulation:

    def __init__(self, path, extension = 'png', first_idx = 1):
        self.path = path
        self.idx = first_idx - 1
        self.extension = extension

    def read(self):

        self.idx = self.idx + 1

        image_path = self.path + str(self.idx)  + '.' + self.extension

        return cv2.imread(image_path)