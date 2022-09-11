from typing import Dict, List
from dataclasses import dataclass
import json

import cv2
import numpy as np
import torch
from service.core.recognizer import Recognizer
from service.core.detector import Detector
from service.dataclasses.shape import Shape

class HTR:
    """
    Основной класс сервиса распознавания рукописного текста.
    """
    def __init__(self, config: dataclass):

        self.config = config
        self._setup_threads()
        self.recognizer = Recognizer(self.config['recognizer'])
        self.detector = Detector(self.config['detector'])

    def predict(self, img: np.ndarray) -> List[Shape]:
        """Распознавание текста на изображении

        Args:
            img (np.ndarray): input rgb image

        Returns:
            List[Shape]: list of shapes with labels and coords
        """
        shapes = []
        boxes = self.detector.predict(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        crops = []
        for box in boxes:
            box = np.array(box).astype(int)
            crops.append(img[box[1]:box[3], box[0]:box[2]])
        labels = self.recognizer.predict(crops)
        return shapes, labels


    def _setup_threads(self):
        """
        Ограничиваем количество потоков для непитоновских библиотек.
        """
        max_threads = self.config.max_threads
        cv2.setNumThreads(max_threads)
        torch.set_num_threads(max_threads)
