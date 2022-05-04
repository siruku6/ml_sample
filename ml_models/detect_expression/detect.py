from typing import List

import numpy as np
from PIL import Image
import pytorch_lightning as pl
import torch
from torchvision.models import resnet18
from torchvision import transforms

from config import logger
from ml_models.model_initializer import ModelInitializer


class ClassifyFacialExpressionNet(pl.LightningModule):
    def __init__(self, mixup_alpha: float = None):
        super().__init__()
        self.resnet = resnet18(pretrained=True)
        self.fc1 = torch.nn.Linear(1000, 7)
        self.fc2 = torch.nn.Linear(7, 3)
        self.mixup_alpha = mixup_alpha

    def forward(self, x):
        h1 = self.resnet(x)
        h2 = self.fc1(h1)
        h3 = self.fc2(h2)
        return h3


# class ModelInitializer:
#     def __init__(self):
#         if not os.path.isfile(MODEL_FILE_PATH):
#             model_initializer.load(
#                 bucket=BUCKET_NAME,
#                 source_filepath=MODEL_FILE_NAME,
#                 target_filepath=MODEL_FILE_PATH,
#             )

#     def load_model(self) -> ClassifyFacialExpressionNet:
#         # 推論モードへの切り替え .eval()
#         net: ClassifyFacialExpressionNet = ClassifyFacialExpressionNet().cpu().eval()
#         net.load_state_dict(torch.load(MODEL_FILE_PATH))
#         return net


class Detection:
    def __init__(self):
        BUCKET_NAME: str = 'fer2013'
        MODEL_SOURCE_NAME: str = 'fer_3_classes_model.pt'
        MODEL_FILE_PATH: str = f'ml_models/detect_expression/{MODEL_SOURCE_NAME}'
        initializer: ModelInitializer = ModelInitializer(
            BUCKET_NAME, MODEL_SOURCE_NAME, MODEL_FILE_PATH
        )
        self.net: ClassifyFacialExpressionNet = initializer.init_model(
            network_class=ClassifyFacialExpressionNet
        )
        self.class_names: List[str] = ['negative', 'neutral', 'positive']

    def run(self, image_name: str) -> float:
        path: str = self._image_file_path(image_name)
        image = self._prepare_image(path)
        with torch.no_grad():
            y = self.net(image)

        # cls: int = np.argmax(result)  # 今回は不要
        logger.info(f'detection result: {y}')

        # NOTE: 行列の積を求め、 0 ~ 1 の範囲の値を出力
        positive_level: np.ndarray = torch.matmul(
            y.softmax(dim=-1), torch.tensor([0.0, 0.5, 1.0])
        ).detach().numpy()
        return round(float(positive_level[0]), ndigits=2)  # , self.class_names[cls]

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
