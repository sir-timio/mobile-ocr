from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
from collections import namedtuple
import cv2
from torch.utils.data import Dataset, DataLoader, Subset
import torch
import json
Sample = namedtuple('Sample', 'label, path, h, w, label_len')


class HKRDataset(Dataset):
    def __init__(self, config: dataclass):
        """Init torch dataset

        Args:
            config (dataclass): see app/configs/_dataclasses
        """
        super(HKRDataset, self).__init__()
        self.config = config
        self.device = config.device
        self.path_to_ds = config.path_to_ds
        self.img_folder = config.img_folder
        self.blank_symbol = config.blank_symbol
        self.charset_path = config.charset_path

        self.batch_size = config.batch_size
        self.shuffle = config.shuffle
        self.num_workers = config.num_workers

        self.max_len = config.max_len

        self.channels = config.img_channels
        self.height = config.img_height
        self.width = config.img_width
        self.resize_factor = config.resize_factor
        self.max_ratio = config.max_ratio
        self.t_h = int(self.height / self.resize_factor)
        self.t_w = int(self.width / self.resize_factor)

        self.train_frac_usage = config.train_frac_usage
        np.random.seed = config.seed
        self.preprocessors_funcs = []
        if config.need_preproc:
            self.preprocessors_funcs.append(self.preprocess_img)
        elif self.resize_factor and self.resize_factor != 1:
            self.preprocessors_funcs.append(self.resize_img_keep_aspect)
        self.preprocessors_funcs.append(self.normalize_img)

        self.samples = self._read_data()

        self._set_mapping()

    def _set_mapping(self):
        """ makes encoder and decoder for labels

            Returns:
            None
        """
        with open(self.charset_path, 'r', encoding="utf-8") as f:
            d = json.load(f)
        self.char_to_num = dict()
        self.num_to_char = dict()
        for k, c in d.items():
            i = int(k)
            self.num_to_char[i] = c
            self.char_to_num[c] = i

        self.blank_index = self.char_to_num[self.blank_symbol]

    def get_train_val_loaders(self):
        """create train valid Dataloaders

        Returns:
            list of Dataloaders: [train_loader, val_loader]
        """

        datasets = {}
        datasets['train'] = Subset(self, self.train_idx)
        datasets['val'] = Subset(self, self.val_idx)
        return [DataLoader(ds, batch_size=self.batch_size,
                           shuffle=self.shuffle, num_workers=self.num_workers)
                for ds in datasets.values()]

    def _read_data(self):
        samples = []
        self.train_idx = []
        self.val_idx = []
        self.test_idx = []
        """make list of samples with fields label, path, h, w, label_len

        Returns:
            [Sample]: list of samples
        """
        ann = pd.read_csv(os.path.join(self.path_to_ds, 'ann.csv'))
        self.img_folder_path = os.path.join(self.path_to_ds, self.img_folder)
        # don't change to "i, row" cause skip some with bad ratio
        # maybe fix with pd.series
        i = 0
        for _, row in ann.iterrows():
            h, w = row['height'], row['width']

            if self.max_ratio and w / h > self.max_ratio:
                continue

            if row['part'] == 'train':
                if np.random.rand() > self.train_frac_usage:
                    continue
                self.train_idx.append(i)
            elif row['part'] == 'val':
                self.val_idx.append(i)
            else:
                self.test_idx.append(i)

            samples.append(Sample(
                label=row['label'],
                path=os.path.join(self.img_folder_path, row['path']),
                h=row['height'],
                w=row['width'],
                label_len=row['label_len']
            ))
            i += 1
        return samples

    def __len__(self):
        """len of Dataset

        Returns:
            int: len(samples)
        """
        return len(self.samples)

    def read_sample_img(self, i):
        img_path = self.samples[i].path
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        return np.array(img, dtype=np.float)

    def resize_or_pad_width(self, img, width):
        h, w = img.shape
        if w > self.t_w:
            img = self.resize_img_keep_aspect(img, height=h, width=width)
        else:
            img = self.pad_img_width(img, width=width)
        return img

    def preprocess_img(self, img):
        h, w = img.shape
        img = self.resize_img_keep_aspect(img, height=self.t_h)
        img = self.resize_or_pad_width(img, width=self.t_w)
        return img

    def resize_img_keep_aspect(self, img, height=None, width=None, ratio=None):
        h, w = img.shape
        dim = None
        if ratio:
            dim = (w / ratio, h / ratio)
        elif width and height:
            dim = (width, height)
        elif height:
            r = height / float(h)
            dim = (int(w * r), height)
        elif width:
            r = width / float(w)
            dim = (width, int(h * r))
        else:
            dim = (w // self.resize_factor, h // self.resize_factor)
        return cv2.resize(img, dim, cv2.INTER_AREA)

    def pad_img_width(self, img, width, white_v=255, center=False):
        pad_v = white_v if np.mean(img) > white_v / 2 else 0
        _, w = img.shape[:2]
        diff_hori = width - w
        if center:
            pad_left = diff_hori//2
        else:
            pad_left = 0
        pad_right = diff_hori - pad_left
        img = cv2.copyMakeBorder(img, 0, 0,
                                 pad_left, pad_right,
                                 cv2.BORDER_CONSTANT, value=pad_v)
        return img

    def pad_img(self, img, white_v=255, center=False):
        pad_v = white_v if np.mean(img) > white_v / 2 else 0
        h, w = img.shape[:2]
        diff_vert = self.height - h
        if center:
            pad_top = diff_vert//2
        else:
            pad_top = 0
        pad_bottom = diff_vert - pad_top

        diff_hori = self.width - w
        if center:
            pad_left = diff_hori//2
        else:
            pad_left = 0
        pad_right = diff_hori - pad_left
        img = cv2.copyMakeBorder(img, pad_top, pad_bottom,
                                 pad_left, pad_right,
                                 cv2.BORDER_CONSTANT, value=pad_v)
        return img

    def normalize_img(self, img):
        img /= 255
        img -= 0.5
        return img

    def pad_label(self, label):
        return np.pad(
            np.vectorize(self.char_to_num.get)(list(label)),
            (0, self.max_len - len(label)),
            mode='constant', constant_values=self.blank_index
        )

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

        img = self.read_sample_img(i)
        for f in self.preprocessors_funcs:
            img = f(img)
        img = np.expand_dims(img, axis=0)

        label = self.pad_label(self.samples[i].label)

        return {
            'images': torch.tensor(img, dtype=torch.float).to(self.device),
            'labels': torch.tensor(label, dtype=torch.float).to(self.device)
        }
