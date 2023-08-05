from src.pipeline.stage_data_ingestion import DataIngestionTrainingPipeline
from src.pipeline.stage_data_validation import DataValidationTrainingPipeline
from src.utils.logger import logger
from src.utils.exception import CustomException
import os
import sys


STAGE_NAME = "Data Ingestion"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise CustomException(e, sys)


STAGE_NAME = "Data Validation"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise CustomException(e, sys)
