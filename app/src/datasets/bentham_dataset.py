import numpy as np
import pandas as pd
import os
from collections import namedtuple

from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader, Subset
import torch
Sample = namedtuple('Sample', 'gt_text, path')


class BenthamDataset(Dataset):
    def __init__(self, config):
        """ Init Bentham dataset

        Args:
            config (dict): dataset configuration with fields:

            'device': str,
            'path_to_ds': str/path,
            'blank_symbol': str,
            'batch_size': int,
            'shuffle': bool,
            'num_workers': int,
            'max_len': int,
            'charset_path': str/path
            }

            Returns:
            torch.nn.Dataset: BenthamDataset
        """
        super(BenthamDataset, self).__init__()
        self.device = config['device']
        self.path_to_ds = config['path_to_ds']
        self.blank_symbol = config['blank_symbol']
        self.charset_path = config['charset_path']

        self.batch_size = config['batch_size']
        self.shuffle = config['shuffle']
        self.num_workers = config['num_workers']

        self.max_len = config['max_len']
        self.samples = self._read_data()

        self._set_mapping()

    def _set_mapping(self):
        """ makes encoder and decoder for labels

            Returns:
            None
        """
        chars = ['UNK'] + open(self.charset_path, 'r',
                               encoding='utf-8').read().split('\n')
        self.char_to_num = dict(zip(chars, range(len(chars))))
        self.num_to_char = dict({v: k for k, v in self.char_to_num.items()})

        self.blank_index = self.char_to_num[self.blank_symbol]

    def get_train_valid_loaders(self, val_split=0.25):
        """create train valid Dataloaders with optional ration

        Args:
            val_split (float, optional): [ratio of valid]. Defaults to 0.25.

        Returns:
            [Dataloaders]: [train_loader, val_loader]
        """
        train_idx, val_idx = train_test_split(
            list(range(len(self))), test_size=val_split)
        datasets = {}
        datasets['train'] = Subset(self, train_idx)
        datasets['val'] = Subset(self, val_idx)
        return [DataLoader(ds, batch_size=self.batch_size,
                           shuffle=self.shuffle, num_workers=self.num_workers)
                for ds in datasets.values()]

    def _read_data(self):
        samples = []
        """make list of samples with fields gt_text and path

        Returns:
            [Sample]: list of samples
        """
        for spec in ['train', 'valid']:
            path_to_img = os.path.join(self.path_to_ds, 'img', spec)
            ann = pd.read_csv(os.path.join(
                self.path_to_ds, 'ann', spec + '.csv'))
            for i in range(len(ann)):
                samples.append(Sample(
                    gt_text=ann['gt_text'].values[i],
                    path=os.path.join(path_to_img, ann['path'].values[i])
                ))
        return samples

    def __len__(self):
        """len of Dataset

        Returns:
            int: len(samples)
        """
        return len(self.samples)

    def __getitem__(self, i):
        """get one item by index, read img
        and make compatible with pytorch
        (channel, height, width), encode pad label with blank

        Args:
            i (int): index of sample

        Returns:
            dict: {
                'images': torch.tensor(dtype=torch.float),
                'labels': torch.tensor(dtype=torch.float)
            }
        """
        img_path = self.samples[i].path
        # images saved in shape (1024, 128) (vertical)
        img = np.load(img_path)
        img = np.transpose(img)
        # make channel first
        img = np.expand_dims(img, axis=0)

        label = self.samples[i].gt_text
        label = np.pad(
            np.vectorize(self.char_to_num.get)(list(label)),
            (0, self.max_len - len(label)),
            mode='constant', constant_values=self.blank_index)

        return {
            'images': torch.tensor(img, dtype=torch.float).to(self.device),
            'labels': torch.tensor(label, dtype=torch.float).to(self.device)
        }
