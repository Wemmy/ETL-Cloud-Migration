
 rem git clone

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

 echo sam deployment
 cd sam-first-lambda