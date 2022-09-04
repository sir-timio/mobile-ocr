from dataclasses import dataclass


@dataclass
class HKRDatasetConfig:
    device: str
    path_to_ds: str
    charset_path: str
    blank_symbol: str
    batch_size: int
    max_len: int
    img_channels: int
    img_height: int
    img_width: int
    resize_factor: int
    img_folder: str = ''
    train_frac_usage: float = 1
    shuffle: bool = False
    num_workers: int = 0
    max_ratio: float = None
    need_preproc: bool = False
    seed: int = 42
