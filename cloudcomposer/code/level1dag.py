# DAG IDENTIFIER 
# DAG OWNER 
# SCHEDULE INTERVAL 
# START DATE 

# THREE IMPORTANT PARTS OF DAG 
# the DAG ID, the time you want to start the DAG, 
# and the interval—in other words, how you want to schedule the DAG. 
# the DAG ID needs to be unique for the entire Airflow environment.

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'jesse-mensah',
}
# For schedule_interval, it follows the CronJob scheduling format.
# it uses five numerical values that represent the following: 
# minute, hour, day(month), month, and day(week).
# An asterisk (*) means every. 
# For example, * * * * * means the DAG will run every minute,
# while 0 1 * * * means the DAG will run every day at 1:00 A.M.
# It's a little bit counter-intuitive if you're using Airflow 
# for the first time, so here's an illustration of this:
# Today is January 1, 2021, and I want to create a DAG that runs immediately today.
# I want it to be scheduled every day at midnight (0 0 * * *).
# What should I put as start_date in Airflow?
# start_date=datetime(2020, 12, 31)
# Airflow DAG runtime is a combination of both start_date and schedule_ interval. 
# if the start date is January 1 and scheduled at midnight, Airflow will know that midnight 
# on January 1 has already passed, and will start the scheduler tomorrow, on January 2 at midnight.
# if we want the DAG to start immediately on January 1, we need to tell Airflow
# that the start_date value is supposed to be December 31, 2020 or the day -1.
# instead of using the exact date, we will use a days_ago() function:
# This simply means that if you submit the DAG today for our exercise, the DAG will immediately run.
# other parameters are optional 
# the DAG owner, handling task errors, and other parameters.
# After learning about DAG, we will learn about tasks and operators. 
# A DAG consists of one or many tasks 
# A task is declared using operators.


with DAG(
    dag_id='hello_world_airflow',
    default_args=args,
    schedule_interval='0 5 * * *',
    start_date=days_ago(1),
) as dag:
# we will use two BashOperator instances, and both operators will print words.
# The first task will print Hello and the second task will print World, like this:
# BashOperator is one of many operators that are available for Airflow. 
# BashOperator is a simple operator for you to run Linux commands.
# Every operator has a task ID and other parameters, and the parameters are different for each operator.
# You need to check two things to use operators: first, what are the available 
# parameters; and second: how to import the operator. 
# The Python library directory is
# not consistent, so you need to check from the public documentation.
    print_hello = BashOperator(
        task_id='print_hello',
        bash_command='echo Hello',
    )

    print_world= BashOperator(
        task_id='print_world',
        bash_command='echo World',
    )
# Bitwise operators use >> to indicate task dependencies, like this:
# A task can be dependent on more than one task
    print_hello >> print_world

if __name__ == "__main__":
    dag.cli()

# GO TO CLOUD SHELL
# NAV TO PYTHON FILE DIRECTORY THAT CONTAINS DAG PYTHON FILE 
# gcloud composer environments storage dags import
# --environment firstcompoer
# --location us-central1 --source level1dag.py