from datetime import timedelta
import pandas as pd
import os, sys, inspect
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

args = {
    'owner': 'geni', # or 'admin'
    'depends_on_past': True
}
dag = DAG(
    dag_id='dynamic_dag',
    default_args=args,
    schedule_interval='@once',
    start_date=days_ago(1)
)

def create_dummy_task(dag, task_id='dummy_task'):
    return DummyOperator(dag=dag, task_id=task_id)

# CSV com lista de códigos PySpark a serem executados. O CSV contém duas colunas: `name` e `depends_on`.
df = pd.read_csv(f'{currentdir}/tasks.csv')

dic = {
    '_-_'.join(task.split('/')[-2:]).replace('.py', ''): BashOperator(
        dag=dag, 
        task_id='_-_'.join(task.split('/')[-2:]).replace('.py', ''), 
        trigger_rule='all_success', # 'all_done', 
        bash_command=f'unset PYSPARK_DRIVER_PYTHON && spark-submit {currentdir}/{task} > {currentdir}/{task.replace(".py", ".txt")}'
    ) for task in set(df['depends_on'].dropna().to_list() + df["name"].dropna().to_list())
}

# Cria a fila de execução de acordo com a ordem e dependências das tarefas no arquivo
for i in range(df.shape[0]):
    task_id = '_-_'.join(df['name'].iloc[i].split('/')[-2:]).replace('.py', '')
    if isinstance(df['depends_on'].iloc[i], str):
        task_depends_on_id = '_-_'.join(df['depends_on'].iloc[i].split('/')[-2:]).replace('.py', '')
        dic[task_depends_on_id] >> dic[task_id]
    else:
        dic[task_id]
    
if __name__ == "__main__":
    dag.cli()
