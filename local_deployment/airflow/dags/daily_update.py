from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from airflow.models import Variable

from extract import get_daily_data
from transform import daily_transformation
from load import daily_load

FMP_API_KEY = Variable.get("FMP_API_KEY", default_var=None)
ALPHA_API_KEY = Variable.get("ALPHA_API_KEY", default_var=None)
POSTGRES_CONFIG = Variable.get("POSTGRES_CONFIG", deserialize_json=True, default_var=None)

stocklist = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'NVDA',  'META', 'TSLA', 'AMD', 'GME', 'CSCO']

args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 11, 27),
    'email': ['wenmin961028@gmail.com'],
    'email_on_failure': True,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='daily_update',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
    params={"example_key": "example_value"},
) as dag:
    

    dummy_task_1 = DummyOperator(
        task_id='start',
    )

    extract = PythonOperator(
        task_id="extract", 
        python_callable=get_daily_data,
        op_kwargs={"API_KEY_FMP": FMP_API_KEY, "API_KEY_ALPHA":ALPHA_API_KEY, "stocklist": stocklist}
    )
    
    transform = PythonOperator(
        task_id="transform", 
        python_callable=daily_transformation
    )
    load = PythonOperator(
        task_id="load", 
        python_callable=daily_load
    )

    dummy_task_2 = DummyOperator(
        task_id='end',
    )
    
    dummy_task_1 >> load >> extract >> transform >> dummy_task_2

# if __name__ == "__main__":
#     dag.cli()