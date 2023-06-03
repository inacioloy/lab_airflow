from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = {
        'owner': 'inacio',
        'depends_on_past': False,
        'start_date': datetime(2023, 1, 1),
        'email': ['airflow@airflow.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
      }

with DAG('dummy_dag', default_args=default_args) as dag:
    task_1 = DummyOperator(task_id='task_1')
    task_2 = DummyOperator(task_id='task_2')
    task_3 = DummyOperator(task_id='task_3')
    task_4 = DummyOperator(task_id='task_4')
    task_5 = DummyOperator(task_id='task_5')

    task_1 >> task_2 >> [task_3, task_4] >> task_5
