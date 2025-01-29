### Status Bi Task

## Tasks
One goal of the BI team is to design and implement dashboards to help Projects Lead have an overview of their project.
Those dashboards will be use for the progress reporting, evaluating the project adoption, and identify improvement. In the Database, you will find data extracted With those, create some indicators concerning:
* Issues distribution.
* The activity on different repositories.
* The Cost of the project.

## Thought process
The first thing was to explore the database and understand which tables will contribute to get the required indicators. Postgress doenst allow cross-plarform reading of tables so I wrote a python script to sync data from the remote connection to local postgres in the docker container.Finally I wrote the dbt models and created the vivualizers.

## Tools
* PostgreSQL database
* DBT
* Grafana

The database configuration:
* host: `recruitment.free.technology`
* port: `5432`
* user: 
* password: 
* database name: `recruitment_task`
* schemas: `raw_github`,`raw_finance`

## Requirements
* Have docker installed

## Usage
Add your db logins to the sync remote python file
* Run this docker command `make dbt-built`
* Open `localhost:3000` on your browser to acess grafana

## Next Steps
To make the solution better a more detailed issue analytics which allows categorizes using github issue labels, resource utlization tracking, and use the data to build an ml model to predict future cost will be included. An issue I faced is that they are a lot of tables which made it a bit more tasking.# Status-Bi-Task-2
