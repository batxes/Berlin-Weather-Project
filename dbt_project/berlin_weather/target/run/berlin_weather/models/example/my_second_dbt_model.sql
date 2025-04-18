

  create or replace view `berlin-weather-project`.`berlin_weather_dataset`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `berlin-weather-project`.`berlin_weather_dataset`.`my_first_dbt_model`
where id = 1;

