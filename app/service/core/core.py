from typing import Dict, List
from dataclasses import dataclass
import json

import cv2
import numpy as np
import torch
from service.core.recognizer import Recognizer
from service.core.detector import Detector
from service.dataclasses.shape import Shape
from service.utils.box_sorting import sort_boxes

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
        polygons = self.detector.predict(img)
        # polygons = sort_boxes(polygons)
        if len(polygons) == 0:
            return ''
        crops = []
        for poly in polygons:
            poly = np.array(poly).astype(int)
            box = self.poly_to_box(poly)
            crop = img[box[1]:box[3], box[0]:box[2]]
            if not all(crop.shape):
                continue
            crops.append(crop)
        labels = self.recognizer.predict(crops)

        return labels[0]

    def poly_to_box(self, polygon):
        pol = np.array(polygon)
        mins = np.min(pol, axis=0)
        maxs = np.max(pol, axis=0)
        return mins[0], mins[1], maxs[0], maxs[1]

    def _setup_threads(self):
        """
        Ограничиваем количество потоков для непитоновских библиотек.
        """
        max_threads = self.config.max_threads
        cv2.setNumThreads(max_threads)
        torch.set_num_threads(max_threads)
