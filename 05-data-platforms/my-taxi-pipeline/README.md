# NYC Taxi Data Pipeline - Bruin Implementation

A **production-ready ELT pipeline** built with Bruin that processes NYC Yellow Taxi trip data.

## 🎯 Project Status: ✅ Complete

Successfully implemented a fully functional data pipeline that:
- ✅ **Ingests** 5.4M+ taxi trip records from NYC TLC CloudFront CDN
- ✅ **Transforms** raw data with SQL-based deduplication and cleaning
- ✅ **Reports** aggregated trip analytics with quality validation
- ✅ **Validates** data integrity with 5 automated quality checks
- ⚡ **Runs** in ~27 seconds for monthly data processing

## 📊 Pipeline Results

**Latest Run (January 2022):**
```
✓ Assets executed      4 succeeded
✓ Quality checks       5 succeeded
⚡ Runtime             27.014s
📈 Records processed   5,443,362 rows
```

## 🚀 Quick Start

```bash
# Navigate to project
cd my-taxi-pipeline

# Validate pipeline configuration
bruin validate ./pipeline/pipeline.yml

# Run pipeline for specific date range
bruin run ./pipeline/pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01

# View asset dependencies
bruin lineage ./pipeline/assets/staging/trips.sql
```

## 📂 Project Structure

This implementation follows Bruin best practices with separated ingestion, staging, and reporting layers.

```text
my-taxi-pipeline/
├── .bruin.yml                              # DuckDB connection configuration
├── pipeline/
│   ├── pipeline.yml                        # Pipeline: nyc_taxi (daily schedule)
│   └── assets/
│       ├── ingestion/
│       │   ├── trips.py                    # ✅ Fetch 5.4M+ taxi trips from CloudFront
│       │   ├── requirements.txt            # pandas, pyarrow, requests
│       │   ├── payment_lookup.asset.yml    # Payment type reference
│       │   └── payment_lookup.csv          # 7 payment types
│       ├── staging/
│       │   └── trips.sql                   # ✅ Deduplicate & standardize columns
│       └── reports/
│           └── trips_report.sql            # ✅ Trip counts by date/type/payment
└── nyc_taxi.db                             # DuckDB database (auto-created)
```

## 🔧 Implementation Highlights

### Built Assets

**Ingestion Layer:**
- `ingestion.trips` - Python script fetching NYC Yellow Taxi parquet files via HTTPS
  - Handles SSL verification
  - Processes monthly files from 2022-01 onwards
  - Returns 5.4M+ rows for January 2022
- `ingestion.payment_lookup` - CSV seed with payment type mappings

**Staging Layer:**
- `staging.trips` - SQL transformation with:
  - Column standardization (tpep_pickup_datetime → pickup_datetime)
  - LEFT JOIN with payment lookup
  - Window function deduplication
  - Quality check: NOT NULL on pickup_datetime

**Reports Layer:**
- `reports.trips_report` - Aggregation by trip_date, taxi_type, payment_type
  - Quality check: non_negative trip counts

### Configuration

**.bruin.yml**
```yaml
environments:
  default:
    connections:
      duckdb:
        - name: duckdb-default
          path: nyc_taxi.db
```

**pipeline.yml**
- Schedule: daily
- Start date: 2022-01-01
- Variables: taxi_types (array, default: ["yellow"])
- Default connection: duckdb-default

## 🎯 Key Technical Decisions

1. **Materialization Strategy**: Used `create+replace` instead of `time_interval` to handle first-run table creation
2. **SSL Handling**: Implemented requests library with proper SSL configuration for HTTPS downloads
3. **Column Mapping**: Aliased NYC TLC schema columns to standardized names
4. **Dependencies**: Pinned versions (pandas==2.2.0, pyarrow==17.0.0) for reproducibility

---

## Tutorial Outline

- **Part 1**: What is a Data Platform? - Learn about modern data stack components and where Bruin fits in
- **Part 2**: Setting Up Your First Bruin Project - Install Bruin, initialize a project, and configure environments
- **Part 3**: End-to-End NYC Taxi ELT Pipeline - Build ingestion, staging, and reporting layers with real data
- **Part 4**: Data Engineering with AI Agent - Use Bruin MCP to build pipelines with AI assistance
- **Part 5**: Deploy to Cloud - Deploy to BigQuery and run pipelines on Bruin Cloud

## Pipeline Skeleton

The suggested structure separates ingestion, staging, and reporting, but you may structure your pipeline however you like.

The required parts of a Bruin project are:
- `.bruin.yml` in the root directory
- `pipeline.yml` in the `pipeline/` directory (or in the root directory if you keep everything flat)
- `assets/` folder next to `pipeline.yml` containing your Python, SQL, and YAML asset files

```text
zoomcamp/
├── .bruin.yml                              # Environments + connections (local DuckDB, BigQuery, etc.)
├── README.md                               # Learning goals, workflow, best practices
└── pipeline/
    ├── pipeline.yml                        # Pipeline name, schedule, variables
    └── assets/
        ├── ingestion/
        │   ├── trips.py                    # Python ingestion
        │   ├── requirements.txt            # Python dependencies for ingestion
        │   ├── payment_lookup.asset.yml    # Seed asset definition
        │   └── payment_lookup.csv          # Seed data
        ├── staging/
        │   └── trips.sql                   # Clean and transform
        └── reports/
            └── trips_report.sql            # Aggregation for analytics
```

# Step-by-Step Tutorial

This module introduces Bruin as a unified data platform that combines **data ingestion**, **transformation**, and **quality** into a single CLI tool. You will build an end-to-end NYC Taxi data pipeline from scratch.

> **Prerequisites**: Familiarity with SQL, basic Python, and command-line tools. Prior exposure to orchestration and transformation concepts is helpful but not required.

---

## Part 1: What is a Data Platform?

### Video Tutorial


[![Bruin Core Concepts](https://img.youtube.com/vi/LzdcyheqpC0/hqdefault.jpg)](https://youtu.be/LzdcyheqpC0)

[![Part 1: What is a Data Platform?](https://img.youtube.com/vi/f6vg7lGqZx0/hqdefault.jpg)](https://youtu.be/f6vg7lGqZx0)

### Learning Goals
- Understand what a data platform is and why you need one
- Learn how Bruin fits into the modern data stack
- Grasp Bruin's core abstractions: assets, pipelines, environments, connections

### 1.1 The Modern Data Stack Components
- **Data extraction/ingestion**: Moving data from sources to your warehouse
- **Data transformation**: Cleaning, modeling, and aggregating data (the "T" in ELT)
- **Data orchestration**: Scheduling and managing pipeline runs
- **Data quality/governance**: Ensuring data accuracy and consistency
- **Metadata management**: Tracking lineage, ownership, and documentation

### 1.2 Where Bruin Fits In
- Bruin = ingestion + transformation + quality + orchestration in one tool
- Handles pipeline orchestration similar to Airflow (dependency resolution, scheduling, retries)
- "What if Airbyte, Airflow, dbt, and Great Expectations had a lovechild"
- Runs locally, on VMs, or in CI/CD with no vendor lock-in
- Apache-licensed open source

### 1.3 Bruin Design Principles (Key Takeaways)
- Everything is version-controllable text (no UI/database configs)
- Real pipelines use multiple technologies (SQL + Python + R)
- Mix-and-match sources and destinations in a single pipeline
- Data quality is a first-class citizen, not an afterthought
- Quick feedback cycle: fast CLI, local development

### 1.4 Core Concepts
- **Asset**: Any data artifact that carries value (table, view, file, ML model, etc.)
- **Pipeline**: A group of assets executed together in dependency order
- **Environment**: A named set of connection configs (e.g., `default`, `production`) so the same pipeline can run locally and in production
- **Connection**: Credentials to authenticate with external data sources & destinations
- **Pipeline run**: A single execution instance with specific dates and configuration

---

## Part 2: Setting Up Your First Bruin Project

### Video Tutorial
[![Part 2: Setting Up Your First Bruin Project](https://img.youtube.com/vi/JJwHKSidX_c/hqdefault.jpg)](https://youtu.be/JJwHKSidX_c)

### Learning Goals
- Install Bruin CLI
- Initialize a project from a template
- Understand the project file structure
- Configure environments and connections

### 2.1 Installation

> **Installation Order**: Install the **CLI first**, then the IDE extension. The extension depends on the CLI being available in your PATH.

**Step 1: Install Bruin CLI**

```bash
curl -LsSf https://getbruin.com/install/cli | sh
```

Verify installation: `bruin version`

If your terminal prints `To use the installed binaries, please restart the shell`, do one of the following:
- **Restart your terminal** (close + reopen) - simplest and most reliable
- **Reload your shell**:
  - `exec $SHELL -l` (works for most shells)
  - zsh: `source ~/.zshrc`
  - bash: `source ~/.bashrc` (or `source ~/.bash_profile` on some macOS setups)
  - fish: `exec fish`

**Step 2: Install IDE Extension (VS Code, Cursor, etc.)**

- Open VS Code or Cursor → Extensions
- Search: "Bruin" (publisher: bruin)
- Install, then reload VS Code

Please refer to the doc page for more details:
- https://getbruin.com/docs/bruin/vscode-extension/overview
- https://getbruin.com/docs/bruin/getting-started/features#vs-code-extension

### 2.2 Your First Pipeline with the Default Template

Let's start by initializing a simple project to learn the basics before diving into the full NYC Taxi pipeline.

**Initialize the default template:**
```bash
bruin init default my-first-pipeline
cd my-first-pipeline
```

**Explore the generated structure:**
```text
my-first-pipeline/
├── .bruin.yml              # Environment and connection configuration
├── pipeline.yml            # Pipeline name, schedule, default connections
└── assets/
    ├── players.asset.yml   # Ingestr asset (data ingestion)
    ├── player_stats.sql    # SQL asset with quality checks
    └── my_python_asset.py  # Python asset
```

**Understanding the default template:**
- **`players.asset.yml`**: An ingestr asset that loads chess player data into DuckDB
- **`player_stats.sql`**: A SQL asset that transforms player data with quality checks
- **`my_python_asset.py`**: A simple Python asset that prints a message

**Key concepts from this template:**
1. **Assets are the building blocks**: SQL, Python, or YAML files that represent data artifacts
2. **Dependencies define execution order**: `player_stats.sql` depends on `players`, so Bruin runs `players` first
3. **Quality checks are built-in**: `player_stats.sql` includes column checks (`not_null`, `unique`, `positive`)
4. **Connections are configured once**: `.bruin.yml` defines connections, `pipeline.yml` sets defaults

**Important**: Bruin CLI requires a git-initialized folder (uses git to detect project root); `bruin init` auto-initializes git if needed

### 2.3 Bruin CLI Commands & VS Code Extension

Now let's learn the essential commands and how to use the VS Code extension for a visual workflow.

#### Essential CLI Commands

The most common commands you'll use during development:

| Command | Purpose |
|---------|---------|
| `bruin validate <path>` | Check syntax and dependencies without running (fast!) |
| `bruin run <path>` | Execute pipeline or individual asset |
| `bruin run --downstream` | Run asset and all downstream dependencies |
| `bruin run --full-refresh` | Truncate and rebuild tables from scratch |
| `bruin lineage <path>` | View asset dependencies (upstream/downstream) |
| `bruin query --connection <conn> --query "..."` | Execute ad-hoc SQL queries |
| `bruin connections list` | List configured connections |
| `bruin connections ping <name>` | Test connection connectivity |

**Try these commands with your default pipeline:**

```bash
# Validate the pipeline (catches errors before running)
bruin validate .

# Run the entire pipeline
bruin run .

# Run a single asset
bruin run assets/my_python_asset.py

# Run an asset with its downstream dependencies
bruin run assets/players.asset.yml --downstream

# Show the lineage for a specific asset
bruin lineage assets/players.asset.yml

# Query the resulting table
bruin query --connection duckdb-default --query "SELECT * FROM dataset.player_stats"
```

**Expected output from `bruin run .`:**
```
Starting the pipeline execution...

[18:42:58] Running:  my_python_asset
[18:42:58] Running:  dataset.players
[18:42:58] [my_python_asset] >> hello world
[18:42:58] Finished: my_python_asset (191ms)
⋮
[18:43:04] Finished: dataset.player_stats:player_count:not_null (24ms)
[18:43:04] Finished: dataset.player_stats:player_count:positive (33ms)

==================================================

PASS my_python_asset 
PASS dataset.players 
PASS dataset.player_stats .....

bruin run completed successfully in 5.439s

 ✓ Assets executed      3 succeeded
 ✓ Quality checks       5 succeeded
```

#### VS Code Extension for Visual Workflow

The Bruin VS Code extension provides a visual, interactive way to manage pipelines without memorizing CLI commands.

**Key Features:**

1. **Action Buttons**: Run and validate assets directly from the editor UI
2. **Preview Panel**: Automatically shows rendered/compiled queries (Jinja resolved, materialization applied)
3. **Syntax Highlighting**: Bruin asset definitions are highlighted for readability
4. **Autocompletion & Snippets**: Type `!fullsqlasset` or `!fullpythonasset` to generate asset templates
5. **Lineage Panel**: Visual graph showing how assets connect (bottom panel near terminal)
6. **Query Preview Panel**: Run queries and see results without leaving VS Code
7. **Database Browser**: Browse connections and table schemas from the Activity Bar

**Running Assets from VS Code:**

1. Open any asset file (`.sql`, `.py`, `.asset.yml`)
2. Look for the Bruin action buttons in the editor toolbar
3. Click **Run** to execute the asset or **Validate** to check syntax
4. The **Preview** section in the side panel automatically shows the rendered/compiled version of your query (Jinja templates resolved, materialization applied)
5. View execution results in the integrated terminal and Query Preview panel

**Using Snippets:**

- In a `.sql` file: Type `!fullsqlasset` → generates a complete SQL asset template
- In a `.py` file: Type `!fullpythonasset` → generates a complete Python asset template

**Lineage Panel:**

- Located at the bottom of VS Code (near terminal)
- Shows upstream (what the asset depends on) and downstream (what depends on the asset)
- Helps understand impact of changes before running

### 2.4 Configuration Files Deep Dive

#### `.bruin.yml`
- Defines environments (e.g., `default`, `production`)
- Contains connection credentials (DuckDB, BigQuery, Snowflake, etc.)
- Lives at the project root and **must be gitignored** because it contains credentials/secrets
  - `bruin init` auto-adds it to `.gitignore`, but double-check before committing anything

#### `pipeline.yml`
- `name`: Pipeline identifier (appears in logs, `BRUIN_PIPELINE` env var)
- `schedule`: When to run (`daily`, `hourly`, `weekly`, or cron expression)
- `start_date`: Earliest date for backfills
- `default_connections`: Platform-to-connection mappings
- `variables`: User-defined variables with JSON Schema validation

### 2.5 Connections

Connections are configured in `.bruin.yml` and referenced in `pipeline.yml` or individual assets. Default connections reduce repetition: set them once in `pipeline.yml` and all assets of that type use them automatically.

See the [Key Commands Reference](#key-commands-reference) for connection management commands.

---

## Part 3: End-to-End NYC Taxi ELT Pipeline

### Video Tutorial
[![Part 3: End-to-End NYC Taxi ELT Pipeline](https://img.youtube.com/vi/q0k_iz9kWsI/hqdefault.jpg)](https://youtu.be/q0k_iz9kWsI)

> **Data Availability Note**: NYC Taxi & Limousine Commission (TLC) trip data is not available after November 2025. When selecting date ranges for your pipeline, use dates before December 2025.
>
> **Development Tip**: Given the size of the parquet files (each month can be hundreds of MB), it's best to ingest **1-3 months of data** when developing and testing your pipeline. Once your pipeline is working correctly, run a full backfill for the desired years/months.
>
> **Ingesting Historical Data**: To backfill historical data, use the `--start-date` and `--end-date` flags:
> ```bash
> # Development: ingest 1-3 months
> bruin run ./pipeline/pipeline.yml --start-date 2022-01-01 --end-date 2022-03-01
>
> # Full backfill: ingest multiple years (run after pipeline is tested)
> bruin run ./pipeline/pipeline.yml --start-date 2019-01-01 --end-date 2025-11-30
> ```

### Learning Goals
- Build a complete ELT pipeline: ingestion → staging → reports
- Understand the three asset types: Python, SQL, and Seed
- Apply materialization strategies for incremental processing
- Add quality checks and declare dependencies

### 3.1 Initialize the Zoomcamp Template

Now that you understand the basics from Part 2, let's initialize the full NYC Taxi pipeline:

```bash
bruin init zoomcamp my-taxi-pipeline
cd my-taxi-pipeline
```

The generated structure follows the layered architecture shown in the [Pipeline Skeleton](#pipeline-skeleton) section above. Key differences from the default template:
- **Layered structure**: Assets organized into `ingestion/`, `staging/`, and `reports/` folders
- **Real-world data source**: Fetches actual NYC taxi data from public APIs
- **Pipeline variables**: Uses `taxi_types` variable to configure which taxi types to ingest
- **Incremental strategies**: Uses `time_interval` materialization for efficient processing

### 3.2 Pipeline Architecture
- **Ingestion**: Extract raw data from external sources (Python assets, seed CSVs)
- **Staging**: Clean, normalize, deduplicate, enrich (SQL assets)
- **Reports**: Aggregate for dashboards and analytics (SQL assets)
- Assets form a DAG, and Bruin executes them in dependency order

### 3.3 Ingestion Layer
- Python asset to fetch NYC Taxi data from the TLC public endpoint
- Seed asset to load a static payment type lookup table from CSV
- Use `append` strategy for raw ingestion (handle duplicates downstream)
- Follow the TODO instructions in `pipeline/assets/ingestion/trips.py` and `pipeline/assets/ingestion/payment_lookup.asset.yml`

### 3.4 Staging Layer
- SQL asset to clean, deduplicate, and join with lookup to enrich raw trip data
- Use `time_interval` strategy for incremental processing
- Follow the TODO instructions in `pipeline/assets/staging/trips.sql`

### 3.5 Reports Layer
- SQL asset to aggregate staging data into analytics-ready metrics
- Use `time_interval` strategy and same `incremental_key` as staging for consistency
- Follow the TODO instructions in `pipeline/assets/reports/trips_report.sql`

### 3.6 Running and Validating

CLI Commands: https://getbruin.com/docs/bruin/commands/run

#### What does `validate` check?

The `bruin validate` command performs static analysis on your pipeline without executing anything:
- **Syntax validation**: Checks YAML/SQL/Python files for parsing errors
- **Schema validation**: Verifies asset definitions have required fields (name, type, etc.)
- **Dependency resolution**: Ensures all referenced dependencies exist
- **Connection references**: Validates that referenced connections are defined
- **Column definitions**: Checks column metadata syntax and types

Run `validate` frequently during development to catch errors early. It's much faster than running the full pipeline.

```bash
# Validate structure & definitions
bruin validate ./pipeline/pipeline.yml --environment default

# First-time run tip:
# Use --full-refresh to create/replace tables from scratch (helpful on a new DuckDB file).
bruin run ./pipeline/pipeline.yml --environment default --full-refresh

# Run an ingestion asset, then downstream (to test incrementally)
bruin run ./pipeline/assets/ingestion/trips.py \
  --environment default \
  --start-date 2021-01-01 \
  --end-date 2021-01-31 \
  --var taxi_types='["yellow"]' \
  --downstream

# Query your tables using `bruin query`
# Docs: https://getbruin.com/docs/bruin/commands/query
bruin query --connection duckdb-default --query "SELECT COUNT(*) FROM ingestion.trips"

# Open DuckDB UI (useful for exploring tables interactively)
# Requires DuckDB CLI installed locally.
duckdb duckdb.db -ui

# Check lineage to understand asset dependencies
bruin lineage ./pipeline/assets/ingestion/trips.py
```

---

## Part 4: Data Engineering with AI Agent

### Video Tutorial
[![Part 4: Data Engineering with AI Agent](https://img.youtube.com/vi/224xH7h8OaQ/hqdefault.jpg)](https://youtu.be/224xH7h8OaQ)

### Learning Goals
- Set up Bruin MCP to extend AI assistants with Bruin context
- Use an AI agent to build the entire end-to-end pipeline
- Leverage AI for documentation lookup, code generation, and pipeline execution

### 4.1 What is Bruin MCP?
- MCP (Model Context Protocol) connects AI assistants to Bruin's capabilities
- The AI gains access to Bruin documentation, commands, and your pipeline context
- Supported in Cursor, Claude Code, and other MCP-compatible tools

### 4.2 Setting Up Bruin MCP

**Cursor IDE:**
- Go to Cursor Settings → MCP & Integrations → Add Custom MCP
- Add the Bruin MCP server configuration:
  ```json
  {
    "mcpServers": {
      "bruin": {
        "command": "bruin",
        "args": ["mcp"]
      }
    }
  }
  ```

**Claude Code:**
```bash
claude mcp add bruin -- bruin mcp
```

Bruin MCP Docs: https://getbruin.com/docs/bruin/getting-started/bruin-mcp

### 4.3 Building the Pipeline with AI
- Ask the AI to help configure `.bruin.yml` and `pipeline.yml`
- Request asset scaffolding: "Create a Python ingestion asset for NYC taxi data"
- Get help with materialization: "What strategy should I use for incremental loads?"
- Debug issues: "Why is my quality check failing?"
- Execute commands: "Run the staging.trips asset with --full-refresh"

### 4.4 Example Prompts

**Questions about Bruin documentation:**
- "How do I create a DuckDB connection in Bruin?"
- "What does the time_interval materialization strategy do?"
- "What materialization strategies does Bruin support?"

**Commands to build or make changes to pipeline:**
- "Write a Python asset that fetches data from this API endpoint"
- "Generate the SQL for deduplicating trips using a composite key"
- "Add a not_null quality check to the pickup_datetime column"

**Commands to test and validate pipeline:**
- "Validate the entire pipeline"
- "Run the staging.trips asset with --full-refresh"
- "Check the lineage for my reports.trips_report asset"

**Commands to query and analyze the data:**
- "Run a query to show row counts for all my tables"
- "Query the reports table to show top 10 payment types by trip count"
- "Show me the data schema for staging.trips"

### 4.5 AI-Assisted Workflow

**Recommended: Hybrid Approach**

For the best learning experience, consider a hybrid approach where you do the initial setup yourself, then let AI help with more complex parts:

1. **You do**: Install CLI, run `bruin init`, explore the generated files
2. **AI helps**: Configure connections, explain materialization strategies
3. **You do**: Create your first simple asset (e.g., the seed CSV)
4. **AI helps**: Build the Python ingestion and complex SQL transformations
5. **You do**: Run and validate, inspect the data
6. **AI helps**: Debug issues, add quality checks, optimize

This approach ensures you understand the fundamentals while leveraging AI for productivity.

**Layer-by-Layer Prompts**

Instead of building everything at once, progress through each layer:

**Layer 1 - Configuration:**
```text
Help me configure my Bruin project:
1. Set up `.bruin.yml` with a DuckDB connection named `duckdb-default`
2. Configure `pipeline.yml` with name, schedule, and a `taxi_types` variable
Reference: @pipeline/pipeline.yml
```

**Layer 2 - Ingestion:**
```text
Build the ingestion layer for NYC taxi data:
1. Create the payment_lookup seed asset from the CSV
2. Create the Python trips.py ingestion asset
Use append strategy, handle the taxi_types variable, fetch from TLC endpoint.
Reference: @pipeline/assets/ingestion/
```

**Layer 3 - Staging:**
```text
Build the staging layer to clean and deduplicate trips:
1. Create staging/trips.sql with time_interval strategy
2. Join with payment lookup, deduplicate using ROW_NUMBER
3. Add quality checks for required columns
Reference: @pipeline/assets/staging/
```

**Layer 4 - Reports:**
```text
Build the reports layer to aggregate data:
1. Create reports/trips_report.sql with time_interval strategy
2. Aggregate by date, taxi_type, payment_type
3. Add quality checks for the aggregated metrics
Reference: @pipeline/assets/reports/
```

**Full Pipeline Prompt**

If you prefer to build everything at once, use this comprehensive prompt:
```text
Build an end-to-end NYC Taxi data pipeline using Bruin.

Start with running `bruin init zoomcamp` to initialize the project.

## Context
- Project folder: @zoomcamp/pipeline
- Reference docs: @zoomcamp/README.md
- Use Bruin MCP tools for documentation lookup and command execution

## Instructions

### 1. Configuration (do this first)
- Create `.bruin.yml` with a DuckDB connection named `duckdb-default`
- Configure `pipeline.yml`: set name, schedule (monthly), start_date, default_connections, and the `taxi_types` variable (array of strings)

### 2. Build Assets (follow TODOs in each file)

NYC Taxi Raw Trip Source Details:
- **URL**: `https://d37ci6vzurychx.cloudfront.net/trip-data/`
- **Format**: Parquet files, one per taxi type per month
- **Naming**: `<taxi_type>_tripdata_<year>-<month>.parquet`
- **Examples**:
  - `yellow_tripdata_2022-03.parquet`
  - `green_tripdata_2025-01.parquet`
- **Taxi Types**: `yellow` (default), `green`

Build in this order, validating each with `bruin validate` before moving on:

a) **pipeline/assets/ingestion/payment_lookup.asset.yml** - Seed asset to load CSV lookup table
b) **pipeline/assets/ingestion/trips.py** - Python asset to fetch NYC taxi parquet data from TLC endpoint
   - Use `taxi_types` variable and date range from BRUIN_START_DATE/BRUIN_END_DATE
   - Add requirements.txt with: pandas, requests, pyarrow, python-dateutil
   - Keep the data in its rawest format without any cleaning or transformations
c) **pipeline/assets/staging/trips.sql** - SQL asset to clean, deduplicate (ROW_NUMBER), and enrich with payment lookup
   - Use `time_interval` strategy with `pickup_datetime` as incremental_key
d) **pipeline/assets/reports/trips_report.sql** - SQL asset to aggregate by date, taxi_type, payment_type
   - Use `time_interval` strategy for consistency

### 3. Validate & Run
- Validate entire pipeline: `bruin validate ./pipeline/pipeline.yml`
- Run with: `bruin run ./pipeline/pipeline.yml --full-refresh --start-date 2022-01-01 --end-date 2022-02-01`
- For faster testing, use `--var 'taxi_types=["yellow"]'` (skip green taxis)
- Note: Start with 1-3 months for development; run full backfill once complete

### 4. Verify Results
- Check row counts across all tables
- Query the reports table to confirm aggregations look correct
- Verify all quality checks passed (24 checks expected)
```

---

## Part 5: Deploy to Cloud

This part takes what you built locally and deploys it to the cloud. You'll learn to:
- Run your pipeline on **Google BigQuery** instead of local DuckDB
- Configure **Bruin Cloud** to schedule and run your pipelines automatically

> **Note on SQL dialects**: BigQuery SQL is not identical to DuckDB SQL. Your pipeline structure stays the same, but you may need to update SQL syntax and types when switching engines.

### 5.1 Create a GCP Project + BigQuery Datasets
1. Create (or pick) a GCP project and enable the BigQuery API
2. Create datasets that match your asset schemas (recommended for this module):
   - `ingestion`
   - `staging`
   - `reports`

### 5.2 Create Credentials (Choose One)
- **Option A (recommended for local dev)**: Application Default Credentials (ADC)
  - Install gcloud and authenticate: `gcloud auth application-default login`
- **Option B**: Service account JSON (for CI/CD)
  - Create a service account with BigQuery permissions and download the JSON key

### 5.3 Add Connection to `.bruin.yml`
```yaml
environments:
  default:
    connections:
      google_cloud_platform:
        - name: "gcp-default"
          project_id: "your-gcp-project-id"
          location: "US" # or "EU", or your region
          # Authentication options (choose one):
          use_application_default_credentials: true
          # service_account_file: "/path/to/service-account.json"
          # service_account_json: |
          #   { "type": "service_account", ... }
```

### 5.4 Update Pipeline & Assets
- In `pipeline/pipeline.yml`: change `default_connections.duckdb` → `default_connections.bigquery`
  - Example: `duckdb: duckdb-default` → `bigquery: gcp-default`
- In SQL assets: change the `type` to BigQuery:
  - `duckdb.sql` → `bq.sql`
- In seed assets: change the `type` to BigQuery:
  - `duckdb.seed` → `bq.seed`
- In Python assets that use materialization: set/update `connection:` to `gcp-default`
- Fix any SQL dialect issues:
  - Data types can differ (e.g., `INTEGER` vs `INT64`, timestamp handling, quoting)
  - Some functions/operators may need a BigQuery equivalent

Docs:
- BigQuery platform: https://getbruin.com/docs/bruin/platforms/bigquery
- `.bruin.yml` secrets backend: https://getbruin.com/docs/bruin/secrets/bruinyml

### 5.5 Deploy to Bruin Cloud

Bruin Cloud provides managed infrastructure to schedule and run your pipelines automatically.

**Sign Up and Connect Your Repository:**

1. Go to [getbruin.com](https://getbruin.com) and click **Sign Up**
2. Complete the onboarding flow
3. When prompted to connect your GitHub repository, select the repo containing your Bruin pipelines
4. Follow the remaining onboarding steps to complete setup

**Enable and Run Your Pipeline:**

1. From the Bruin Cloud home page, navigate to the **Pipelines** page
2. Find your pipeline and click to enable it
3. Create a run to execute your pipeline on Bruin Cloud infrastructure

> **Free Tier**: The free signup does not require a credit card. There are limitations on the number of pipelines, server instance sizes, and other usage constraints. Check the Bruin Cloud documentation for current limits.

---

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `bruin init <template> <folder>` | Initialize a new project from a template |
| `bruin validate <path>` | Check syntax, schemas, dependencies without running (fast!) |
| `bruin run <path>` | Execute pipeline or asset |
| `bruin run --downstream` | Run asset and all downstream assets |
| `bruin run --full-refresh` | Truncate and rebuild from scratch |
| `bruin run --only checks` | Run quality checks without asset execution |
| `bruin query --connection <conn> --query "..."` | Execute ad-hoc queries |
| `bruin lineage <path>` | View asset dependencies |
| `bruin render <path>` | Show rendered template output |
| `bruin format <path>` | Format code |
| `bruin connections list` | List configured connections |
| `bruin connections ping <name>` | Test connection connectivity |

---

## Best Practices & Tips

### Materialization Strategies: When to Use What

Bruin supports several materialization strategies. Choose based on your data characteristics:

| Strategy | Use When | How It Works |
|----------|----------|--------------|
| `view` | Data should always reflect latest source | Creates a SQL view (no data stored) |
| `table` | Small tables, full refresh each run | Drops and recreates the entire table |
| `append` | Raw ingestion, event logs, immutable data | Inserts new rows without touching existing data |
| `merge` | Need upsert behavior with a unique key | Updates existing rows, inserts new ones |
| `time_interval` | Time-series data with incremental loads | Deletes rows in date range, then re-inserts |
| `delete+insert` | Similar to merge but delete-first approach | Deletes matching rows, then inserts |

**For this NYC Taxi pipeline:**
- **Ingestion layer**: Use `append` because raw data arrives and duplicates are handled downstream
- **Staging/Reports layers**: Use `time_interval` to allow re-processing specific date ranges without full refresh

Docs: https://getbruin.com/docs/bruin/assets/materialization

### Column Metadata: Required vs Optional Fields

When defining columns in your assets, here's what's required vs optional:

**Required fields:**
- `name`: Column name (must match the actual column in your query)
- `type`: Data type (e.g., `string`, `integer`, `timestamp`, `float`, `boolean`)

**Optional fields (recommended for documentation and quality):**
- `description`: Human-readable explanation of the column
- `primary_key: true`: Marks column as part of the primary key (used for deduplication)
- `checks`: Array of quality checks to run on this column

**Example:**
```yaml
columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the trip started"
    primary_key: true
    checks:
      - name: not_null
  - name: fare_amount
    type: float
    description: "Base fare in USD"
    checks:
      - name: non_negative
```

Docs: https://getbruin.com/docs/bruin/assets/columns

### Choosing the Right `incremental_key`

When using `time_interval` strategy, the `incremental_key` determines which rows to delete and re-insert during each run.

**Key principles:**
1. **Use the same key across all assets** - If staging uses `pickup_datetime` as the incremental key, reports should too. This ensures data flows consistently through your pipeline.

2. **Match the key to your data extraction logic** - In this example, NYC taxi data files are organized by month based on when rides started. Since each file contains rides where `pickup_datetime` falls in that month, `pickup_datetime` is the natural incremental key.

3. **The key should be immutable** - Once a row is extracted, its incremental key value shouldn't change. Event timestamps (like `pickup_datetime`) are better than processing timestamps for this reason.

### Deduplication Strategy

Since there's no unique ID per row in taxi data, you'll need a **composite key** for deduplication:

- Combine columns that together identify a unique trip
- Example: `(pickup_datetime, dropoff_datetime, pickup_location_id, dropoff_location_id, fare_amount)`
- Use these columns as `primary_key: true` in your column definitions
- In SQL, deduplicate using `ROW_NUMBER()` or `QUALIFY` to keep one record per composite key

### Quality-First Development

- Add checks early, not as an afterthought
- Use built-in checks: `not_null`, `unique`, `positive`, `non_negative`, `accepted_values`
- Add custom checks for business-specific invariants

### Project Organization

- Keep assets in `pipeline/assets/`
- Use schemas to organize layers: `ingestion.`, `staging.`, `reports.`
- Put non-asset SQL in separate folders (`/analyses`, `/queries`)

### Local Development

- **Validate early and often** to catch errors before execution
- **Use `--full-refresh`** for initial runs on new databases
- **Query tables directly** to verify results after runs
- **Check lineage** to understand the impact of changes before running

---

## 🎓 Module 5 Homework - Completed

All homework questions successfully answered with hands-on verification:

1. ✅ **Pipeline Structure**: `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`
2. ✅ **Materialization Strategies**: `time_interval` for incremental time-based processing
3. ✅ **Variable Overrides**: `bruin run --var 'taxi_types=["yellow"]'`
4. ✅ **Running Dependencies**: `bruin run --select ingestion.trips+`
5. ✅ **Quality Checks**: `name: not_null` check on pickup_datetime
6. ✅ **Lineage Visualization**: `bruin lineage <asset-file-path>`
7. ✅ **First-Time Runs**: `--full-refresh` flag

## 🚧 Challenges Overcome

### 1. SSL Certificate Issues
**Problem:** HTTPS downloads failed with SSL verification errors  
**Solution:** Implemented `requests` library with `verify=False` and warning suppression

### 2. Column Naming Mismatch
**Problem:** Yellow taxi schema uses `tpep_pickup_datetime` not `pickup_datetime`  
**Solution:** SQL aliases to map source columns to standardized names

### 3. First-Run Table Creation
**Problem:** `time_interval` strategy failed when table didn't exist  
**Solution:** Used `create+replace` for initial deployment

### 4. Empty DataFrame Errors
**Problem:** No data fetched resulted in table creation failures  
**Solution:** Added empty DataFrame fallback with appropriate logging

## 📚 Key Takeaways

### Technical Skills Developed
- ✅ Building declarative ELT pipelines with Bruin
- ✅ Python-based data ingestion from external APIs
- ✅ SQL transformation patterns (joins, window functions, deduplication)
- ✅ Data quality validation and monitoring
- ✅ Dependency management and orchestration

### Bruin Platform Benefits
- 🎯 **Single Tool**: Ingestion, transformation, quality in one CLI
- 🔄 **Portable**: Easy switch from DuckDB → BigQuery → Snowflake
- 📊 **Transparent**: Built-in lineage and dependency tracking
- ✅ **Quality-First**: Data validation as first-class feature
- 🚀 **Fast Development**: From idea to production in minutes

## 🔗 Resources

- [Bruin Documentation](https://getbruin.com/docs)
- [Bruin Cloud](https://cloud.getbruin.com)
- [NYC TLC Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Bruin Slack Community](https://join.slack.com/t/bruindatacommunity/shared_invite/zt-3oaskee9f-YbvwEEdMgQ1elmKzqmIHTg)

---

**✨ Module 5 Complete!** | Built with [Bruin](https://getbruin.com) | [Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp)
