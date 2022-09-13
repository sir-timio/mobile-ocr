import torch
import numpy as np
import math
import cv2
from service.utils.representer import Representer

class Detector:
    def __init__(self, config) -> None:
        self.config = config
        self.model = torch.jit.load(config['model_path'], config['device'])
        self.model.eval()
        self.device = config['device']
        self.mean = np.array(config['mean'])
        self.image_short_side = config['image_short_side']
        self.thresh = config['thresh']
        self.box_thresh = config['box_thresh']
        self.representer = Representer(thresh=self.thresh, box_thresh=self.box_thresh)

    def preprocess_img(self, img):
        original_shape = img.shape[:2]
        height, width= img.shape[:2]
        if height < width:
            new_height = self.image_short_side
            new_width = int(math.ceil(new_height / height * width / 32) * 32)
        else:
            new_width = self.image_short_side
            new_height = int(math.ceil(new_width / width * height / 32) * 32)
        img = cv2.resize(img, (new_width, new_height))
        img = img.copy().astype(np.float32)
        img -= self.mean
        img /= 255.
        tensor = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0)

        return tensor, original_shape
    
    def predict(self, img: np.ndarray):        
        h, w = img.shape[:2]
        batch = {'shape': [(h, w)]}
        with torch.no_grad():
            batch['image'] = torch.tensor(img).unsqueeze(0)
            tensor, original_shape = self.preprocess_img(img)
            pred = self.model(tensor.to(self.device))
        
        batch_boxes, batch_scores = self.representer(batch, pred, is_output_polygon=False)
        boxes, scores = batch_boxes[0], batch_scores[0]
        return boxes