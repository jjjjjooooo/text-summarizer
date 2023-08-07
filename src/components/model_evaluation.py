from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk, load_metric
import torch
import pandas as pd
from tqdm import tqdm
from src.entity import ModelEvaluationConfig
from src.utils.exception import CustomException
from src.utils.logger import logger
import sys


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def batch_iterator(self, element_list, batch_size):
        try:
            """split the dataset into smaller batches that we can process simultaneously
            Yield successive batch-sized chunks from list_of_elements."""
            for i in range(0, len(element_list), batch_size):
                yield element_list[i : i + batch_size]
        except Exception as e:
            raise CustomException(e, sys)

    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer, batch_size=16):
        try:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = model.to(device)
            article_batches = list(self.batch_iterator(dataset[self.config.input_feature], batch_size))
            target_batches = list(self.batch_iterator(dataset[self.config.target_feature], batch_size))

            for article_batch, target_batch in tqdm(zip(article_batches, target_batches), total=len(article_batches)):
                inputs = tokenizer(
                    article_batch, max_length=1024, truncation=True, padding="max_length", return_tensors="pt"
                )

                summaries = model.generate(
                    input_ids=inputs["input_ids"].to(device),
                    attention_mask=inputs["attention_mask"].to(device),
                    length_penalty=0.8,
                    num_beams=8,
                    max_length=128,
                )
                """ parameter for length penalty ensures that the model does not generate sequences that are too long. """

                # Finally, we decode the generated texts,
                # replace the  token, and add the decoded texts with the references to the metric.
                decoded_summaries = [
                    tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_spaces=True) for s in summaries
                ]

                # decoded_summaries = [d.replace("", " ") for d in decoded_summaries]

                metric.add_batch(predictions=decoded_summaries, references=target_batch)

            #  Finally compute and return the ROUGE scores.
            score = metric.compute()
            return score

        except Exception as e:
            raise CustomException(e, sys)

    def evaluate(self):
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
            logger.info("Tokenizer loaded")
            trained_model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path)
            logger.info("Model loaded")

            # loading data
            transformed_dataset = load_from_disk(self.config.data_path)
            logger.info("Test dataset loaded")

            rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

            rouge_metric = load_metric("rouge")
            logger.info("Metrics loaded")

            score = self.calculate_metric_on_test_ds(
                dataset=transformed_dataset["test"],
                metric=rouge_metric,
                model=trained_model,
                tokenizer=tokenizer,
                batch_size=50,
            )
            logger.info("Metrics calculated")

            rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)

            df = pd.DataFrame(rouge_dict, index=["text_summarizer"])
            df.to_csv(self.config.metric_file_name, index=False)
            logger.info("Metrics saved")

        except Exception as e:
            raise CustomException(e, sys)
