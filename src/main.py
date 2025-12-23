# Main entry point for the person detection based automated video collection system.

import os
import time
from .config import (
    STREAM_URL,
    CHECK_INTERVAL,
    NO_DETECT_TIMEOUT,
    START_FRAMES,
    OUTPUT_DIR,
    MAX_LENGTH,
    CHUNK_DURATION,
)
from .capture import Capture
from .detector import Detector
from .recorder import Recorder
from .logger import logger

def main():
    capture = Capture(STREAM_URL)
    detector = Detector()

    # Probe FPS and frame size (try a few times)
    probe_frame = None
    for _ in range(3):
        probe_frame = capture.read_frame()
        if probe_frame is not None:
            break
        time.sleep(1)

    fps = capture.get_fps()
    if probe_frame is not None:
        h, w = probe_frame.shape[:2]
        frame_size = (w, h)
    else:
        frame_size = capture.get_frame_size()

    recorder = Recorder(
        stream_url=STREAM_URL,
        output_dir=OUTPUT_DIR,
        max_length=MAX_LENGTH,
        chunk_duration=CHUNK_DURATION,
        fps=fps,
        frame_size=frame_size,
        no_detect_timeout=NO_DETECT_TIMEOUT,
    )

    is_recording = False
    consecutive_on = 0
    last_detect_ts = None

    while True:
        frame = capture.read_frame()
        if frame is None:
            logger.warning("프레임 읽기 실패, 재연결 중...")
            time.sleep(2)
            continue

        detected = detector.detect(frame)

        if detected:
            consecutive_on += 1
            last_detect_ts = time.time()
        else:
            consecutive_on = 0

        if not is_recording and consecutive_on >= START_FRAMES:
            recorder.start_recording()
            is_recording = True
            logger.info("녹화 시작")

        if is_recording:
            # write current frame to the active writer (video only)
            recorder.write_frame(frame)
            # 녹화 관련 조건 처리 (no-detect, max length, chunk 분할 등)
            recorder.check_recording_conditions(last_detect_ts)
            # If overall recording was stopped (writer released and session ended)
            if recorder.writer is None and recorder.record_start_ts is None:
                is_recording = False
                logger.info("녹화 상태: 중지")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()