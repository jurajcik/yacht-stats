# yacht-stats
Statistics about prices of yachts in Croatia using the [Boataround.com API](https://api.boataround.com/). 

## Getting Started
 
- install [PostgreSQL DB](https://www.postgresql.org/)
  - create a DB to be used by yacht-stats
  - create a DB-user for the python app
  - create a DB-user for Grafana 
- install [Grafana](https://grafana.com/grafana/download?pg=get&plcmt=selfmanaged-box1-cta1)
  - configure the PostgreSQL DB as data source
- in [config.py property DB_STRING](yachtstats/config.py) configure the connection to the DB
- make sure to have python 3 and pipenv installed
- install dependencies with `pipenv install`
- run the script [main.py](yachtstats/main.py)
  - e.g. with `pipenv shell` and then `python yachtstats/main.py`
  - this will create the DB tables and execute the first collecting of data
- create SELECT grants to the tables for the Grafana user
- collect data regularly e.g. [set up daily scheduled task in windows](https://www.technipages.com/scheduled-task-windows)
  - there is a guard in place that tha data is not collected more often than [20 hours](yachtstats/config.py)
