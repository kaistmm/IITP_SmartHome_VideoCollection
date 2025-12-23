import os
from datetime import datetime

def create_output_directory(base_dir):
    today_folder = os.path.join(base_dir, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(today_folder, exist_ok=True)
    return today_folder

def get_timestamped_filename(base_dir, prefix, extension):
    ts = datetime.now().strftime("%H%M%S")
    return os.path.join(base_dir, f"{prefix}_{ts}{extension}")

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"