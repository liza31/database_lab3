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
