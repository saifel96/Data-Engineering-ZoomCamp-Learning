# NYC Taxi Data Pipeline

A containerized data pipeline for ingesting NYC Yellow Taxi trip data into PostgreSQL using Docker, Python, and pandas.

## Overview

This project provides a Docker-based solution to download, process, and load NYC taxi trip data from the official data source into a PostgreSQL database. It includes pgAdmin for database management and visualization.

## Features

- **Automated Data Ingestion**: Downloads and processes NYC Yellow Taxi trip data in chunks
- **Dockerized Environment**: Fully containerized setup with PostgreSQL and pgAdmin
- **Flexible Configuration**: Command-line arguments for customizing data ingestion parameters
- **Efficient Processing**: Chunked CSV reading for handling large datasets
- **Data Type Management**: Predefined schema for proper data type handling

## Tech Stack

- **Python 3.13** - Core programming language
- **PostgreSQL 18** - Database for storing taxi trip data
- **pgAdmin 4** - Web-based database management interface
- **Docker & Docker Compose** - Container orchestration
- **pandas** - Data manipulation and analysis
- **SQLAlchemy** - Database toolkit and ORM
- **psycopg2** - PostgreSQL adapter for Python
- **uv** - Fast Python package installer

## Project Structure

```
pipeline/
├── docker-compose.yaml    # Container orchestration configuration
├── Dockerfile            # Docker image definition for ingestion script
├── ingest_data.py        # Main data ingestion script
├── pyproject.toml        # Python project dependencies
└── README.md            # This file
```

## Prerequisites

- Docker Desktop installed and running
- At least 2GB of free disk space
- Internet connection for downloading data

## Quick Start

### 1. Start PostgreSQL and pgAdmin

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port `5432`
- pgAdmin on port `8085` (http://localhost:8085)

**pgAdmin Login:**
- Email: `admin@admin.com`
- Password: `root`

### 2. Build the Ingestion Docker Image

```bash
docker build -t taxi_ingest:v001 .
```

### 3. Run Data Ingestion

```bash
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_2021_1 \
    --year=2021 \
    --month=1 \
    --chunksize=100000
```

## Configuration

### Command-Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--pg-user` | Yes | PostgreSQL username | `root` |
| `--pg-pass` | Yes | PostgreSQL password | `root` |
| `--pg-host` | Yes | PostgreSQL host (container name) | `pgdatabase` |
| `--pg-port` | Yes | PostgreSQL port | `5432` |
| `--pg-db` | Yes | Database name | `ny_taxi` |
| `--target-table` | Yes | Target table name | `yellow_taxi_trips_2021_1` |
| `--year` | Yes | Year of data to download | `2021` |
| `--month` | Yes | Month of data to download | `1` |
| `--chunksize` | No | Number of rows per chunk | `100000` |

### Environment Variables (docker-compose.yaml)

PostgreSQL:
- `POSTGRES_USER=root`
- `POSTGRES_PASSWORD=root`
- `POSTGRES_DB=ny_taxi`

pgAdmin:
- `PGADMIN_DEFAULT_EMAIL=admin@admin.com`
- `PGADMIN_DEFAULT_PASSWORD=root`

## Data Schema

The ingestion script handles NYC Yellow Taxi trip data with the following schema:

```python
{
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "tpep_pickup_datetime": "datetime",
    "tpep_dropoff_datetime": "datetime"
}
```

## Usage Examples

### Ingest Different Months

```bash
# January 2021
docker run -it --network=pipeline_default taxi_ingest:v001 \
  --pg-user=root --pg-pass=root --pg-host=pgdatabase --pg-port=5432 \
  --pg-db=ny_taxi --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 --month=1 --chunksize=100000

# February 2021
docker run -it --network=pipeline_default taxi_ingest:v001 \
  --pg-user=root --pg-pass=root --pg-host=pgdatabase --pg-port=5432 \
  --pg-db=ny_taxi --target-table=yellow_taxi_trips_2021_2 \
  --year=2021 --month=2 --chunksize=100000
```

### Custom Chunk Size for Memory Optimization

```bash
# Smaller chunks for limited memory environments
docker run -it --network=pipeline_default taxi_ingest:v001 \
  --pg-user=root --pg-pass=root --pg-host=pgdatabase --pg-port=5432 \
  --pg-db=ny_taxi --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 --month=1 --chunksize=50000
```

## Accessing the Database

### Via pgAdmin

1. Open browser: http://localhost:8085
2. Login with credentials above
3. Add server:
   - Name: `Local PostgreSQL`
   - Host: `pgdatabase`
   - Port: `5432`
   - Username: `root`
   - Password: `root`
   - Database: `ny_taxi`

### Via psql CLI

```bash
docker exec -it pipeline-pgdatabase-1 psql -U root -d ny_taxi
```

Example queries:
```sql
-- Count total trips
SELECT COUNT(*) FROM yellow_taxi_trips_2021_1;

-- Average trip distance
SELECT AVG(trip_distance) FROM yellow_taxi_trips_2021_1;

-- Top 10 pickup locations
SELECT "PULocationID", COUNT(*) as trip_count 
FROM yellow_taxi_trips_2021_1 
GROUP BY "PULocationID" 
ORDER BY trip_count DESC 
LIMIT 10;
```

## Troubleshooting

### Container Can't Connect to Database

**Error:** `could not translate host name "pgdatabase" to address`

**Solution:** Ensure you're using the correct network:
```bash
# Check which network PostgreSQL is on
docker inspect pipeline-pgdatabase-1 --format='{{range $key, $value := .NetworkSettings.Networks}}{{$key}}{{end}}'

# Use that network (typically pipeline_default)
docker run -it --network=pipeline_default taxi_ingest:v001 ...
```

### Port Already in Use

**Error:** `port 5432 already allocated`

**Solution:** Stop any local PostgreSQL service or change the port in docker-compose.yaml:
```yaml
ports:
  - "5433:5432"  # Use host port 5433 instead
```

### Out of Memory During Ingestion

**Solution:** Reduce the chunk size:
```bash
--chunksize=50000  # or even 25000
```

## Data Source

Data is sourced from the official NYC Taxi & Limousine Commission dataset:
- Repository: https://github.com/DataTalksClub/nyc-tlc-data
- Format: `.csv.gz` (compressed CSV)
- Update frequency: Monthly

## Stopping the Pipeline

```bash
# Stop containers but keep data
docker-compose stop

# Stop and remove containers (data persists in volumes)
docker-compose down

# Remove everything including data volumes
docker-compose down -v
```

## Performance

- **Average ingestion time**: ~4-5 minutes per month (~1.3M rows)
- **Chunk processing**: ~20-25 seconds per 100K rows
- **Storage**: ~150-200MB per month uncompressed

## Future Enhancements

- [ ] Add data validation and quality checks
- [ ] Implement incremental loading (avoid duplicates)
- [ ] Add support for green taxi and FHV data
- [ ] Create automated ETL scheduler
- [ ] Add data transformation pipeline
- [ ] Implement logging and monitoring
- [ ] Add unit tests

## License

This project is part of the DataTalks.Club Data Engineering Zoomcamp learning materials.

## Acknowledgments

- [DataTalks.Club](https://datatalks.club/) for the Data Engineering Zoomcamp
- NYC Taxi & Limousine Commission for providing the open dataset
