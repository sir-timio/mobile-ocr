import cv2
import numpy as np


def test_model_on_predict(model, test_images_in_byte):
    img = cv2.imdecode(np.frombuffer(test_images_in_byte[0], np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    predict = model.predict(img)
    assert predict is not None