
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `kestra-sandbox-486523.zoomcamp.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://saif-zoomcamp-bucket/yellow/2024/yellow_tripdata_2024-*.parquet']
);

-- HomeWork Q1 : 

SELECT count(*) FROM `kestra-sandbox-486523.zoomcamp.external_yellow_tripdata`;

-- Check yellow trip data
SELECT * FROM `zoomcamp.external_yellow_tripdata`;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE zoomcamp.yellow_tripdata_non_partitioned AS
SELECT * FROM zoomcamp.external_yellow_tripdata;



-- Homework Q2: 

SELECT count(DISTINCT(PULocationID)) FROM `kestra-sandbox-486523.zoomcamp.external_yellow_tripdata`;

SELECT count(DISTINCT(PULocationID)) FROM `kestra-sandbox-486523.zoomcamp.yellow_tripdata_non_partitioned`;



-- Homework Q3 : 

SELECT PULocationID FROM `kestra-sandbox-486523.zoomcamp.yellow_tripdata_non_partitioned`;

SELECT PULocationID, DOLocationID FROM `kestra-sandbox-486523.zoomcamp.yellow_tripdata_non_partitioned`;


-- Homework Q4

SELECT COUNT(*)
FROM `kestra-sandbox-486523.zoomcamp.yellow_tripdata_non_partitioned`
WHERE fare_amount = 0;

-- Homework Q5:

CREATE OR REPLACE TABLE zoomcamp.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM zoomcamp.external_yellow_tripdata;


-- Homework Q6:
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE zoomcamp.yellow_tripdata_partitioned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM zoomcamp.external_yellow_tripdata;


-- Impact of partition
-- Non Partitioned Table
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE zoomcamp.yellow_tripdata_non_partitioned AS
SELECT * FROM zoomcamp.external_yellow_tripdata;

SELECT DISTINCT(VendorID)
FROM `kestra-sandbox-486523.zoomcamp.yellow_tripdata_non_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned Table 
SELECT DISTINCT(VendorID)
FROM `kestra-sandbox-486523.zoomcamp.yellow_tripdata_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';


-- Bonus Q: -> 0 B

SELECT COUNT(*) FROM `kestra-sandbox-486523.zoomcamp.yellow_tripdata_non_partitioned`
