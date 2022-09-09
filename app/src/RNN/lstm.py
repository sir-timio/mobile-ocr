from torch import nn


class LSTM(nn.Module):
    def __init__(self, config):
        """constuct lstm module

        Args:
            config (dataclass):
            in_out_features (int): the number of expected features
            in the input x
            num_layers (int): number of layers in RNN
            dropout (float): proba in [0, 1)
        """
        super(LSTM, self).__init__()
        self.features = config.in_out_features
        self.dropout = config.dropout
        self.features += self.features % 2
        self.num_layers = config.num_layers
        self.lstm = nn.LSTM(self.features, self.features//2,
                            bidirectional=True, num_layers=self.num_layers,
                            batch_first=True, dropout=self.dropout)

    def forward(self, x):
        """pass forward LSTM

        Args:
            x (torch.tensor): tensor in shape of (bs, timesteps, features)

        Returns:
            x (torch.tensor): tensor in shape of (bs, timesteps, features)

        """
        x, _ = self.lstm(x)
        return x
