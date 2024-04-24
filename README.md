# Databases. Laboratory work #3


## Base dataset

[**World Weather Repository**](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository)
was taken as the base dataset for the current laboratory work by the task.

### Used columns

Among all dataset columns, next were selected as base for the domain model of the laboratory project:

* `country` — country of the weather data
* `location_name` — name of the location (city)

* `latitude` — latitude coordinate of the location
* `longitude` — longitude coordinate of the location 

* `timezone` — timezone of the location (in accordance with IANA database)
* `lat_updated_epoch` __*__ — Unix timestamp of the last data update
* `last_updated` — local time of the last data update

* `temperature_celsius` — temperature in degrees Celsius (°C)
* `temperature_fahrenheit` __*__ — temperature in degrees Fahrenheit (°F)

* `humidity` — humidity as a percentage

* `feels_like_celsius` — apparent temperature in degrees Celsius (°C)
* `feels_like_fahrenheit` __*__ — apparent temperature in degrees Fahrenheit (°F)

* `pressure_mb` — pressure in millibars
* `pressure_in` __*__ — pressure in inches of Mercury

* `wind_kph` — wind speed in kilometers per hour
* `wind_mph` __*__ — wind speed in miles per hour

* `wind_direction` — wind direction as a 16-point compass

* `gust_kph` — wind gust in kilometers per hour
* `gust_mph` __*__ — wind gust in miles per hour

* `air_quality_Carbon_Monoxide` — air toxic average concentration (μg/m^3) measurement: Carbon Monoxide (CO)
* `air_quality_Ozone` — air toxic average concentration (μg/m^3) measurement: Ozone (O3)
* `air_quality_Nitrogen_dioxide` — air toxic average concentration (μg/m^3) measurement: Nitrogen Dioxide (NO2)
* `air_quality_Sulphur_dioxide` — air toxic average concentration (μg/m^3) measurement: Sulphur Dioxide (SO2)
* `air_quality_PM2.5` — air toxic average concentration (μg/m^3) measurement: PM2.5 particles (<= 2.5 μm)
* `air_quality_PM10` — air toxic average concentration (μg/m^3) measurement: PM10 particles (<= 10 μm)

* `air_quality_us-epa-index` — air quality index calculated by methodology of [__US EPA__](https://www.epa.gov/)
* `air_quality_gb-defra-index` — air quality index calculated by methodology of [__UK DEFRA__](https://www.gov.uk/government/organisations/department-for-environment-food-rural-affairs)

* `condition_text` — weather condition description

_(__*__ — columns taken into the project's domain model as virtual (non-stored) properties)_


## Used technologies

### Application side

* Application programming language: [**Python**](https://www.python.org/)
* Application ORM-framework: [**SQLAlchemy**](https://pypi.org/project/SQLAlchemy/)

### Database side

* Database management systems: [**PostgreSQL**](https://www.postgresql.org/), [**MySQL**](https://www.mysql.com/)
* Database migration tool: [**Alembic**](https://pypi.org/project/alembic/)

### Other tools

* Containerization: [**Docker**](https://www.docker.com/)


## Project structure

The project, created for the current laboratory work and called **WWWeather** aka "_World Wide Weather_" 
or something like that, consists of two main parts:

* Database in charge of storing all weather data with [**Alembic** migration environment](alembic/README.md) 
  to provide version tracking and migrations application 

* Application built in accordance with the _Layered architecture_ approach 
  and consists of multiple **Python** packages:

  + [**WWWeather.Core**](pkgs/core/README.md) — application core package:  
    declares the application _Domain model_ and provides interfaces for data repository management 
    as well as data export and import from external feeds
 
  + [**WWWeather.Data-CSV**](pkgs/data-csv/README.md) — application CSV import/export adapter package:  
    provides **WWWeather.Core** weather records dumping/loading interfaces 
    implementations for the CSV format
  + [**WWWeather.Data-SQLAlchemy**](pkgs/data-sqlalchemy/README.md) — application storage implementation package:  
    implements WWWeather.Core weather records repository interface 
    for SQLAlchemy-driven database storage

  + [**WWWeather.CLI**](cli/README.md) — application simple commandline interface package:  
    provides such basic functionality as running weather records import/export
    and search functionality invocation


## Application deployment & step-to-step migration

The primary way of **WWWeather** application deployment is by using **Docker Compose** 
for which project includes numerous dockerfiles and [compose configuration](docker-compose.yaml).

However, in order to ease non-routine operations with the **WWWeather CLI** and **Alembic** we will also set up
a local virtual environment capable of running **Alembic** migrations and/or **WWWeather CLI** operations 
on the remote (in our case, deployed in **Docker** container) database.

The whole process of the deployment will also be plit by so-called steps — versions of the **WWWeather** project 
and current repository strictly correspond to the steps of the current laboratory work execution required by its task. 

### Prerequisites

To deploy **WWWeather** application with database server in **Docker** and **Alembic** migration environment, 
you will need to have the next software installed on your machine:

* **Python** `3.10` or higher
* **Docker Desktop** or **Docker Engine**/**Docker CLI** with the **Compose** plugin

### Preparations

#### Virtual environment

For local operations, we need to set up a **Python** virtual environment 
in the `.venv` directory in the root of our project — it can be done via the next command:

```shell
python -m venv .venv
```

Then activate it:

* on Linux/MacOS:

  ```shell
  source venv/bin/activate
  ```

* on Windows:

  ```shell
  .venv/Scripts/activate
  ```

#### Data files and work directories

To run scenarios, declared in further steps, we need to create a couple 
of special work folders in the root of our project:

* `.secrets` — secrets directory - will be used with **Docker Compose**
* `.data` — large data files directory — to load dataset files from
* `.out` — output directory — to save weather records export files into

Then we need to download the dataset CSV file into the `.data` directory,
the file itself should be named `GlobalWeatherRepository.csv`.

### Step 01

**Database schema:** `solid table`  
**Database server(s):** `PostgreSQL`  
**WWWeather.Core version:** `0.1.0`

In the current step we will initialize a **PostgreSQL** application database 
with the single table `weather_records` and import data from dataset CSV feed into it.

1. Start with installing **WWWeather** packages into the local virtual environment:
   
   ```shell
   pip install -e pkgs\core -e pkgs\data-csv\ -e pkgs\data-sqlalchemy\ -e cli\
   ```

2. Build **Docker** images of distribution files for these packages:

   ```shell
   docker build -f pkgs/core/dist.Dockerfile -t wwweather/dists/core:0.1.0 pkgs/core
   docker build -f pkgs/data-csv/dist.Dockerfile -t wwweather/dists/data-csv:0.1.0 pkgs/data-csv
   docker build -f pkgs/data-sqlalchemy/dist.Dockerfile -t wwweather/dists/data-sqlalchemy:0.1.0 pkgs/data-sqlalchemy
   docker build -f cli/dist.Dockerfile -t wwweather/dists/cli:0.1.0 cli
   ```

3. Create `db_postgres-password.txt` password file for the **PostgreSQL** application database 
   in the `.secrets` subdirectory of the project root directory, write a password to it as a single line and save.

4. Build a **Docker Compose** for the current configuration:

   ```shell
   docker-compose build --no-cache
   ```

5. Run **Docker Compose** `postgres-import_origin` profile to initialize the **PostgreSQL** database, 
   apply base migration to the `model-0.1.0` revision to it and perform weather records import 
   from the dataset `GlobalWeatherRepository.csv` file:

   ```shell
   docker compose --profile postgres-import_origin up -d --force-recreate
   ```

#### Available Docker Compose profiles

At the moment of the [**Step 01**](#step-01) the [compose configuration](docker-compose.yaml) contains next profiles:

* `postgres` — 
  run a **PostgreSQL** server for the application database

* `postgres-upgrade` — 
  run **Alembic** `upgrade` command to upgrade a **PostgreSQL** hema to the latest available version

* `postgres-import_origin` — 
  run **WWWeather.CLI** `import` command to import weather records 
  from the `.data/GlobalWeatherRepoitory.csv` file into the application database

* `postgres-export` — 
  run **WWWeather.CLI** `export` command to export weather records 
  from the application database into the `.out/wwweather_db-export.csv` file

* `postgres-import_origin` — 
  run **WWWeather.CLI** `import` command to import weather records 
  from the `.out/wwweather_db-export.csv` file into the application database

### Step 02

**Database schema:** `1-to-1 tables`
**Database server(s):** `PostgreSQL`  
**WWWeather.Core version:** `0.2.0`

In the current step we will migrate the application database located on the **PostgreSQL** server 
to the new schema version, separating new `air_quality_records` table from the original `weather_records` table
with _1-to-1_ relation between them.

1. Reinstall **WWWeather** application packages in the local virtual environment

   ```shell
   pip uninstall -y WWWeather.CLI WWWeather.Data-SQLAlchemy WWWeather.Data-CSV WWWeather.Core
   pip install -e pkgs\core -e pkgs\data-csv\ -e pkgs\data-sqlalchemy\ -e cli\
   ```

2. Build **Docker** images of distribution files for the new versions of these packages:

   ```shell
   docker build -f pkgs/core/dist.Dockerfile -t wwweather/dists/core:0.2.0 pkgs/core
   docker build -f pkgs/data-csv/dist.Dockerfile -t wwweather/dists/data-csv:0.2.0 pkgs/data-csv
   docker build -f pkgs/data-sqlalchemy/dist.Dockerfile -t wwweather/dists/data-sqlalchemy:0.2.0 pkgs/data-sqlalchemy
   docker build -f cli/dist.Dockerfile -t wwweather/dists/cli:0.2.0 cli
   ```
   
3. Re-build a **Docker Compose** for the current configuration:

   ```shell
   docker-compose build --no-cache
   ```

4. Run **Docker Compose** `postgres-upgrade` profile to apply migration up to the `model-0.2.0` revision:

   ```shell
   docker compose --profile postgres-upgrade up -d --force-recreate
   ```
