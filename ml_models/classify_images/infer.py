from typing import List, Tuple

import numpy as np
from PIL import Image
import pytorch_lightning as pl
import torch
from torchvision.models import resnet18
from torchvision import transforms


class PredPostureNet(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.resnet = resnet18(pretrained=True)
        self.fc = torch.nn.Linear(1000, 4)

    def forward(self, x):
        h0 = self.resnet(x)
        h1 = self.fc(h0)
        return h1


class Inference:
    def __init__(self):
        # 推論モードへの切り替え .eval()
        self.net: PredPostureNet = PredPostureNet().cpu().eval()
        network_file_name: str = 'ml_models/classify_images/classify_posture_network.pt'
        self.net.load_state_dict(torch.load(network_file_name))
        self.class_names: List[str] = ['handstand', 'lying_down', 'sit', 'stand']

    def run(self, image_name: str) -> Tuple[np.ndarray, int]:
        path: str = self._image_file_path(image_name)
        image = self._prepare_image(path)
        y = self.net(image)

        # NOTE: 1行しかないので 0 で次元を落とす
        result: np.ndarray = y.softmax(dim=-1).detach().numpy()[0]
        cls: int = np.argmax(result)
        return np.round(result, decimals=4), self.class_names[cls]

    def _image_file_path(self, image_name: str) -> str:
        return f'media/images/{image_name}'

    def _prepare_image(self, path: str):
        transform = transforms.Compose([
            # ImageNetで学習したモデルを使うときは、256->224の変換が一般的
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            # PyTorch公式でもこのmean, stdが推奨されている
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        img = Image.open(path).convert('RGB')
        transformed_img = transform(img)
        img_torch = torch.stack([transformed_img])
        return img_torch
