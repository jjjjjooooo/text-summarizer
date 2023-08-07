# End-to-End Text Summarization Project

## Introduction

The "End-to-End Text Summarization Project" is a comprehensive initiative focused on developing an NLP-based text summarizer. The project entails creating a robust pipeline that encompasses data ingestion, validation, transformation, model training, and evaluation. Using this pipeline, an app will be developed and deployed on AWS using a CI/CD workflow. The main goal of the project is to leverage this pipeline to automatically generate concise and accurate summaries from lengthy textual content, providing users with a dependable and efficient solution for text summarization.

* Model: t5-small
* Dataset: https://huggingface.co/datasets/samsum

## Workflow of the project

Create all the needed files and folders using template.py
Create a new virtual environment
Install packages using requirements.txt
Set up project using setup.py (automatically configured)

Update src/constants/__init__.py
Update src/utils/logger.py
Update src/utils/exception.py
Update src/utils/utils.py

Test project code using notebook

for each component in components:

    1. Test component code using notebook
    2. Update config.yaml
    3. Update params.yaml
    4. Update entity/__init__.py
    5. Update src/config/config.py
    6. Update src/components/component.py
    7. Update src/pipeline/stage_component.py
    8. Update main.py

Update src/pipeline/prediction.py
Update app.py
Update Dockerfile
Update .github/workflows/main.yaml

Create App
Deploy App


## AWS CICD deployment with Github


### 1. Login to AWS console

### 2. Create IAM user for deployment

* Create a new user with the following policies:

    1. AmazonEC2ContainerRegistryFullAccess

    2. AmazonEC2FullAccess

* Create and save the security credentials

	
### 3. Create ECR repo to store/save docker image
  
* Save the URL of ECR

### 4. Create EC2 virtual machine (Ubuntu)

### 5. Open EC2 and install docker in EC2 virtual Machine:
	
optinal

* sudo apt-get update -y

* sudo apt-get upgrade

required

* curl -fsSL https://get.docker.com -o get-docker.sh

* sudo sh get-docker.sh

* sudo usermod -aG docker ubuntu

* newgrp docker
	
### 6. Configure EC2 as self-hosted runner:

* github> setting> actions> runners> new self-hosted runner> choose os> run command one by one on EC2

* check the status of runners: idle -> connected

### 7. Setup github secrets

* github> setting> secrets and variables> actions> new repository secret> create the following parameters

    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_REGION
    AWS_ECR_LOGIN_URI
    ECR_REPOSITORY_NAME

### 8. Add the correct port to EC2