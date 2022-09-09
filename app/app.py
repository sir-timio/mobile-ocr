import os


import sys
sys.path.append('/app')

from flask import Flask
from omegaconf import OmegaConf
from service.containers import Container
from service.routes import recognition
from service.routes import health_check



def create_app():
    """
    Входная точка сервиса.
    """
    app = Flask(__name__)
    # работа с конфигами
    # инициализируем контейнер
    if not OmegaConf.has_resolver('weights_path'):
        OmegaConf.register_new_resolver('weights_path', _weights_path)
    cfg = OmegaConf.load(_abs_path('configs/config.yml'))
    container = Container()
    container.config.from_dict(cfg)
    container.wire(modules=[recognition])

    set_routes(app)
    return app


def set_routes(app: Flask):
    """
    Объявляем все роуты.
    """
    app.add_url_rule(
        '/health_check',
        'health_check',
        health_check.health_check,
        methods=['GET'],
    )
    app.add_url_rule(
        '/predict',
        'predict',
        recognition.predict,
        methods=['POST'],
    )



def _abs_path(local_path: str) -> str:
    proj_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(proj_dir, local_path)


def _weights_path(local_path: str) -> str:
    return os.path.join(_abs_path('weights'), local_path)


app = create_app()