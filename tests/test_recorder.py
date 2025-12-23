import unittest
from unittest.mock import patch, MagicMock
from src.recorder import Recorder

class TestRecorder(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_start_writer(self, mock_popen):
        recorder = Recorder()
        recorder.start_writer()
        self.assertIsNotNone(recorder.ffmpeg_process)
        mock_popen.assert_called_once()

    @patch('subprocess.Popen')
    def test_stop_writer(self, mock_popen):
        recorder = Recorder()
        recorder.start_writer()
        recorder.stop_writer("Test reason")
        self.assertIsNone(recorder.ffmpeg_process)

    def test_recording_state(self):
        recorder = Recorder()
        self.assertFalse(recorder.is_recording)
        recorder.start_writer()
        self.assertTrue(recorder.is_recording)
        recorder.stop_writer("Test reason")
        self.assertFalse(recorder.is_recording)

if __name__ == '__main__':
    unittest.main()