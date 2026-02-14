with fhv_source as (

    select * from {{source ('staging','fhv_tripdata')}}
),

fhv_renamed as (

    select 

    cast(dispatching_base_num as string) as dispatching_base_num,
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropOff_datetime, 
    cast(PUlocationID as integer) as pickup_location_id,
    cast(DOlocationID as integer) as dropoff_location_id,
    cast(SR_Flag as string) as shared_trips_flag, -- if 1 shared rides from high volume FHV company, 0 non-shared rides
    cast(Affiliated_base_number as string) as affiliated_base_number


    from fhv_source

    where dispatching_base_num is not null 
)

select * from fhv_renamed


