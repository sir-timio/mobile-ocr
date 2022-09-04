from torch.utils.tensorboard import SummaryWriter
from submodule.OCR_metrics.OCR_metrics import get_metrics
from submodule.set_global_seed.set_global_seed import set_global_seed
from submodule.gpu_management.gpu_management import gpu_usage
import os
from pathlib import Path

import torch
import numpy as np

from configs.long_hkr_config import (
    dataset_config,
    model_config,
    exp_config,
)

import src.engine as engine
from src.datasets.hkr_dataset import HKRDataset
from src.model import CTCModel
from src.decoder import ctc_decode_predictions


@gpu_usage
def train():
    """
    general train function
    """
    tb_logdir = exp_config.tb_logdir
    logger = SummaryWriter(tb_logdir)

    checkpoint_path = exp_config.checkpoint_dir
    os.makedirs(Path(checkpoint_path).parent, exist_ok=True)

    best_loss = np.inf
    ds = HKRDataset(dataset_config)
    train_loader, val_loader = ds.get_train_val_loaders()
    # device = torch.device("cuda:0,1" if torch.cuda.is_available() else "cpu")
    model = CTCModel(config=model_config)
    # model = torch.nn.DataParallel(model, device_ids=[0, 1]).to(device)
    model.to('cuda')
    optim = None
    if exp_config.optim == 'AdamW':
        optim = torch.optim.AdamW(model.parameters(), lr=exp_config.lr)
    elif exp_config.optim == 'Adam':
        optim = torch.optim.Adam(model.parameters(), lr=exp_config.lr)
    elif exp_config.optim == 'Adagrad':
        optim = torch.optim.Adagrad(model.parameters(), lr=exp_config.lr)
    elif exp_config.optim == 'Adadelta':
        optim = torch.optim.Adadelta(model.parameters())

    assert optim, "NONE OPTIMIZER"

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optim, factor=exp_config.lr_factor,
        patience=exp_config.plato_patience, verbose=True
    )

    for epoch in range(exp_config.epochs):
        train_loss = engine.train_fn(model, train_loader, optim)
        valid_true, valid_pred, valid_loss = engine.eval_fn(model, val_loader)

        scheduler.step(valid_loss)

        if valid_loss < best_loss:
            best_loss = train_loss
            torch.save(model.state_dict(), checkpoint_path)

        ctc_decoded_pred = ctc_decode_predictions(valid_pred)

        metrics = get_metrics([g.detach().cpu().numpy()
                              for g in valid_true], ctc_decoded_pred)
        cer, wer, ser = np.mean(metrics['cer']), np.mean(
            metrics['wer']), np.mean(metrics['ser'])
        # tensorboard
        logger.add_scalar('loss/train', train_loss, epoch)
        logger.add_scalar('loss/val', valid_loss, epoch)
        logger.add_scalar('cer', cer, epoch)
        logger.add_scalar('wer', wer, epoch)
        logger.add_scalar('ser', ser, epoch)
        print(f'cer: {cer}, wer:{wer}, ser:{ser}')


if __name__ == '__main__':
    set_global_seed(exp_config.seed)
    train()
