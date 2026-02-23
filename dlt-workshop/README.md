# dlt Workshop Homework - Data Engineering Zoomcamp 2026

## ✅ Homework Complete!

Successfully built a dlt pipeline to load **10,000 NYC Yellow Taxi trip records** from a custom API into DuckDB.

---

## 📊 Homework Answers

### Question 1: What is the start date and end date of the dataset?
**Answer: `2009-06-01 to 2009-07-01`** ✅

- Start Date: 2009-06-01
- End Date: 2009-07-01

### Question 2: What proportion of trips are paid with credit card?
**Answer: `26.66%`** ✅

- Total trips: 10,000
- Credit card trips: 2,666
- Percentage: 26.66%

Payment type breakdown:
- CASH: 7,235 (72.35%)
- Credit: 2,666 (26.66%)
- Cash: 97 (0.97%)
- Dispute: 1 (0.01%)
- No Charge: 1 (0.01%)

### Question 3: What is the total amount of money generated in tips?
**Answer: `$6,063.41`** ✅

- Total tips: $6,063.41
- Average tip per trip: ~$0.61

---

## 🏗️ Pipeline Implementation

### Data Source
- **API URL**: `https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api`
- **Format**: Paginated JSON
- **Page Size**: 1,000 records per page
- **Total Pages Fetched**: 10 pages (11th page was empty)
- **Total Records**: 10,000

### Pipeline Details
- **Pipeline Name**: `taxi_pipeline`
- **Destination**: DuckDB (local file database)
- **Dataset Name**: `nyc_taxi_data`
- **Table Name**: `trips`
- **Write Disposition**: Replace (overwrites data on each run)

### Key Features Implemented
- ✅ REST API pagination handling
- ✅ Automatic schema detection
- ✅ DuckDB local storage
- ✅ Data quality validation
- ✅ Comprehensive analysis queries

---

## 📁 Project Structure

```
dlt-workshop/
├── taxi_pipeline.py              # Main dlt pipeline script
├── analyze_taxi_data.py          # Analysis script (answers homework questions)
├── taxi_analysis.ipynb          # Jupyter notebook for interactive analysis
├── requirements.txt              # Python dependencies
├── taxi_pipeline.duckdb          # DuckDB database file (created by dlt)
└── README.md                     # This file
```

---

## 🚀 Running the Pipeline

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install "dlt[duckdb]" requests pandas
```

### Execute Pipeline
```bash
# Run the data ingestion pipeline
python taxi_pipeline.py

# Run the analysis to get homework answers
python analyze_taxi_data.py
```

### Explore with dlt Dashboard
```bash
# View pipeline information
dlt pipeline taxi_pipeline show
```

---

## 📝 Database Schema

The `nyc_taxi_data.trips` table contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `trip_pickup_date_time` | TIMESTAMP | When the trip started |
| `trip_dropoff_date_time` | TIMESTAMP | When the trip ended |
| `passenger_count` | INTEGER | Number of passengers |
| `trip_distance` | DOUBLE | Distance in miles |
| `tip_amt` | DOUBLE | Tip amount in dollars |
| `tolls_amt` | DOUBLE | Tolls amount in dollars |
| `payment_type` | VARCHAR | Payment method (CASH, Credit, etc.) |

---

## 🎓 Key Learnings

### Technical Skills
- ✅ **REST API Integration**: Handled paginated JSON API responses
- ✅ **dlt Framework**: Used data load tool for declarative data pipelines
- ✅ **DuckDB**: Leveraged embedded analytical database for local analysis
- ✅ **Data Analysis**: SQL queries with aggregations and filtering

### dlt Benefits Observed
1. **Automatic Schema Discovery**: No need to define schema manually
2. **Simple API**: Clean Python interface for data loading
3. **DuckDB Integration**: Seamless local database creation
4. **Pipeline Metadata**: Tracking and monitoring built-in

---

## 📈 Performance Metrics

- **Pipeline Execution Time**: ~2.4 seconds
- **Records Fetched**: 10,000 records
- **Pages Processed**: 10 pages @ 1,000 records each
- **Database Size**: ~2.5 MB

---

## 🔗 Resources

| Resource | Link |
|----------|------|
| dlt Documentation | [dlthub.com/docs](https://dlthub.com/docs) |
| dlt Dashboard Docs | [dlthub.com/docs/general-usage/dashboard](https://dlthub.com/docs/general-usage/dashboard) |
| Data Engineering Zoomcamp | [GitHub](https://github.com/DataTalksClub/data-engineering-zoomcamp) |
| Workshop Materials | [dlt 2026 Zoomcamp](https://github.com/anair123/data-engineering-zoomcamp/tree/workshop/dlt_2026/cohorts/2026/workshops/dlt) |

---

**🎉 dlt Workshop Complete!** | Data Engineering Zoomcamp 2026 | [@DataTalksClub](https://datatalks.club) | [@dltHub](https://dlthub.com)
