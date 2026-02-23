"""
NYC Taxi Data Pipeline using dlt
Fetches data from custom API and loads into DuckDB
"""
import dlt
import requests
from typing import Iterator, Dict, Any


def fetch_taxi_data() -> Iterator[Dict[str, Any]]:
    """
    Fetch paginated NYC taxi trip data from the custom API.
    
    API Details:
    - Base URL: https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
    - Format: Paginated JSON (1,000 records per page)
    - Pagination: Stop when an empty page is returned
    """
    base_url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        
        # Fetch data from API with page parameter
        response = requests.get(f"{base_url}?page={page}")
        response.raise_for_status()
        
        data = response.json()
        
        # Stop if we get an empty response
        if not data or len(data) == 0:
            print(f"No more data. Stopped at page {page}")
            break
        
        print(f"  Received {len(data)} records from page {page}")
        
        # Yield each record
        for record in data:
            yield record
        
        page += 1


def run_pipeline():
    """
    Run the dlt pipeline to load taxi data into DuckDB
    """
    # Create a pipeline
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data"
    )
    
    # Run the pipeline with the taxi data resource
    load_info = pipeline.run(
        fetch_taxi_data(),
        table_name="trips",
        write_disposition="replace"  # Replace data on each run
    )
    
    # Print load information
    print("\n" + "="*50)
    print("Pipeline Load Information:")
    print("="*50)
    print(load_info)
    print("\n" + "="*50)
    print("Pipeline run completed successfully!")
    print(f"Database location: {pipeline.dataset_name}")
    print("="*50)


if __name__ == "__main__":
    run_pipeline()
