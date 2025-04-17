{{
  config(
    materialized='view'
  )
}}

SELECT
  V_TE002,
  V_TE005,
  V_TE010,
  V_TE020,
  V_TE050,
  V_TE100,
  -- Add your transformation logic here
  (V_TE002 + V_TE005) / 2 AS average_te002_te005
FROM
  `berlin-weather-project.berlin_weather_dataset.berlin_soil_temperature`
