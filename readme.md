 <div align="center">
  <p>
      <img src="https://github.com/Wemmy/ETL-Cloud-Migration/blob/main/excalidraw/pipeline.png"></a>
  </p>
</div>

## Overview

This project emphasizes a comprehensive cloud migration strategy, transitioning from developing a local Streamlit application to deploying the entire process on AWS. The purpose of this app is to display a financial dashboard, showcasing essential financial metrics and predictors of interest, thereby aiding in portfolio optimization and management.

## Highlights

- Fully replicated functionalities from Local to Cloud
- End-to-End pipline from data ingestion, transformation to serving data in app

## App Archetecture

- page1: market trends
  - indices movements
  - economica indicators (fed rate, cpi, retail sales, inflation, etc.)
  - key sectors (technology, retail, real estate, energy, ect.) news with sentiments analysis
- page2: individual stock trends
  - price movement
  - basic stats
  - statement movement (cashflow, income, balance)
- page3: efficinet frontier
  - porforlio distribution based on mean variance optimization

## requirement

- python
- streamlit
- docker
- airflow
- AWS-SAM (lambda function development)

## To Replicate

# Local Deployment:

clone the repo

```cmd
git clone {repo_url}
cd 'to/your/path'

echo install required python model
pip install -r requirement.py

echo spin up local db and airflow
docker-compose -f local_deployment/docker-compose.yaml build
docker-compose -f local_deployment/docker-compose.yaml up airflow-init
docker-compose -f local_deployment/docker-compose.yaml up -d

echo extract data
python local_deployment/extract.py

echo transform data
python local_deployment/transform.py

echo load data to local
python local_deployment/load.py

streamlit run app.py -- -l True
```

# Airflow

Two cadences:

- daily udpate for EOD price and news
- Monthly update for economic indicators and stock statements

# AWS Deployment:

please note you have to set your local AWS config for using sam deploy

```cmd
echo this is for the extract lambda function
cd sam-first-lambda

sam build
sam deploy
```

For transformation and load, we use AWS web UI to set GLUE and lambda function.

- GLUE:
  - [transform.py](https://github.com/Wemmy/ETL-Cloud-Migration/blob/main/aws_deployment/transform.py): tirggerred by GLUE Scheduled Trigger
- Lambda
  - [end_load.py](https://github.com/Wemmy/ETL-Cloud-Migration/blob/main/aws_deployment/end_load.py): triggerred by S3 put event
  - [merics_load.py](https://github.com/Wemmy/ETL-Cloud-Migration/blob/main/aws_deployment/merics_load.py): triggerred by EventBridge (Cloud Watch Event)
  - [news_load.py](https://github.com/Wemmy/ETL-Cloud-Migration/blob/main/aws_deployment/news_load.py): triggerred by S3 put event

> [!NOTE]
> We currently use psycopg2 for load csv data which may not be the best practice. If you decide to follow this please configure your connection accordingly.
> GLUE uses [DynamicFrame](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html) which may not suitable for dealing with Json data and RDS instance. We convert back and forth between DynamicFrame and Spark Datafram for transformation, which may not be the ideal use case

Dockernize the app and deploy on EC2

```cmd
docker build -t streamlit .
docker run -p 8501:8501 streamlit
```

# EC2 Deployment

- Prepare Your EC2 Instance

  - install docker (example by Ubuntu)

  ```cmd
  sudo apt-get update
  sudo apt-get install docker.io
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo usermod -aG docker ${USER}
  ```

  - install Aws cli following this [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
  - config your aws config

- Pull the Docker Image
  aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
  Replace your-region with your AWS region (e.g., us-west-2) and your-account-id with your AWS account ID.

Once authenticated, pull the Docker image from ECR using:

bash
Copy code
docker pull your-account-id.dkr.ecr.your-region.amazonaws.com/your-repository-name:your-tag
Replace your-repository-name with the name of your repository in Amazon ECR and your-tag with the tag of the image you want to pull. If you don’t specify a tag, Docker will pull the latest tag by default.

6. Run the Docker Image (Optional)
   After pulling the image, you can run it on your EC2 instance using:

bash
Copy code
docker run -d -p localPort:containerPort your-account-id.dkr.ecr.your-region.amazonaws.com/your-repository-name:your-tag
Replace localPort with the port on your EC2 instance you want to bind, containerPort with the port your application runs on within the Docker container, and adjust other details as necessary.
