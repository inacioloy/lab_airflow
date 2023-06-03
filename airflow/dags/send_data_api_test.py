import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def read_data_from_api():
    print("RODOU SERIALIZERS")
    # response = requests.get('https://api.example.com/data')
    data = {"A": "B"}
    return data


def serialize_data(**kwargs):
    ti = kwargs['ti']
    print("RODOU SERIALIZERS")
    data = ti.xcom_pull(task_ids='read_data_from_api')
    # Lógica para serializar os dados
    data_clean = data
    return data_clean


def send_data_to_api(**kwargs):
    ti = kwargs['ti']
    print("RODOU SEND DATA")
    serialized_data = ti.xcom_pull(task_ids='serialize_data')
    return {"status_code": 201}
    # Lógica para enviar os dados serializados para a API de destino


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

dag = DAG('interoperability_pipeline', default_args=default_args, schedule_interval='* * * * *')

read_task = PythonOperator(task_id='read_data_from_api', python_callable=read_data_from_api, dag=dag)
serialize_task = PythonOperator(task_id='serialize_data', python_callable=serialize_data, provide_context=True, dag=dag)
send_task = PythonOperator(task_id='send_data_to_api', python_callable=send_data_to_api, provide_context=True, dag=dag)

read_task >> serialize_task >> send_task
