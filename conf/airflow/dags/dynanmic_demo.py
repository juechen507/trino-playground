from datetime import datetime

from airflow.sdk import DAG, task


@task
def add_one(x: int):
    return x + 1


@task
def sum_it(values: list[int]):
    print(f"Total was {sum(values)}")


with DAG(dag_id="dynamic-map-simple", start_date=datetime(2022, 1, 1)) as dag:
    summed = sum_it(values=add_one.expand(x=[1, 2, 3, 4, 5]))
