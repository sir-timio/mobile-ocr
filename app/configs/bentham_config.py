import os
COMMON_DIR = '/dev_common'
PROJECT_NAME = 'torch-ocr'
EXPERIMENT_NAME = 'torch-ctc-bentham'
DATASET_DIR = f'{COMMON_DIR}/data/bentham'
CHECKPOINTS_DIR = f'{COMMON_DIR}/models/{PROJECT_NAME}/{EXPERIMENT_NAME}'
max_label_len = 110
DEVICE = "cuda"

CNN_config = {
    'out_features': 128
}

RNN_config = {
    'in_out_features': 256,
    'num_layers': 2
}

model_config = {
    'input_img_shape': [1, 128, 1024],
    'vocab_len': 87,
    'CNN_config': CNN_config,
    'RNN_config': RNN_config,
}


exp_config = {
    'checkpoints_dir': CHECKPOINTS_DIR,
    'epochs': 1000,
    'lr': 1e-3,
    'lr_factor': 0.9,
    'patience': 10,
    'seed': 42,
}

dataset_config = {
    'device': DEVICE,
    'path_to_ds': DATASET_DIR,
    'blank_symbol': '@',
    'batch_size': 8,
    'shuffle': False,
    'num_workers': 0,
    'max_len': max_label_len,
    'charset_path': os.path.join(DATASET_DIR, 'charset.txt')
}

task_config = {
    'project_name': 'ctc-ocr-torch',
    'task_name': 'bentham ds'
}
