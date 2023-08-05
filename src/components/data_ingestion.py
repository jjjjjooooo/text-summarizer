import os
import sys
import urllib.request as request
import zipfile
from src.config.config import DataIngestionConfig
from src.utils.exception import CustomException
from src.utils.logger import logger
from src.utils.utils import get_size
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                filename, headers = request.urlretrieve(
                    url=self.config.source_URL, filename=self.config.local_data_file
                )
                logger.info(f"{filename} downloaded with following info: \n{headers}")
            except Exception as e:
                logger.exception(e)
                raise CustomException(e, sys)
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        try:
            with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
                zip_ref.extractall(unzip_path)
                logger.info(f"Unzip completed")
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)
