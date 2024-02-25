 <div align="center">
  <p>
      <img src="https://github.com/Wemmy/yolov8_aimbot-main/blob/main/media/test.gif"></a>
  </p>
</div>
 
 rem git clone

 cd 'to/your/path'
 
 echo install required python model
 pip install -r requirement.py

 echo extract data
 python ./utils/extract.py

 echo transform data
 python ./utils/transform.py

 echo spin up local db and airflow
 docker-compose -f local_deployment/docker-compose.yaml build
 docker-compose -f local_deployment/docker-compose.yaml up airflow-init 
 docker-compose -f local_deployment/docker-compose.yaml up -d

 echo load data to local
 python ./utils/load.py
  
 streamlit run app.py -- -l True