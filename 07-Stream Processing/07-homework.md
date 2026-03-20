# Module 7 Homework: Stream Processing with Redpanda and PyFlink

**Dataset:** NYC Green Taxi — October 2025  
**Stack:** Redpanda (Kafka-compatible), Apache Flink (PyFlink), Docker

---

## Answers Summary

| # | Question | Answer |
|---|----------|--------|
| Q1 | Redpanda version | `v25.3.9` |
| Q2 | Time to send full dataset to Kafka | `10 seconds` |
| Q3 | Trips with `trip_distance > 5` | `8,506` |
| Q4 | Most frequent `PULocationID` in 5-min tumbling window | `74` |
| Q5 | Trip count in longest session window | `81` |
| Q6 | Hour with largest total tip amount | `2025-10-16 18:00:00` |

---

## Environment Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.x with packages: `pandas`, `pyarrow`, `kafka-python`
- Workshop stack: `07-Stream Processing/class_materials/workshop/`

### Start the stack

```bash
cd "07-Stream Processing/class_materials/workshop/"

docker compose build
docker compose up -d
```

> If you have stale containers or volumes from a previous run:
> ```bash
> docker compose down -v
> docker compose build
> docker compose up -d
> ```

---

## Question 1 — Redpanda Version

**Answer: `v25.3.9`**

```bash
docker exec workshop-redpanda-1 rpk version
```

Output:
```
rpk version: v25.3.9
Redpanda Cluster ... v25.3.9
```

---

## Question 2 — Time to Produce Full Dataset

**Options:** 10s / 60s / 120s / 300s  
**Answer: `10 seconds`**

First, create (or reset) the topic:

```bash
docker exec workshop-redpanda-1 rpk topic delete green-trips
docker exec workshop-redpanda-1 rpk topic create green-trips
```

Producer script:

```python
import json
from time import time

import pandas as pd
from kafka import KafkaProducer

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount",
]

df = pd.read_parquet(URL, columns=COLUMNS)
for col in ["lpep_pickup_datetime", "lpep_dropoff_datetime"]:
    df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d %H:%M:%S")

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

t0 = time()
for row in df.to_dict(orient="records"):
    producer.send("green-trips", value=row)
producer.flush()
t1 = time()

print(f"Took {t1 - t0:.2f} seconds to produce {len(df):,} records")
```

Measured time in this environment: **~2.92 seconds** → closest option is **10 seconds**.

---

## Question 3 — Count Trips with `trip_distance > 5`

**Options:** 6,506 / 7,506 / 8,506 / 9,506  
**Answer: `8,506`**

Consumer logic:

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "green-trips",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

count = 0
for message in consumer:
    trip = message.value
    if float(trip.get("trip_distance") or 0) > 5.0:
        count += 1

print(f"Trips with trip_distance > 5: {count}")
```

Result: **8,506 trips**

---

## Question 4 — Top Pickup Location (5-Min Tumbling Window)

**Options:** 42 / 74 / 75 / 166  
**Answer: `74`**

PyFlink job using event-time tumbling windows over `lpep_pickup_datetime`.

**Source table DDL:**

```sql
CREATE TABLE green_trips (
    lpep_pickup_datetime VARCHAR,
    PULocationID         INT,
    event_time AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector'                     = 'kafka',
    'topic'                         = 'green-trips',
    'properties.bootstrap.servers'  = 'redpanda:29092',
    'properties.group.id'           = 'flink-consumer',
    'scan.startup.mode'             = 'earliest-offset',
    'format'                        = 'json'
);
```

**Aggregation query:**

```sql
SELECT
    window_start,
    window_end,
    PULocationID,
    COUNT(*) AS trip_count
FROM TABLE(
    TUMBLE(TABLE green_trips, DESCRIPTOR(event_time), INTERVAL '5' MINUTES)
)
GROUP BY window_start, window_end, PULocationID
ORDER BY trip_count DESC
LIMIT 1;
```

Top result: **`PULocationID = 74`**

---

## Question 5 — Longest Session Window (Trip Count)

**Options:** 12 / 31 / 51 / 81  
**Answer: `81`**

PyFlink session window job (gap = 5 minutes), with `env.set_parallelism(1)`.

**Session window query:**

```sql
SELECT
    PULocationID,
    window_start,
    window_end,
    COUNT(*) AS trip_count
FROM TABLE(
    SESSION(TABLE green_trips, DESCRIPTOR(event_time), INTERVAL '5' MINUTES)
)
GROUP BY PULocationID, window_start, window_end
ORDER BY trip_count DESC
LIMIT 1;
```

The session window with the highest trip count contained **81 trips**.

---

## Question 6 — 1-Hour Window with Largest Total Tip

**Options:** 2025-10-01 18:00 / 2025-10-16 18:00 / 2025-10-22 08:00 / 2025-10-30 16:00  
**Answer: `2025-10-16 18:00:00`**

**Source table** (same DDL as Q4/Q5, with `tip_amount` added):

```sql
CREATE TABLE green_trips (
    lpep_pickup_datetime VARCHAR,
    tip_amount           DOUBLE,
    event_time AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH ( ... );
```

**1-hour tumbling window query:**

```sql
SELECT
    window_start,
    SUM(tip_amount) AS total_tip
FROM TABLE(
    TUMBLE(TABLE green_trips, DESCRIPTOR(event_time), INTERVAL '1' HOUR)
)
GROUP BY window_start
ORDER BY total_tip DESC
LIMIT 1;
```

Hour with the highest total tip amount: **`2025-10-16 18:00:00`**