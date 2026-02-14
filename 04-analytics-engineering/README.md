# Module 4: Analytics Engineering with dbt

## 🎯 Module Objective

Building a robust data pipeline with **dbt (data build tool)** to transform raw NYC Taxi trip data (Green, Yellow, and FHV) from Google BigQuery into clean, analyzable data models following analytics engineering best practices.

---

## 📁 Project Structure

```
04-analytics-engineering/
├── dbt_project.yml              # dbt project configuration
├── packages.yml                 # dbt package dependencies
├── ingest_taxidata_2019_2020.yaml  # Kestra workflow for data ingestion
├── models/
│   ├── staging/                 # Raw data transformations
│   │   ├── source.yml          # Source definitions
│   │   ├── stg_yellow_tripdata.sql
│   │   ├── stg_green_tripdata.sql
│   │   └── stg_fhv_tripdata.sql
│   ├── intermediate/            # Business logic transformations
│   │   ├── int_trips_unioned.sql
│   │   └── int_trips.sql
│   └── marts/                   # Final analytical models
│       ├── dim_vendors.sql
│       ├── dim_zones.sql
│       ├── fct_trips.sql
│       ├── fct_trips.yml
│       └── reporting/
│           └── fct_monthly_zone_revenue.sql
├── macros/                      # Reusable SQL functions
│   ├── get_trip_duration_minutes.sql
│   ├── get_vendor_data.sql
│   └── safe_cast.sql
├── seeds/                       # CSV reference data
│   ├── payment_type_lookup.csv
│   └── taxi_zone_lookup.csv
└── tests/                       # Data quality tests
```

## 🛠 Technical Highlights & Key Concepts

### dbt Architecture (Medallion Structure)

* **Staging Layer:** Created models (`stg_green_tripdata`, `stg_yellow_tripdata`, `stg_fhv_tripdata`) with column name standardization, data type conversions (casting), and filtering of invalid records (e.g., `dispatching_base_num is not null`).
* **Intermediate Layer:** Business logic transformations and data enrichments
* **Core/Marts Layer:** Unification of different taxi types into a central fact table (`fct_trips`) and dimension tables (`dim_vendors`, `dim_zones`).
* **Reporting Layer:** Built aggregation tables for business questions, such as `fct_monthly_zone_revenue` to analyze revenue by zone and month.

### Data Quality & Testing

* Implemented **dbt tests** (`accepted_values`, `not_null`, `unique`) to ensure data integrity (e.g., `payment_type`).
* Experience with **test severity**: Understanding when a build should fail hard on errors (`error`) vs. when it should only issue a warning (`warn`).

### Macros & Packages

* Utilized **dbt macros** (e.g., `get_payment_type_description`, `get_trip_duration_minutes`) to make SQL logic (case statements) reusable.
* Leveraged community packages like **dbt_utils** for efficient surrogate key generation.

### Seeds & Reference Data

* Loaded CSV reference data (`payment_type_lookup.csv`, `taxi_zone_lookup.csv`) for dimension tables

## 🚨 Technical Challenges & Problem-Solving

### ⚠️ Challenge 1: Schema Drift - The Parquet Fix

**Problem:** Parquet files in Google Cloud Storage had inconsistent data types (e.g., `ehail_fee` sometimes as `INT64`, sometimes as `DOUBLE`), causing BigQuery External Table failures.

**Root Cause:** `green_tripdata` was configured as an EXTERNAL table

#### Step 1: Confirm the problem

```sql
SELECT table_name, table_type
FROM `kestra-sandbox-486523.zoomcamp`.INFORMATION_SCHEMA.TABLES
WHERE table_name = 'green_tripdata';
```

Result: The table type was `EXTERNAL`, which doesn't allow schema modifications.

---

#### Step 2: Free the name + keep external reference (optional)

```sql
-- Rename external table for reference
CREATE OR REPLACE EXTERNAL TABLE `kestra-sandbox-486523.zoomcamp.green_tripdata_external`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://saif-zoomcamp-bucket/green/2019/*.parquet',
    'gs://saif-zoomcamp-bucket/green/2020/*.parquet'
  ]
);

-- Drop the original external table
DROP TABLE `kestra-sandbox-486523.zoomcamp.green_tripdata`;
```

---

#### Step 3: Create the native table with fixed schema

```sql
CREATE TABLE `kestra-sandbox-486523.zoomcamp.green_tripdata` (
  VendorID INT64,
  lpep_pickup_datetime TIMESTAMP,
  lpep_dropoff_datetime TIMESTAMP,
  store_and_fwd_flag STRING,
  RatecodeID FLOAT64,
  PULocationID INT64,
  DOLocationID INT64,
  passenger_count FLOAT64,
  trip_distance FLOAT64,
  fare_amount FLOAT64,
  extra FLOAT64,
  mta_tax FLOAT64,
  tip_amount FLOAT64,
  tolls_amount FLOAT64,
  ehail_fee FLOAT64,
  improvement_surcharge FLOAT64,
  total_amount FLOAT64,
  payment_type INT64
);
```

---

### ⚠️ Challenge 2: Schema Drift Across Parquet Files

**Problem:** Different Parquet files had inconsistent schemas:
- `ehail_fee` type mismatch (INT vs FLOAT)
- `payment_type` was FLOAT in some files, INT64 in others

#### **Solution:** File-by-file load with explicit type casting

I migrated from External Tables to **Native Tables**. Using a **Bash script** in Cloud Shell, I loaded files individually and normalized them through explicit `CAST` operations in BigQuery.

This approach bypasses Parquet schema autodetection and enforces consistent types.

**Run in Cloud Shell:**

```bash
PROJECT="kestra-sandbox-486523"
DS="zoomcamp"
RAW="$PROJECT:$DS.green_raw_tmp"

# Optional: start clean
bq query --project_id="$PROJECT" --use_legacy_sql=false \
"TRUNCATE TABLE \`$PROJECT.$DS.green_tripdata\`;"

# Loop over all parquet files (2019 + 2020)
for f in $(gsutil ls gs://saif-zoomcamp-bucket/green/2019/*.parquet gs://saif-zoomcamp-bucket/green/2020/*.parquet); do
  echo "Processing $f"

  # 1) Load ONE file into a raw temp table (overwrite each time)
  bq load --project_id="$PROJECT" \
    --replace \
    --autodetect \
    --source_format=PARQUET \
    "$RAW" \
    "$f" || { echo "FAILED LOAD: $f"; exit 1; }

  # 2) Insert into final native table with explicit type casting
  bq query --project_id="$PROJECT" --use_legacy_sql=false \
    "INSERT INTO \`$PROJECT.$DS.green_tripdata\`
     SELECT
       VendorID,
       lpep_pickup_datetime,
       lpep_dropoff_datetime,
       store_and_fwd_flag,
       CAST(RatecodeID AS FLOAT64),
       PULocationID,
       DOLocationID,
       CAST(passenger_count AS FLOAT64),
       CAST(trip_distance AS FLOAT64),
       CAST(fare_amount AS FLOAT64),
       CAST(extra AS FLOAT64),
       CAST(mta_tax AS FLOAT64),
       CAST(tip_amount AS FLOAT64),
       CAST(tolls_amount AS FLOAT64),
       CAST(ehail_fee AS FLOAT64) AS ehail_fee,
       CAST(improvement_surcharge AS FLOAT64),
       CAST(total_amount AS FLOAT64),
       SAFE_CAST(payment_type AS INT64) AS payment_type
     FROM \`$PROJECT.$DS.green_raw_tmp\`;" || { echo "FAILED INSERT: $f"; exit 1; }
done
```

**Why this works:**
- Loads one file at a time into a temporary table
- Uses explicit `CAST` operations to normalize types
- `SAFE_CAST` for `payment_type` handles any conversion errors gracefully
- Inserts clean data into the native table

---

#### Step 4: Validate the load

```bash
bq query --project_id=kestra-sandbox-486523 --use_legacy_sql=false \
"SELECT COUNT(*) AS total_rows FROM \`kestra-sandbox-486523.zoomcamp.green_tripdata\`;"
```

**Result:** `8,035,161` rows ✅

**Outcome:** A stable data foundation with over **8 million rows** for Green Taxis.

---

### ⚠️ Challenge 3: `trip_type` column missing in green_tripdata

dbt model referenced a `trip_type` column that didn't exist in the source data.

#### Solution: Remove or set to NULL in staging model

In `models/staging/stg_green_tripdata.sql`, either:

**Option 1: Remove the column**
```sql
-- Just don't select trip_type
```

**Option 2: Add as NULL** (if downstream models expect it)
```sql
CAST(NULL AS INT64) AS trip_type,
```

---

## 📈 Key Results & Validation

### Data Volume
* ✅ Successfully imported and transformed **8,035,161** Green Taxi records
* ✅ Processed over **43 million** FHV records for 2019
* ✅ Complete Yellow Taxi data for 2019-2020

### Business Insights
* 📊 Identified top revenue month for Green Taxis: **October 2019** (**421,509 trips**)
* 📍 Discovered top revenue zones (e.g., **East Harlem South**) for 2020
* 💰 Monthly revenue analysis by zone and taxi type

### Data Quality
* ✅ All dbt tests passing successfully
* ✅ No schema conflicts
* ✅ Consistent data types across all sources

---

## ✅ Final Results

- Native BigQuery tables created with consistent schemas
- All 8+ million green taxi records loaded successfully
- dbt models run without schema conflicts
- Staging, intermediate, and mart layers working correctly

## 🔧 Key Commands Used

```bash
# Run dbt models
dbt run

# Run specific model
dbt run --select stg_green_tripdata

# Test data quality
dbt test

# Generate documentation
dbt docs generate
dbt docs serve

# Check BigQuery table info
bq show kestra-sandbox-486523:zoomcamp.green_tripdata
```

## 📚 Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Analytics Engineering Guide](https://www.getdbt.com/analytics-engineering/)

---

## 🚀 Key Takeaways

Analytics engineering is more than just writing SQL—it's about building **robust, production-grade data pipelines** that don't break when source data is messy or inconsistent. This module taught me that:

- **Schema drift is real:** Data sources evolve, and pipelines must be resilient to type changes
- **Native tables > External tables:** For transformation workloads, native tables offer better control and performance
- **Testing is critical:** dbt tests catch data quality issues before they reach dashboards
- **Documentation matters:** Self-documenting pipelines make collaboration and maintenance easier
- **Incremental improvements work:** Breaking down complex problems (like the Parquet schema issue) into manageable steps leads to success

The combination of **BigQuery for compute power** and **dbt for structure and testing** creates a powerful modern data stack.

---

**Status:** ✅ Module 4 Complete
