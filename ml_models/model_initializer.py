import os

import boto3
import torch
import pytorch_lightning as pl

import config.logger as logger


class ModelInitializer:
    def __init__(self, bucket_name: str, model_source_name: str, model_target_path: str):
        self.model_target_path: str = model_target_path

        if os.path.isfile(model_target_path):
            logger.info('model file is already set on local server !')
        else:
            self._load_model_file(
                bucket=bucket_name,
                source_filepath=model_source_name,
                target_filepath=model_target_path,
            )
            logger.info(f'succeeded to load model file from {model_target_path} on AWS S3!')

    def init_model(self, network_class: pl.LightningModule) -> pl.LightningModule:
        # 推論モードへの切り替え .eval()
        net: pl.LightningModule = network_class().cpu().eval()
        net.load_state_dict(torch.load(self.model_target_path))
        return net

    def _load_model_file(self, bucket: str, source_filepath: str, target_filepath: str):
        client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        )
        client.download_file(bucket, source_filepath, target_filepath)
