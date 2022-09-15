from cv2 import resize
import torch
import numpy as np
from pyctcdecode import build_ctcdecoder
import cv2

class Recognizer:
    def __init__(self, config) -> None:
        self.config = config
        self.model = torch.jit.load(config['model_path'], config['device'])
        self.model.eval()
        self.device = config['device']
        self.in_img_channels = config['img_channels']
        self.in_img_height = config['img_height']
        self.in_img_width = config['img_width']
        self.input_img_shape = [self.in_img_channels, self.in_img_height, self.in_img_width]
        self.vocab = config['vocab']
        self.blank = config['blank']
        self.chars = self.vocab[:-1]
        self.num_to_char = dict()
        for i, c in enumerate(self.model.vocab):
            self.num_to_char[i] = c
        self.decoder = build_ctcdecoder(labels=list(self.chars))
        self.beam_width = 50
    
    def predict(self, imgs: np.ndarray):
        if len(imgs) == 0:
            return ''
        input_tensor = torch.stack([self.preprocess_img(i) for i in imgs])
        with torch.no_grad():
            output_tensor = self.model(input_tensor.to(self.device))
        labels = self.decode(output_tensor)
        return labels


    def preprocess_img(self, img: np.ndarray) -> torch.Tensor:
        if img.shape[-1] in [0,3]:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        h, w = img.shape[:2]
        # width proportional to change in h
        r = self.in_img_height / float(h)
        new_w = int(w * r)
        # new_width cannot be bigger than width
        if new_w >= self.in_img_width:
            img = cv2.resize(img, (self.in_img_width, self.in_img_height), cv2.INTER_CUBIC)
        else:
            delta = self.in_img_width - new_w
            img = cv2.resize(img, (new_w, self.in_img_height), cv2.INTER_CUBIC)
            pad_left = 0
            pad_right = delta

            pad_value = np.zeros(len(img.shape)) + np.median(img)
            img = cv2.copyMakeBorder(
                img, 0, 0,
                pad_left, pad_right,
                cv2.BORDER_CONSTANT, value=pad_value
            )
        
        img = img.astype(np.float32) / 255
        img -= 0.5
        img = np.expand_dims(img, axis=0)
        tensor = torch.from_numpy(img).float()
        return tensor
    

    def decode(self, batch: torch.tensor):
        labels = []

        batch = torch.softmax(batch, 2)
        batch = [b.detach().cpu().numpy() for b in batch.moveaxis(0, 1)]
        for b in batch:
            beam_result = self.decoder.decode_beams(b, beam_width=self.beam_width)
            labels.append(beam_result[0][0])
        return labels