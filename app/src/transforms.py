import torch
import math
import torchvision
import cv2
import random
import numpy as np


class RescalePaddingImage:
    def __init__(self, height, width, is_val=True, rng=None):
        self.rng = rng or np.random.default_rng()
        self.height = height
        self.width = width
        self.is_val = is_val

    def __call__(self, img):
        h, w = img.shape[:2]
        # width proportional to change in h
        r = self.height / float(h)
        new_w = int(w * r)
        # new_width cannot be bigger than width
        if new_w >= self.width:
            img = cv2.resize(img, (self.width, self.height), cv2.INTER_CUBIC)
        else:
            delta = self.width - new_w
            img = cv2.resize(img, (new_w, self.height), cv2.INTER_CUBIC)
            if self.is_val:
                pad_left = 0
                pad_right = delta
            else:
                pad_left = self.rng.integers(0, delta)
                pad_right = delta - pad_left
            
            
            pad_value = np.zeros(len(img.shape)) + np.median(img)
            img = cv2.copyMakeBorder(img, 0, 0,
                                    pad_left, pad_right,
                                    cv2.BORDER_CONSTANT, value=pad_value)

        return img


class Normalize:
    def __call__(self, img):
        img = img.astype(np.float32) / 255
        img = img - 0.5
        return img


class ToTensor:
    def __call__(self, arr):
        arr = np.expand_dims(arr, axis=0)
        return arr


class ToGrayscale:
    def __init__(self):
        pass
    
    def __call__(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


class MoveChannels:
    """Move the channel axis to the zero position as required in pytorch."""

    def __init__(self, to_channels_first=True):
        self.to_channels_first = to_channels_first

    def __call__(self, img):
        if self.to_channels_first:
            return np.moveaxis(img, -1, 0)
        else:
            return np.moveaxis(img, 0, -1)


class InferenceTransform:
    def __init__(self, height, width):
        self.transforms = get_val_transforms(height, width)

    def __call__(self, imgs):
        transformed_images = []
        for img in imgs:
            img = self.transforms(img)
            transformed_images.append(img)
        transformed_tensor = torch.stack(transformed_images, 0)
        return transformed_tensor


def get_val_transforms(height, width):
    transforms = torchvision.transforms.Compose([
        RescalePaddingImage(height, width, is_val=True),
        ToGrayscale(),
        Normalize(),
        ToTensor()
    ])
    return transforms
