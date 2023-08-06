from src.constants import *
from src.utils.exception import CustomException
from src.utils.logger import logger
from src.utils.utils import load_yaml, create_directories, get_size
from src.entity import DataIngestionConfig
from src.entity import DataValidationConfig
from src.entity import DataTransformationConfig


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = load_yaml(config_filepath)
        self.params = load_yaml(params_filepath)

        create_directories([self.config["artifacts_root"]])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config["data_ingestion"]

        create_directories([config["root_dir"]])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config["root_dir"],
            source_URL=config["source_URL"],
            local_data_file=config["local_data_file"],
            unzip_dir=config["unzip_dir"],
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config["data_validation"]

        create_directories([config["root_dir"]])

        data_validation_config = DataValidationConfig(
            root_dir=config["root_dir"],
            STATUS_FILE=config["STATUS_FILE"],
            ALL_REQUIRED_FILES=config["ALL_REQUIRED_FILES"],
            UNZIPPED_FOLDER=config["UNZIPPED_FOLDER"],
        )

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config["data_transformation"]

        create_directories([config["root_dir"]])

        data_transformation_config = DataTransformationConfig(
            root_dir=config["root_dir"],
            data_path=config["data_path"],
            tokenizer_name=config["tokenizer_name"],
            input_feature=config["input_feature"],
            target_feature=config["target_feature"],
        )

        return data_transformation_config
