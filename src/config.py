# Configuration variables for the video collection framework

STREAM_URL = "rtsp://~"      # RTSP stream URL (to be filled with actual URL)
CHECK_INTERVAL = 0.05        # Interval to check for detections
NO_DETECT_TIMEOUT = 1.0      # Timeout for no detection before stopping recording
MAX_LENGTH = 600.0           # Maximum recording length in seconds (10 minutes)
CHUNK_DURATION = 20.0        # Duration in seconds for each recorded chunk
START_FRAMES = 3             # Number of consecutive detections to start recording
OUTPUT_DIR = "./video_saved" # Directory to save recorded videos