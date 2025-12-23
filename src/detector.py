class Detector:
    def __init__(self, model_path='yolov8s.pt'):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        from ultralytics import YOLO
        import torch

        if torch.cuda.is_available():
            print("GPU is available. Loading model to GPU.")
            model = YOLO(model_path).to('cuda')
        else:
            print("No GPU found. Loading model to CPU.")
            model = YOLO(model_path)
        
        return model

    def detect(self, frame, confidence_threshold=0.5):
        results = self.model.predict(source=frame, classes=[0], conf=confidence_threshold, verbose=False)
        detected = any(len(r.boxes) > 0 for r in results)
        return detected