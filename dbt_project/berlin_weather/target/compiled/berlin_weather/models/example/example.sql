-- models/stg_soil_temperature.sql

with raw_data as (

  select
    STATIONS_ID,
    MESS_DATUM,
    QN_2,
    V_TE002,
    V_TE005,
    V_TE010,
    V_TE020,
    V_TE050,
    V_TE100,
    eor,

    -- Convert MESS_DATUM (e.g., 2023120905) to TIMESTAMP
    parse_timestamp('%Y%m%d%H', cast(MESS_DATUM as string)) as mess_datum_ts

  from `berlin-weather-project.berlin_weather_dataset.berlin_soil_temperature`

)

select *
from raw_data