from torch import nn
from collections import OrderedDict


class CNN(nn.Module):

    def __init__(self, config):
        """construct feature extraction cnn block with w_reduction
        and h_reduction

        Args:
            config (dict):
                out_features (int):  out_channels of last Conv2d
        """
        super(CNN, self).__init__()
        self.w_reduction = 4
        self.h_reduction = 4
        self.out_features = config.out_features
        self.cnn = nn.Sequential(OrderedDict([
            ('conv1', nn.Conv2d(1, 16, kernel_size=(3, 3), padding=1)),
            ('lrelu1', nn.LeakyReLU(inplace=True)),
            ('pool1', nn.MaxPool2d(kernel_size=(2, 2))),
            ('bn1', nn.BatchNorm2d(16)),

            ('conv2', nn.Conv2d(16, 32, kernel_size=(3, 3), padding=1)),
            ('lrelu2', nn.LeakyReLU(inplace=True)),
            ('pool2', nn.MaxPool2d(kernel_size=(2, 2))),
            ('bn2', nn.BatchNorm2d(32)),

            ('conv3', nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1)),
            ('lrelu3', nn.LeakyReLU(inplace=True)),
            ('bn3', nn.BatchNorm2d(64)),

            ('conv4', nn.Conv2d(64, 64, kernel_size=(3, 3), padding=1)),
            ('lrelu4', nn.LeakyReLU(inplace=True)),
            ('bn4', nn.BatchNorm2d(64)),

            ('conv5', nn.Conv2d(64, 128, kernel_size=(3, 3), padding=1)),
            ('lrelu5', nn.LeakyReLU(inplace=True)),

            ('bn5', nn.BatchNorm2d(128)),


            ('conv6', nn.Conv2d(128, self.out_features, kernel_size=(3, 3),
                                padding=1)),
            ('lrelu6', nn.LeakyReLU(inplace=True)),
            ('bn6', nn.BatchNorm2d(self.out_features)),
        ]))

    def forward(self, images):
        """pass forward CNN

        Args:
            images (torch.tensor): batch of images in shape of (bs, 1, w, h)
        Returns:
            torch.tensor: extracted features in shape (bs,
            self.out_features, w // w_reduction, h // h_reduction)
        """
        batch_size, channels, w, h = images.size()
        x = self.cnn(images)
        return x
