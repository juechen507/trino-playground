import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, Asset, AssetOrTimeSchedule, CronTriggerTimetable

dag1_asset = Asset("s3://dag1/output_1.txt", extra={"hi": "bye"})

with DAG(
    dag_id="asset_produces_1",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule="@daily",
    tags=["produces", "asset-scheduled"],
) as dag1:
    # [START task_outlet]
    BashOperator(outlets=[dag1_asset], task_id="producing_task_1", bash_command="sleep 5")
    # [END task_outlet]
