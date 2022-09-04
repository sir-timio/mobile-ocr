from dataclasses import dataclass
from typing import List


@dataclass
class ModelConfig:
    input_img_shape: List
    vocab_len: int
    CNN_config: dataclass
    RNN_config: dataclass


@dataclass
class CNNConfig:
    out_features: int


@dataclass
class RNNConfig:
    in_out_features: int
    num_layers: int
    dropout: float
