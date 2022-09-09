from typing import Dict, List
from dataclasses import dataclass
import json

import cv2
import numpy as np
import torch
from service.core.model import HTRModel


class HTR:
    """
    Основной класс сервиса распознавания рукописного текста.
    """

    def __init__(self, config: dataclass):

        self.config = config
        self._setup_threads()
        self.model = HTRModel(self.config['model'])
        self.input_img_height = self.model.input_img_height
        self.input_img_width = self.model.input_img_width
        self.input_img_shape = self.model.input_img_shape
        self.blank = self.model.blank
        self.decoder = dict()
        for i, c in enumerate(self.model.vocab):
            self.decoder[i] = c
        self.blank = self.decoder[len(self.decoder)-1]

    def predict(self, img: np.ndarray, need_preproc: bool = True) -> str:
        """Распознавание текста на изображении

        Args:
            img (np.ndarray): входное изображение

        Returns:
            str: предсказанный текст
        """
        # зачем создаём копию и сохраняем здесь же?
        if need_preproc:
            img = img.copy()
            img = self.preprocess_img(np.array(img))

        tensor = torch.tensor(img, dtype=torch.float)    
        raw_preds = self.model.forward(tensor)
        label = self.decode_predictions(raw_preds)[0]
        return label

    def preprocess_img(self, img):
        dim = (self.input_img_width, self.input_img_height)
        img = cv2.resize(img, dim, cv2.INTER_AREA)
        img = np.expand_dims(img, axis=0)
        img = img / 255
        img -= 0.5
        return img
    

    def decode_predictions(self, raw_preds):
        """ decode raw output batch from NN

        Args:
            raw_preds (torch.tensor): prediction in shape [T, B, M]
            T - timestemps
            B - batch size
            M - max label length

        Returns:
            List: labels of bathes
        """
        blank = raw_preds[0].shape[-1] - 1
        labels = []
        batch = raw_preds.permute(1, 0, 2)
        batch = torch.softmax(batch, 2)
        batch = torch.argmax(batch, 2)
        batch = batch.detach().cpu().numpy()
        for sample in batch:
            sample = [sample[0]] + \
                [c for i, c in enumerate(sample[1:]) if c != sample[i]]
            sample = list(filter(lambda i: i != blank, sample))
            label = ''.join([self.decoder[w.item()]
                for w in sample]).replace(self.blank, '')
            labels.append(label)
        
        return labels



    def _setup_threads(self):
        """
        Ограничиваем количество потоков для непитоновских библиотек.
        """
        max_threads = self.config.max_threads
        cv2.setNumThreads(max_threads)
        torch.set_num_threads(max_threads)

