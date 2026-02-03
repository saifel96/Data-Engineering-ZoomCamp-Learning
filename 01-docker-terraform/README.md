# Module 1: Docker & Terraform

## Overview

This module covers containerization with Docker and infrastructure as code with Terraform - essential tools for modern data engineering. The module includes practical implementations of data pipelines using Docker containers and PostgreSQL.

## Contents

### 📦 [Pipeline Project](./pipeline/)

A complete containerized data pipeline for ingesting NYC Yellow Taxi trip data into PostgreSQL.

**Features:**
- Automated data ingestion from NYC TLC dataset
- Docker Compose orchestration (PostgreSQL + pgAdmin)
- Python-based ETL with pandas and SQLAlchemy
- Configurable via command-line arguments
- Chunk-based processing for large datasets

**Tech Stack:** Python 3.13, PostgreSQL 18, Docker, pandas, SQLAlchemy, uv

[View detailed documentation →](./pipeline/README.md)

## Learning Objectives

### Docker
- ✅ Container fundamentals and Docker commands
- ✅ Creating Dockerfiles for Python applications
- ✅ Docker Compose for multi-container applications
- ✅ Docker networking and volume management
- ✅ Building and running containerized data pipelines

### Terraform
- ⬜ Infrastructure as Code (IaC) basics
- ⬜ Terraform configuration and providers
- ⬜ Managing cloud resources
- ⬜ State management
- ⬜ Terraform workflows

## Key Concepts

### Containerization Benefits
- **Reproducibility**: Same environment across development, testing, and production
- **Isolation**: Dependencies don't conflict with host system
- **Portability**: Run anywhere Docker is installed
- **Scalability**: Easy to replicate and orchestrate containers

### Data Pipeline Components
1. **Data Source**: NYC TLC trip data (CSV format, compressed)
2. **Processing**: pandas for data transformation and chunking
3. **Storage**: PostgreSQL for structured data storage
4. **Management**: pgAdmin for database administration

## Quick Start

```bash
# Navigate to the pipeline directory
cd pipeline/

# Start PostgreSQL and pgAdmin
docker-compose up -d

# Build the ingestion image
docker build -t taxi_ingest:v001 .

# Run data ingestion
docker run -it --network=pipeline_default taxi_ingest:v001 \
  --pg-user=root --pg-pass=root --pg-host=pgdatabase \
  --pg-port=5432 --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 --month=1 --chunksize=100000
```

## Project Structure

```
01-docker-terraform/
├── README.md                    # This file
└── pipeline/                    # NYC Taxi data pipeline
    ├── docker-compose.yaml      # PostgreSQL + pgAdmin setup
    ├── Dockerfile              # Data ingestion container
    ├── ingest_data.py          # ETL script with CLI arguments
    ├── pyproject.toml          # Python dependencies
    ├── uv.lock                 # Locked dependency versions
    └── README.md               # Pipeline documentation
```

## Technologies Used

| Technology | Purpose | Version |
|------------|---------|---------|
| Docker | Containerization platform | Latest |
| Docker Compose | Multi-container orchestration | v2 |
| PostgreSQL | Relational database | 18 |
| pgAdmin | Database management UI | 4 |
| Python | Programming language | 3.13 |
| pandas | Data manipulation | Latest |
| SQLAlchemy | Database toolkit | Latest |
| psycopg2 | PostgreSQL adapter | Latest |
| uv | Fast package installer | Latest |

## Resources

### Documentation
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Terraform Documentation](https://www.terraform.io/docs)

### Data Source
- [NYC TLC Trip Record Data](https://github.com/DataTalksClub/nyc-tlc-data)
- [NYC Taxi & Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

### Course Material
- [DataTalks.Club Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## Common Commands

### Docker
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container logs
docker logs <container_id>

# Execute command in container
docker exec -it <container_id> bash

# Remove container
docker rm <container_id>

# Remove image
docker rmi <image_name>

# List networks
docker network ls

# Inspect network
docker network inspect <network_name>
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build -d
```

### PostgreSQL (via Docker)
```bash
# Connect to PostgreSQL
docker exec -it pipeline-pgdatabase-1 psql -U root -d ny_taxi

# Useful SQL queries
SELECT COUNT(*) FROM yellow_taxi_trips_2021_1;
SELECT * FROM yellow_taxi_trips_2021_1 LIMIT 10;
\dt  # List tables
\d yellow_taxi_trips_2021_1  # Describe table
```

## Progress Tracker

- [x] Set up Docker environment
- [x] Create Dockerfile for Python application
- [x] Set up PostgreSQL with Docker Compose
- [x] Add pgAdmin for database management
- [x] Implement data ingestion script
- [x] Add command-line argument parsing
- [x] Test data pipeline with real data
- [x] Document the project
- [ ] Add Terraform configurations
- [ ] Deploy to cloud infrastructure

## Troubleshooting

### Issue: Container can't connect to database
**Solution:** Check the network and use the correct one (usually `pipeline_default`)

### Issue: Port conflicts
**Solution:** Modify ports in `docker-compose.yaml` or stop conflicting services

### Issue: Permission denied errors
**Solution:** Ensure Docker Desktop is running and you have proper permissions

### Issue: Out of memory
**Solution:** Reduce `--chunksize` parameter or allocate more memory to Docker

## Next Steps

1. ✅ Complete Docker module
2. 📝 Start Terraform module
3. 🚀 Deploy pipeline to cloud (GCP/AWS)
4. 🔄 Implement automated scheduling
5. 📊 Add data quality checks

## Notes

This module is part of the DataTalks.Club Data Engineering Zoomcamp (2024-2025 cohort). The focus is on building practical, production-ready data engineering solutions using modern tools and best practices.
