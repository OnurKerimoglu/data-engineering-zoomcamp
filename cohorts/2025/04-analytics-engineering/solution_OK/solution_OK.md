**Q1**\
**A1**:
`select * from dtc_zoomcamp_2025.raw_nyc_tripdata.ext_green_taxi`

**Q2**\
**A2**:
Update the WHERE clause to pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY

**Q3**\
**A2**:
dbt run --select +models/core/

**Q4**\
**A5**:
First the new core model: `models/core/fct_taxi_trips_quarterly_revenue.sql`:
```
{{ config(materialized='table') }}

with trips_data as (
    select * from {{ ref('fact_trips') }}
)
    select 
    -- Revenue grouping
    service_type,
    {{ dbt.date_trunc("year", "pickup_datetime") }} as revenue_year, 
    {{ dbt.date_trunc("quarter", "pickup_datetime") }} as revenue_quarter, 
    -- Revenue calculation 
    sum(total_amount) as revenue_year_quarterly_total_amount
    from trips_data
    group by 1,2,3
```
Then,
```
WITH cleaned as (
SELECT
service_type,
extract (YEAR FROM revenue_year) as year,
extract (QUARTER FROM revenue_quarter) as quarter,
revenue_year_quarterly_total_amount as revenue
FROM `ny-taxi-453114.ny_taxi_dev.fct_taxi_trips_quarterly_revenue`
where 
extract (YEAR FROM revenue_year)=2020 
),
ranked as (
select *,
ROW_NUMBER() over (partition by service_type order by revenue desc) as RN
from cleaned
)
select *
from ranked
where RN in (1,4)
order by service_type, RN
```
Reveals:
Green: {best:2020-Q1 worst: 2020-Q2}\
Yellow: {best:2020-Q1 worst:2020-Q2}


