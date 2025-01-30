### Status Bi Task

## Tasks
One goal of the BI team is to design and implement dashboards to help Projects Lead have an overview of their project.
Those dashboards will be used for progress reporting, evaluating the project adoption, and identifying improvement. In the Database, you will find data extracted With those, create some indicators concerning:
* Issues distribution.
* The activity on different repositories.
* The Cost of the project.

## Thought process
The first thing was to explore the database and understand which tables would contribute to getting the required indicators. Postgres doesn't allow cross-platform reading of tables so I wrote a Python script to sync data from the remote connection to local Postgres in the docker container. Finally, I wrote the dbt models and created the visualizers.

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
To make the solution better a more detailed issue analytics which allows categorizes using GitHub issue labels, resource utilization tracking, and use of the data to build an ML model to predict future costs will be included. An issue I faced was that there were many tables, making it a bit more tasking.
