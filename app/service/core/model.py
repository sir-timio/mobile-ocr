import torch

class HTRModel:
    """
    Класс, хранящий модель
    """

    def __init__(self, config) -> None:
        self.config = config
        self.model = torch.jit.load(config['model_path'], config['device'])
        self.device = config['device']
        self.vocab = self.model.vocab
        self.blank = self.model.blank
        self.input_img_shape = self.model.input_img_shape
        self.input_img_channels = self.input_img_shape[0]
        self.input_img_height = self.input_img_shape[1]
        self.input_img_width = self.input_img_shape[2]

    
    def get_model_input_shape(self):
        """
        Returns:
            list: shape in order [channel, height, width]
        """
        return self.input_img_shape
    
    def forward(self, img: torch.tensor):
        img = img.expand([1, *img.shape])
        return self.model.forward(img)
