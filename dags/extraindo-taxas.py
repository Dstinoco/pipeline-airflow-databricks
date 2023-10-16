from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime
from pytz import timezone
brasilia_tz = timezone('America/Sao_Paulo')


with DAG(
    'Executando-notebook-etl',
    start_date=datetime(2023, 8, 25, tzinfo=brasilia_tz),
        schedule_interval="20 11 * * *"  # Inicia às 11:15

    ) as dag_executando_notebook_extracao:



    extraindo_dados = DatabricksRunNowOperator(
    task_id = 'Extraindo-conversoes',
    databricks_conn_id = 'databricks_default',
    job_id = 307543230213856,
    notebook_params={"data_execucao": '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    
    )


    transformando_dados = DatabricksRunNowOperator(
    task_id = 'transformando_dados',
    databricks_conn_id = 'databricks_default',
    job_id = 421985359739676
    )

    enviando_relatorio = DatabricksRunNowOperator(
    task_id = 'enviando-relatorio',
    databricks_conn_id = 'databricks_default',
    job_id = 619895746953593
    )


    extraindo_dados >> transformando_dados >> enviando_relatorio
