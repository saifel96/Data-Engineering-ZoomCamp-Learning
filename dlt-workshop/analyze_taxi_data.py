"""
Quick analysis script to answer homework questions
"""
import duckdb

# Connect to the DuckDB database
conn = duckdb.connect('/Users/saif/Desktop/ZoomCamp Learning/Data-Engineering-ZoomCamp-Learning/dlt-workshop/taxi_pipeline.duckdb')

print("="*70)
print("NYC TAXI DATA ANALYSIS - dlt Workshop Homework")
print("="*70)
print()

# Question 1: Date range
print("QUESTION 1: What is the start date and end date of the dataset?")
print("-"*70)
query = """
SELECT 
    DATE(MIN(trip_pickup_date_time)) as start_date,
    DATE(MAX(trip_pickup_date_time)) as end_date
FROM nyc_taxi_data.trips
"""
result = conn.execute(query).fetchdf()
print(f"Start Date: {result['start_date'][0]}")
print(f"End Date:   {result['end_date'][0]}")
print()

# Question 2: Credit card proportion
print("QUESTION 2: What proportion of trips are paid with credit card?")
print("-"*70)

# First check payment types
payment_types = conn.execute("""
SELECT payment_type, COUNT(*) as count
FROM nyc_taxi_data.trips
GROUP BY payment_type
ORDER BY count DESC
""").fetchdf()
print("Payment types:")
print(payment_types)
print()

query = """
SELECT 
    COUNT(*) as total_trips,
    SUM(CASE WHEN LOWER(payment_type) LIKE '%credit%' OR LOWER(payment_type) LIKE '%crd%' THEN 1 ELSE 0 END) as credit_trips,
    ROUND(100.0 * SUM(CASE WHEN LOWER(payment_type) LIKE '%credit%' OR LOWER(payment_type) LIKE '%crd%' THEN 1 ELSE 0 END) / COUNT(*), 2) as percentage
FROM nyc_taxi_data.trips
"""
result = conn.execute(query).fetchdf()
print(f"Total trips: {result['total_trips'][0]:,}")
print(f"Credit card trips: {result['credit_trips'][0]:,}")
print(f"Percentage: {result['percentage'][0]}%")
print()

# Question 3: Total tips
print("QUESTION 3: What is the total amount of money generated in tips?")
print("-"*70)
query = """
SELECT 
    SUM(tip_amt) as total_tips,
    ROUND(SUM(tip_amt), 2) as total_tips_rounded
FROM nyc_taxi_data.trips
"""
result = conn.execute(query).fetchdf()
print(f"Total tips: ${result['total_tips_rounded'][0]:,.2f}")
print()

print("="*70)
print("Analysis Complete!")
print("="*70)

conn.close()
