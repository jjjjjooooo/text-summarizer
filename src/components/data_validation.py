import os
import sys
from src.utils.exception import CustomException
from src.utils.logger import logger
from src.entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exists(self):
        try:
            validation_status = None

            all_files = os.listdir(os.path.join("artifacts", "data_ingestion", self.config.UNZIPPED_FOLDER))

            for file in self.config.ALL_REQUIRED_FILES:
                if file not in all_files:
                    validation_status = False
                    logger.info(f"Data validation failed for {file}")
                    with open(self.config.STATUS_FILE, "a") as f:
                        f.write(f"Validation status: {validation_status} >>>>> {file}\n")
                else:
                    validation_status = True
                    logger.info(f"Data validation succeeded for {file}")
                    with open(self.config.STATUS_FILE, "a") as f:
                        f.write(f"Validation status: {validation_status} >>>>> {file}\n")
            return validation_status
        except Exception as e:
            raise CustomException(e, sys)
