import os
import sys
from src.utils.exception import CustomException
from src.utils.logger import logger
from transformers import AutoTokenizer
from datasets import load_from_disk
from src.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_name)

    def convert_examples_to_features(self, batch):
        input_encodings = self.tokenizer(batch[self.config.input_feature], max_length=1024, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(batch[self.config.target_feature], max_length=1024, truncation=True)

        return {
            "input_ids": input_encodings["input_ids"],
            "attention_mask": input_encodings["attention_mask"],
            "label": target_encodings["input_ids"],
        }

    def convert(self):
        dataset = load_from_disk(self.config.data_path)
        dataset_transformed = dataset.map(self.convert_examples_to_features, batched=True)
        logger.info("Dataset transformation done.")
        dataset_transformed.save_to_disk(os.path.join(self.config.root_dir, "transformed_dataset"))
        logger.info("Transformed dataset saved")
