# IITP_SmartHome_VideoCollection

## Overview
The IITP_SmartHome_VideoCollection is a Python application that captures video streams from an RTSP source and records video when a person is detected using the YOLO object detection model. This project is designed to be modular and maintainable, separating functionalities into distinct components.

## Project Structure
```
IITP_SmartHome_VideoCollection
├── src
│   ├── __init__.py
│   ├── main.py          # Entry point of the application
│   ├── config.py        # Configuration variables
│   ├── capture.py       # Video stream handling
│   ├── detector.py      # Object detection logic
│   ├── recorder.py      # Recording management
│   ├── logger.py        # Logging setup
│   └── utils.py         # Utility functions
├── tests
│   ├── test_detector.py  # Unit tests for the Detector class
│   └── test_recorder.py  # Unit tests for the Recorder class
├── requirements.txt      # Project dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore file
└── README.md             # Project documentation
```

## Installation
1. Clone the repository or unzip the file:
   ```
   git clone https://github.com/kaistmm/IITP_SmartHome_VideoCollection.git    # or unzip IITP_SmartHome_VideoCollection.zip
   cd IITP_SmartHome_VideoCollection
   ```

2. Create a virtual environment (optional but recommended):
   ```
   conda create -n {env_name} python=3.8
   conda activate {env_name}
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
- Fill `src/config.py` and update the values as needed, particularly the RTSP URL and any other sensitive information.

## Usage
To start the application, run the following command:
```
python -m src.main
```

The application will begin capturing video from the specified RTSP stream and will record video files when a person is detected.

## License

This project is licensed under the AGPL-3.0 License.