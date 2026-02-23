"""@bruin
name: ingestion.trips
type: python
image: python:3.11

connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
@bruin"""

import os
import json
import pandas as pd
from datetime import datetime
import requests
from io import BytesIO
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    # Generate list of months between start and end dates
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    months = pd.date_range(start=start, end=end, freq='MS')
    
    # Fetch parquet files from CloudFront
    dataframes = []
    
    for taxi_type in taxi_types:
        for month in months:
            year = month.year
            month_num = str(month.month).zfill(2)
            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month_num}.parquet"
            
            try:
                # Download the parquet file using requests
                response = requests.get(url, verify=False, timeout=60)
                response.raise_for_status()
                
                # Read parquet from bytes
                df = pd.read_parquet(BytesIO(response.content))
                dataframes.append(df)
                print(f"Successfully fetched {url} with {len(df)} rows")
            except Exception as e:
                print(f"Warning: Could not fetch {url}: {e}")
    
    if not dataframes:
        print("Warning: No data was fetched, returning empty DataFrame")
        return pd.DataFrame()
    
    final_dataframe = pd.concat(dataframes, ignore_index=True)
    print(f"Total rows in final dataframe: {len(final_dataframe)}")
    
    return final_dataframe