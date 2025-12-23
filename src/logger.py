import logging
import os

def setup_logger(name, log_file, level=logging.INFO, console=True):
    """Function to set up a logger with a specified name and log file."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers on repeated imports
    if logger.handlers:
        return logger

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if console:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

# Module-level default logger (exported as `logger`)
_default_log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
os.makedirs(_default_log_dir, exist_ok=True)
_default_log_file = os.path.join(_default_log_dir, "app.log")

logger = setup_logger('video_collector', _default_log_file)