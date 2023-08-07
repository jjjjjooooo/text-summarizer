import os
import sys
from src.utils.exception import CustomException
from src.utils.logger import logger
from transformers import TrainingArguments, Trainer
from transformers import EarlyStoppingCallback
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
import torch
from src.entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
            logger.info("Tokenizer initialized")

            # Check if CUDA is available and select the device accordingly
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            # Move the model to the selected device (GPU)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt)
            logger.info("Model initialized")

            data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
            logger.info("Data Collator initialized")

            # loading data
            dataset_transformed = load_from_disk(self.config.data_path)
            logger.info("Dataset loaded")

            trainer_args = TrainingArguments(
                output_dir=self.config.root_dir,
                num_train_epochs=self.config.num_train_epochs,
                warmup_steps=self.config.warmup_steps,
                per_device_train_batch_size=self.config.per_device_train_batch_size,
                per_device_eval_batch_size=self.config.per_device_eval_batch_size,
                weight_decay=self.config.weight_decay,
                logging_steps=self.config.logging_steps,
                evaluation_strategy=self.config.evaluation_strategy,
                eval_steps=self.config.eval_steps,
                save_steps=1e6,
                gradient_accumulation_steps=self.config.gradient_accumulation_steps,
                load_best_model_at_end=True,
            )

            trainer = Trainer(
                model=model.to(device),
                args=trainer_args,
                tokenizer=tokenizer,
                data_collator=data_collator,
                train_dataset=dataset_transformed["train"],
                eval_dataset=dataset_transformed["validation"],
                callbacks=[EarlyStoppingCallback(early_stopping_patience=3, early_stopping_threshold=0.001)],
            )
            logger.info("Trainer initialized")

            trainer.train()
            logger.info("Training process finished")

            ## Save model
            model.save_pretrained(os.path.join(self.config.root_dir, "trained-model"))
            logger.info("Trained model saved")

            ## Save tokenizer
            tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))
            logger.info("Tokenizer saved")

        except Exception as e:
            raise CustomException(e, sys)
