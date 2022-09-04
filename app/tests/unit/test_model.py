import cv2
import numpy as np


def test_model_on_predict(model, test_images_in_byte):
    image = cv2.imdecode(np.frombuffer(test_images_in_byte[0], np.uint8), cv2.IMREAD_GRAYSCALE)
    predict = model.predict(image)
    assert predict is not None