from configs._dataclasses.ModelConfig import (
    ModelConfig,
    CNNConfig,
    RNNConfig
)
from configs._dataclasses.ExpConfig import ExpConfig
from configs._dataclasses.DatasetConfig import HKRDatasetConfig

# GENERAL
COMMON_DIR = '/dev_common'
PROJECT_NAME = 'torch-ocr'
DEVICE = 'cuda'
# DATASET
DATASET_NAME = 'HKR'
BLANK = '#'
DATASET_DIR = f'{COMMON_DIR}/data/{DATASET_NAME}'
IMG_FOLDER = 'img'
NEED_PREPROC = True
CHARSET_DICT_PATH = f'{DATASET_DIR}/num_to_char.json'
MAX_LABEL_LEN = 50
BATCH_SIZE = 8
IMG_CHANNELS = 1
IMG_HEIGHT = 128
IMG_WIDTH = 1024
RESIZE_FACTOR = 2
IMG_SHAPE = [IMG_CHANNELS, IMG_HEIGHT, IMG_WIDTH]
TRAIN_FRAC_USAGE = 1


# MODEL
RESIZED_IMG_SHAPE = [IMG_CHANNELS,
                     IMG_HEIGHT // RESIZE_FACTOR,
                     IMG_WIDTH // RESIZE_FACTOR]
VOCAB_LEN = 75

# CNN
CNN_FEATURES = 128

# RNN
RNN_FEATURES = 256
RNN_NUM_LAYERS = 2
RNN_DROPOUT = 0.1

# EXPERIMENT
OPTIM = 'AdamW'
EXPERIMENT_NAME = f'{PROJECT_NAME}-{DATASET_NAME}-{OPTIM}-TEST'
CHECKPOINT_DIR = f'{COMMON_DIR}/models/{PROJECT_NAME}/{EXPERIMENT_NAME}'
TB_LOGDIR = f'{COMMON_DIR}/logs/{EXPERIMENT_NAME}'
PLATO_PATIENCE = 10
LR_FACTOR = 0.9
LR = 1e-3
EPOCHS = 10000
SEED = 42


model_config = ModelConfig(
    input_img_shape=RESIZED_IMG_SHAPE,
    vocab_len=VOCAB_LEN,
    CNN_config=CNNConfig(CNN_FEATURES),
    RNN_config=RNNConfig(
        in_out_features=RNN_FEATURES,
        num_layers=RNN_NUM_LAYERS,
        dropout=RNN_DROPOUT
    )
)


exp_config = ExpConfig(
    checkpoint_dir=CHECKPOINT_DIR,
    tb_logdir=TB_LOGDIR,
    epochs=EPOCHS,
    optim=OPTIM,
    lr=LR,
    lr_factor=LR_FACTOR,
    plato_patience=PLATO_PATIENCE,
    seed=SEED
)


dataset_config = HKRDatasetConfig(
    device=DEVICE,
    path_to_ds=DATASET_DIR,
    img_folder=IMG_FOLDER,
    charset_path=CHARSET_DICT_PATH,
    blank_symbol=BLANK,
    batch_size=BATCH_SIZE,
    max_len=MAX_LABEL_LEN,
    img_channels=IMG_CHANNELS,
    img_height=IMG_HEIGHT,
    img_width=IMG_WIDTH,
    resize_factor=RESIZE_FACTOR,
    need_preproc=NEED_PREPROC,
    seed=SEED,
    train_frac_usage=TRAIN_FRAC_USAGE
)
