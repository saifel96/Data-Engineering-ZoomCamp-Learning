# Module 3: Data Warehouse with BigQuery

## 📚 Overview
This module covers working with Google BigQuery as a data warehouse solution, including data ingestion from GCS, external tables, partitioning, clustering, and query optimization.

## 🎯 Learning Objectives
- Understanding BigQuery architecture and features
- Creating external tables from GCS data
- Implementing table partitioning and clustering strategies
- Analyzing query performance and costs
- Working with large-scale taxi trip data

## 🗂️ Project Structure

```
03-Data-Warehouse-BigQuery/
├── README.md                          # This file
├── ingest_yellow_2024_to_gcs.yaml    # Kestra workflow for data ingestion
└── big_query.sql                      # BigQuery SQL queries and homework solutions
```

## 🚀 What I Completed

### 1. Data Ingestion Pipeline
**File:** `ingest_yellow_2024_to_gcs.yaml`

Created a Kestra workflow that:
- Downloads NYC Yellow Taxi trip data for all 12 months of 2024
- Uses Docker containers for reproducible execution
- Uploads Parquet files to Google Cloud Storage
- Organizes data with proper folder structure (`yellow/2024/`)
- Implements ForEach loop for efficient batch processing

**Key Features:**
- Automated monthly data downloads from CloudFront CDN
- Direct upload to GCS bucket
- Securely managed GCP credentials using Kestra secrets
- Dynamic file naming with month variables

### 2. BigQuery Data Warehouse Implementation
**File:** `big_query.sql`

#### External Tables
Created external tables pointing to GCS Parquet files:
```sql
CREATE OR REPLACE EXTERNAL TABLE `external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://saif-zoomcamp-bucket/yellow/2024/yellow_tripdata_2024-*.parquet']
);
```

#### Table Types Explored
1. **External Tables** - Query data directly from GCS
2. **Non-Partitioned Tables** - Standard BigQuery tables
3. **Partitioned Tables** - Partitioned by pickup/dropoff date
4. **Partitioned + Clustered Tables** - Optimized with VendorID clustering

### 3. Homework Solutions

Completed comprehensive homework analyzing NYC taxi data:

- **Q1:** Total record count queries on external tables
- **Q2:** Distinct pickup location analysis comparing external vs materialized tables
- **Q3:** Data scanning and cost estimation exercises
- **Q4:** Fare amount analysis (records with zero fare)
- **Q5:** Created partitioned and clustered table for optimal performance
- **Q6:** Analyzed partition impact on query performance and data scanned

### 4. Performance Optimization

Compared query performance across different table types:

| Table Type | Use Case | Performance |
|------------|----------|-------------|
| External Table | Ad-hoc queries, cost-effective storage | Slower, scans all data |
| Non-Partitioned | Small datasets, full table scans | Fast for small data |
| Partitioned | Date-range queries | Significantly faster, less data scanned |
| Partitioned + Clustered | Filtered queries on cluster key | Best performance |

**Key Finding:** Partitioned + Clustered tables reduced data scanned from full dataset to only relevant partitions when querying specific date ranges.

## 🔑 Key Concepts Learned

### Partitioning
- Improves query performance for date-range filters
- Reduces costs by scanning less data
- Partitioned by `DATE(tpep_pickup_datetime)` and `DATE(tpep_dropoff_datetime)`

### Clustering
- Further optimizes queries with filters on clustered columns
- Used `VendorID` as clustering column
- Automatically sorts data within each partition

### External vs Materialized Tables
- **External:** Cost-effective for infrequent queries, data stays in GCS
- **Materialized:** Better performance, optimized for frequent queries

## 🛠️ Technologies Used
- **Google BigQuery** - Data warehouse and analytics
- **Google Cloud Storage (GCS)** - Data lake storage
- **Kestra** - Workflow orchestration
- **Docker** - Containerized task execution
- **Parquet** - Columnar storage format

## 📊 Dataset
- **Source:** NYC Taxi & Limousine Commission (TLC)
- **Type:** Yellow Taxi Trip Records
- **Period:** January - December 2024
- **Format:** Parquet files
- **Size:** 12 monthly files

## 💡 Best Practices Applied
1. ✅ Used external tables for cost-effective data exploration
2. ✅ Implemented partitioning for date-based queries
3. ✅ Added clustering for frequently filtered columns
4. ✅ Analyzed query costs before running expensive operations
5. ✅ Stored data in columnar Parquet format for efficiency
6. ✅ Organized GCS data with logical folder structure

## 🎓 Skills Gained
- BigQuery SQL query optimization
- Data warehouse design and architecture
- GCP integration and authentication
- Workflow orchestration with Kestra
- Performance tuning and cost optimization
- Working with large-scale datasets

## 🔗 Resources
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Kestra Documentation](https://kestra.io/docs)

---

**Status:** ✅ Completed  
**Date:** February 2026  
*Part of the Data Engineering Zoomcamp 2026*
