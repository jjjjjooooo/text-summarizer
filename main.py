from src.pipeline.stage_data_ingestion import DataIngestionTrainingPipeline
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
