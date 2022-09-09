from pathlib import Path
import sys


import locale
locale.getpreferredencoding(False)

import torch
import cv2
import numpy as np
import pandas as pd
import pytest
from omegaconf import OmegaConf
from PIL import Image
import sys
sys.path.append('/workspace/handwritten_lines/ci-ctc-ocr/app/')
from run_app import create_app
from service.core.core import HTR

folder_images = 'tests/test_data'
images = Path(folder_images).glob('*.jpg')
images = [str(i) for i in images]

def image_in_byte(image):
    fname = image
    image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
    Image.fromarray(image)
    flag, image_encoded = cv2.imencode('.png', image)
    return image_encoded.tobytes()


@pytest.fixture(scope='session')
def config():
    return OmegaConf.load('tests/config.yml')


@pytest.fixture(scope='session')
def model(config):  # noqa: WPS442
    model = HTR(config['htr'])
    input_data = torch.rand(model.input_img_shape)
    model.predict(input_data, need_preproc=False)
    return model


@pytest.fixture
def test_images_in_byte():
    return list(map(image_in_byte, images))


@pytest.fixture(scope='session')
def client():
    app = create_app()

    with app.test_client() as client:  # noqa: WPS442
        yield client

