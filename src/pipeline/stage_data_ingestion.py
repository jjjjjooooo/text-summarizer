from src.config.config import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.utils.logger import logger
from src.utils.exception import CustomException
import os
import sys


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        if not os.path.exists("artifacts/data_ingestion/data/"):
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()
