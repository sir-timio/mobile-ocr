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
        self.detector = Recognizer(self.config['recognizer'])

    def predict(self, img: np.ndarray) -> List[Shape]:
        """Распознавание текста на изображении

        Args:
            img (np.ndarray): input image

        Returns:
            List[Shape]: list of shapes with labels and coords
        """
        shapes = []
        
        return shapes

    


    def _setup_threads(self):
        """
        Ограничиваем количество потоков для непитоновских библиотек.
        """
        max_threads = self.config.max_threads
        cv2.setNumThreads(max_threads)
        torch.set_num_threads(max_threads)
