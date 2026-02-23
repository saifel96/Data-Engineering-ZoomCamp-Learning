/* @bruin
name: staging.trips
type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: create+replace

columns:
  - name: pickup_datetime
    type: timestamp
    primary_key: true
    checks:
      - name: not_null

@bruin */

SELECT
    t.tpep_pickup_datetime AS pickup_datetime,
    t.tpep_dropoff_datetime AS dropoff_datetime,
    CAST(NULL AS INTEGER) AS pickup_location_id,
    CAST(NULL AS INTEGER) AS dropoff_location_id,
    t.fare_amount,
    'yellow' AS taxi_type,
    p.payment_type_name
FROM ingestion.trips t
LEFT JOIN ingestion.payment_lookup p
    ON t.payment_type = p.payment_type_id
WHERE t.tpep_pickup_datetime >= '{{ start_datetime }}'
  AND t.tpep_pickup_datetime < '{{ end_datetime }}'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY t.tpep_pickup_datetime, t.tpep_dropoff_datetime, t.fare_amount
    ORDER BY t.tpep_pickup_datetime
) = 1