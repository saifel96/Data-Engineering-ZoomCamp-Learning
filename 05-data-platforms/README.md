# Module 5: Data Platforms with Bruin

This module demonstrates building an end-to-end ELT pipeline using Bruin, processing NYC taxi trip data.

## 🚀 Project Overview

Built a complete data pipeline that:
- Ingests NYC Yellow Taxi trip data from NYC TLC dataset
- Processes and transforms data through staging layers
- Generates analytical reports
- Implements data quality checks

### Pipeline Architecture

```
ingestion.trips ──────────┐
                          ├──→ staging.trips ──→ reports.trips_report
ingestion.payment_lookup ─┘
```

## 📊 Pipeline Assets

### Ingestion Layer
- **`ingestion.trips`** (Python): Fetches NYC taxi trip parquet files from CloudFront CDN
- **`ingestion.payment_lookup`** (CSV Seed): Payment type reference data

### Staging Layer
- **`staging.trips`**: Cleaned and deduplicated trip data with payment type labels

### Reports Layer
- **`reports.trips_report`**: Aggregated trip statistics by date, taxi type, and payment method

## 🛠️ Technical Implementation

### Technologies Used
- **Bruin CLI**: Modern ELT orchestration framework
- **DuckDB**: Embedded analytical database
- **Python**: Data fetching and processing
- **Pandas & PyArrow**: Data manipulation

### Key Features Implemented
✅ Environment-based configuration with `.bruin.yml`  
✅ Dynamic date range processing using pipeline variables  
✅ SSL-enabled HTTPS data fetching  
✅ Materialization strategies (create+replace)  
✅ Data quality checks (not_null, non_negative)  
✅ Deduplication using SQL window functions  

## 📁 Project Structure

```
05-data-platforms/
└── my-taxi-pipeline/
    ├── .bruin.yml                    # Connection configuration
    ├── pipeline/
    │   ├── pipeline.yml              # Pipeline definition
    │   └── assets/
    │       ├── ingestion/
    │       │   ├── trips.py          # Fetch trip data
    │       │   ├── payment_lookup.asset.yml
    │       │   ├── payment_lookup.csv
    │       │   └── requirements.txt  # Python dependencies
    │       ├── staging/
    │       │   └── trips.sql         # Clean & transform
    │       └── reports/
    │           └── trips_report.sql  # Summary report
    └── nyc_taxi.db                   # DuckDB database
```

## 🚦 Running the Pipeline

### Prerequisites
```bash
# Install Bruin CLI
curl -LsSf https://getbruin.com/install/cli | sh
```

### Execution
```bash
# Navigate to project directory
cd my-taxi-pipeline

# Validate pipeline
bruin validate ./pipeline/pipeline.yml

# Run pipeline for a specific date range
bruin run ./pipeline/pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01

# Run with full refresh
bruin run ./pipeline/pipeline.yml --full-refresh

# Run specific asset and downstream dependencies
bruin run --select ingestion.trips+

# Check asset lineage
bruin lineage ./pipeline/assets/staging/trips.sql
```

## 📈 Pipeline Results

**Successful execution metrics:**
- ✅ **5.4M+ rows** processed (January 2022 Yellow Taxi data)
- ✅ **4 assets** executed successfully
- ✅ **5 quality checks** passed
- ⚡ **~27 seconds** total runtime

## 🔍 Data Quality Checks

Implemented checks:
- `not_null` on pickup_datetime (staging.trips)
- `not_null` on payment type fields (ingestion.payment_lookup)
- `unique` on payment_type_id (ingestion.payment_lookup)
- `non_negative` on trip_count (reports.trips_report)

## 🎓 Module 5 Homework

Completed homework questions covering:
1. ✅ Bruin project structure requirements
2. ✅ Materialization strategies (time_interval)
3. ✅ Pipeline variable overrides
4. ✅ Running assets with dependencies
5. ✅ Quality check configurations
6. ✅ Lineage visualization
7. ✅ Full refresh executions

## 🐛 Challenges & Solutions

### Challenge 1: SSL Certificate Verification
**Problem**: HTTPS downloads failing with SSL certificate errors  
**Solution**: Implemented requests library with `verify=False` and SSL warning suppression

### Challenge 2: Column Name Mapping
**Problem**: Yellow taxi data uses `tpep_pickup_datetime` instead of `pickup_datetime`  
**Solution**: Used SQL aliases to standardize column names in staging layer

### Challenge 3: First-Run Table Creation
**Problem**: `time_interval` strategy attempted DELETE before table existed  
**Solution**: Changed to `create+replace` strategy for initial runs

### Challenge 4: Missing Dependencies
**Problem**: Python environment lacked pandas and pyarrow  
**Solution**: Added versioned dependencies to `requirements.txt`

## 📚 Key Learnings

- **Declarative ELT**: Define what you want, not how to get it
- **Incremental Processing**: Efficient data pipeline design with time-based strategies
- **Quality-First Approach**: Built-in data validation at every layer
- **Dependency Management**: Automatic topological execution ordering
- **Environment Flexibility**: Easy transition from local DuckDB to cloud warehouses

## 🔗 Resources

- [Bruin Documentation](https://getbruin.com/docs)
- [NYC Taxi & Limousine Commission Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

---

**Module 5 Complete** ✅ | Data Engineering Zoomcamp 2026 | [@DataTalksClub](https://datatalks.club)
