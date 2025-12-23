import unittest
from src.detector import Detector

class TestDetector(unittest.TestCase):

    def setUp(self):
        self.detector = Detector(model_path='yolov8s.pt')

    def test_model_loading(self):
        self.assertIsNotNone(self.detector.model, "Model should be loaded successfully.")

    def test_detection(self):
        # Assuming we have a test image to pass for detection
        test_image = 'path/to/test/image.jpg'
        results = self.detector.detect(test_image)
        self.assertIsInstance(results, list, "Detection results should be a list.")
        self.assertGreater(len(results), 0, "There should be at least one detection.")

if __name__ == '__main__':
    unittest.main()