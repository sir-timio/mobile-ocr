from dependency_injector import containers, providers
from service.core.core import HTR


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    htr = providers.Factory(HTR, config=config.htr)
