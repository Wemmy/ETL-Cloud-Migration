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
python ./utils/extract.py

echo transform data
python ./utils/transform.py

echo load data to local
python ./utils/load.py

streamlit run app.py -- -l True


```

# AWS Deployment:

please note you have to set your local AWS config for using sam deploy

```cmd
echo this is for the extract lambda function
cd sam-first-lambda

sam build
sam deploy
```

For transformation and load, we use AWS web UI to set GLUE and lambda function.

- GLUE: -[transform.py]: tirggerred by GLUE Scheduled Trigger
- Lambda
  - [end_load](): triggerred by S3 put event
  - [merics_load](): triggerred by EventBridge (Cloud Watch Event)
  - [news_load](): triggerred by S3 put event

> [!NOTE]
> We currently use psycopg2 for load csv data which may not be the best practice. If you decide to follow this please configure your connection accordingly.
> GLUE uses [DynamicFrame](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html) which may not suitable for dealing with Json data. We convert back and forth between DynamicFrame and Spark Datafram for transformation, which may not be the ideal use case

Dockernize the app and deploy on EC2

```cmd
docker build -t streamlit .
docker run -p 8501:8501 streamlit
```
