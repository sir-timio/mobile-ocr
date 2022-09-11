import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from flask import request
from service.containers import Container
from service.core.core import HTR



@inject
def predict(service: HTR = Provide[Container.htr]):
    image = cv2.imdecode(np.frombuffer(request.data, np.uint8), cv2.IMREAD_COLOR)
    label = service.predict(image)
    return label

