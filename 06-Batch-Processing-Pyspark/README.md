# Module 6: Batch Processing with Apache Spark

## Overview

This module covers batch processing using **Apache Spark** and **PySpark**. It walks through setting up a local Spark environment, working with large datasets, running SQL queries, and connecting Spark to Google Cloud Storage (GCS) and Dataproc.

---

## Topics Covered

### 1. Getting Started with PySpark (`04_pyspark.ipynb`)
- Installing and configuring PySpark locally
- Creating a `SparkSession`
- Reading CSV files into Spark DataFrames
- Exploring schema and data types
- Partitioning data and writing Parquet files

### 2. Defining Schemas (`05_taxi_schema.ipynb`)
- Manually defining schemas using `pyspark.sql.types`
- Reading data with an enforced schema
- Handling type mismatches and null values

### 3. Spark SQL (`06_spark_sql.ipynb`)
- Registering DataFrames as temporary views
- Writing SQL queries with `spark.sql()`
- Combining green and yellow taxi datasets
- Computing revenue metrics and grouping results
- Converting the notebook to a standalone Python script

### 4. GroupBy & Joins (`07_groupby_join.ipynb`)
- GroupBy operations and aggregations in Spark
- Shuffle and non-shuffle joins
- Joining taxi trip data with zone lookup tables
- Understanding the Spark execution plan

### 5. Spark & Google Cloud Storage (`09_spark_gcs.ipynb`)
- Uploading data to GCS with `gsutil`
- Configuring the GCS Hadoop connector
- Reading and writing Parquet files from/to GCS

---

## Homework (`my-homework-pyspark.ipynb`)

Hands-on homework using the **NYC Yellow Taxi dataset (November 2025)**:

| Question | Task |
| :--- | :--- |
| **Q1** | Spark version check |
| **Q2** | Read parquet, repartition to 4 partitions, write to Parquet — check average file size |
| **Q3** | Count trips with pickup date = `2025-11-15` using Spark SQL |
| **Q4** | Find the longest trip duration in hours |
| **Q5** | Identify the most frequent pickup zone using a join with the taxi zone lookup table |

### Key operations used:
- `SparkSession.builder` with `local[*]`
- `df.repartition(4)` and `df.write.parquet()`
- `df.registerTempTable()` for SQL queries
- `F.to_date()`, `unix_timestamp()` for datetime operations
- `df.join()` for enriching trips with zone names
- Grouping and ordering results with `spark.sql()`

---

## Running Spark in the Cloud

See [cloud.md](./cloud.md) for detailed instructions on:
- **Local Standalone Cluster** — `start-master.sh` / `start-worker.sh`
- **`spark-submit`** — submitting scripts to a Spark cluster
- **GCS Connector** — reading/writing data from Google Cloud Storage
- **Google Cloud Dataproc** — managed Spark on GCP

---

## Setup

### Prerequisites
- Java 8 or 11
- Python 3.8+
- PySpark

### Install PySpark

```bash
pip install pyspark
```

### Download Data

```bash
# Yellow Taxi November 2025
curl -o yellow_tripdata_2025-11.parquet \
  https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet

# Taxi Zone Lookup
curl -o taxi_zone_lookup.csv \
  https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

---

## Tech Stack

| Tool | Purpose |
| :--- | :--- |
| Apache Spark 3.x | Distributed batch processing engine |
| PySpark | Python API for Spark |
| Spark SQL | SQL interface for DataFrames |
| Google Cloud Storage | Cloud data lake storage |
| Google Cloud Dataproc | Managed Spark cluster on GCP |
| Parquet | Columnar storage format |
