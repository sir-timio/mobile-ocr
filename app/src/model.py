import torch
from torch import nn
from torch.nn import functional as F
from src.CNN.cnn_medium import CNN
from src.RNN.lstm import LSTM


class CTCModel(nn.Module):
    def __init__(self, config):
        """construct CTC model based on CRNN

        Args:
            config (dataclass):
                vocab_len (int): length of vocabulary included UNK and blank
                input_img_shape (list): img shape (1, height, width)
                RNN_config (dataclass): config for LSTM block
                CNN_config (dataclass): config for CNN block
        """
        super(CTCModel, self).__init__()
        self.vocab_len = config.vocab_len
        self.blank_index = self.vocab_len - 1
        self.loss_fn = nn.CTCLoss(
            blank=self.blank_index, zero_infinity=False, reduction='sum'
        )

        self.cnn = CNN(config.CNN_config)
        self.lstm = LSTM(config.RNN_config)

        self.input_img_shape = config.input_img_shape
        self.input_img_channels = self.input_img_shape[0]
        self.input_img_height = self.input_img_shape[1]
        self.input_img_width = self.input_img_shape[2]
        self.w_reduction = self.cnn.w_reduction
        self.h_reduction = self.cnn.h_reduction
        self.cnn_features = self.cnn.out_features
        self.lstm_features = self.lstm.features


        self.linear = nn.Sequential(
            nn.Linear((self.input_img_shape[1] // self.h_reduction)
                      * self.cnn_features, self.lstm_features),
            nn.Dropout(0.2)
        )

        self.output = nn.Linear(self.lstm_features, self.vocab_len)

    def compute_loss(self, preds, labels):
        """compute ctc loss

        Args:
            preds (torch.tensor): probability over timesteps prediction
            labels (torch.tensor): gt texts

        Returns:
            float: ctc loss
        """
        batch_size = labels.shape[0]
        log_probs = F.log_softmax(preds, 2)
        input_lengths = torch.full(
            size=(batch_size,), fill_value=log_probs.size(0), dtype=torch.int32
        )
        target_lengths = torch.tensor(
            [torch.sum(s != self.blank_index) for s in labels]
        )
        loss = self.loss_fn(
            log_probs, labels, input_lengths, target_lengths
        )
        return loss

    def forward(self, images):
        """pass forward model

        Args:
            images (torch.tensor): batch of images in shape of (bs, 1, w, h)


        Returns:
            x (torch.tensor): probability over timesteps model prediction
        """
        batch_size, c, h, w = images.size()
        x = self.cnn(images)

        x = x.permute(0, 3, 1, 2)
        x = torch.reshape(x, shape=(
            batch_size, w // self.w_reduction,
            h // self.h_reduction * self.cnn_features))
        x = self.linear(x)
        x = self.lstm(x)

        x = self.output(x)
        x = x.permute(1, 0, 2)

        return x


        