import cv2
import time

class Capture:
    def __init__(self, url, retry_sleep=2):
        self.url = url
        self.retry_sleep = retry_sleep
        self.cap = self.open_capture()

    def open_capture(self):
        while True:
            cap = cv2.VideoCapture(self.url)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                return cap
            print("Failed to open capture, retrying...")
            time.sleep(self.retry_sleep)

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read frame, reconnecting...")
            time.sleep(2)
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = self.open_capture()
            return None
        return frame

    def release(self):
        try:
            self.cap.release()
        except Exception:
            pass

    def get_fps(self, fallback=25.0):
        try:
            fps = float(self.cap.get(cv2.CAP_PROP_FPS) or 0.0)
            if fps <= 0.0:
                return float(fallback)
            return fps
        except Exception:
            return float(fallback)

    def get_frame_size(self, fallback=(640,480)):
        try:
            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
            if w <= 0 or h <= 0:
                return tuple(fallback)
            return (w, h)
        except Exception:
            return tuple(fallback)