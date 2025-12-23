import os
import time
from datetime import datetime
import cv2
from .logger import logger

class Recorder:
    def __init__(self, stream_url, output_dir, max_length=600.0, chunk_duration=20.0,
                 fps=25.0, frame_size=(640,480), no_detect_timeout=1.0, fourcc='mp4v'):
        self.stream_url = stream_url
        self.output_dir = output_dir
        self.max_length = max_length
        self.chunk_duration = chunk_duration
        self.no_detect_timeout = no_detect_timeout

        self.fps = float(fps)
        self.frame_size = tuple(map(int, frame_size))  # (width, height)
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)

        self.writer = None
        self.record_idx = 0
        self.record_start_ts = None      # overall recording session start
        self.writer_start_ts = None      # current file start

        os.makedirs(self.output_dir, exist_ok=True)

    def _make_output_path(self):
        today_folder = os.path.join(self.output_dir, datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(today_folder, exist_ok=True)
        ts = datetime.now().strftime("%H%M%S")
        path = os.path.join(today_folder, f"record_{self.record_idx:04d}_{ts}.mp4")
        return path

    def start_recording(self):
        # increment record index only when starting a new overall session
        if self.record_start_ts is None:
            self.record_idx += 1
            self.record_start_ts = time.time()

        path = self._make_output_path()
        # create writer for video only (no audio)
        self.writer = cv2.VideoWriter(path, self.fourcc, self.fps, self.frame_size)
        if not self.writer.isOpened():
            logger.error(f"Failed to open VideoWriter for {path}")
            self.writer = None
            return

        self.writer_start_ts = time.time()
        logger.info(f"Recording (video only) started -> {path}")

    def stop_recording(self, reason="", full_stop=True):
        if self.writer:
            try:
                self.writer.release()
            except Exception:
                pass
            self.writer = None

        if full_stop:
            # end overall session
            self.record_start_ts = None
            self.writer_start_ts = None
            logger.info(f"Recording stopped. Reason: {reason}")
        else:
            # only reset current writer (used for chunk rotation)
            self.writer_start_ts = None
            logger.info(f"Chunk writer stopped, will open new chunk. Reason: {reason}")

    def rotate_chunk(self):
        # rotate current writer into a new file but keep session timestamps
        if self.writer:
            self.stop_recording(reason="Chunk rotation", full_stop=False)
        # start a new writer (record_start_ts stays set)
        self.start_recording()

    def write_frame(self, frame):
        if self.writer is None:
            return
        # ensure frame has expected size; resize if necessary
        h, w = frame.shape[:2]
        expected_w, expected_h = self.frame_size
        if (w, h) != (expected_w, expected_h):
            frame = cv2.resize(frame, (expected_w, expected_h))
        self.writer.write(frame)

    def check_recording_conditions(self, last_detect_ts):
        now = time.time()

        if self.writer:
            # 1) maximum overall session length
            if self.record_start_ts and (now - self.record_start_ts) >= self.max_length:
                self.stop_recording("Maximum overall length reached", full_stop=True)
                return

            # 2) chunk duration exceeded -> rotate chunk (keep overall session)
            if self.writer_start_ts and (now - self.writer_start_ts) >= self.chunk_duration:
                logger.info("Chunk duration exceeded, rotating chunk file.")
                self.rotate_chunk()
                return

            # 3) no-detect timeout -> stop overall recording
            if last_detect_ts and (now - last_detect_ts) >= self.no_detect_timeout:
                self.stop_recording("No detection timeout exceeded", full_stop=True)
                return