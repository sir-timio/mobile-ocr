from dataclasses import dataclass


@dataclass
class ExpConfig:
    checkpoint_dir: str
    tb_logdir: str
    epochs: int = 1000
    optim: str = 'AdamW'
    lr: float = 1e-3
    lr_factor: float = 0.9
    plato_patience: int = 20
    seed: int = 42
