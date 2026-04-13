# NYC-Cab-Engine 🚖

A production-ready Medallion Data Architecture pipeline built to ingest, clean, and optimize massive-scale NYC Taxi & Limousine Commission (TLC) datasets. This project demonstrates the transition from flat-file analysis to a modular, containerized ETL system.

## 📌 Overview
NYC-Cab-Engine automates the lifecycle of urban mobility data. It handles the ingestion of raw, inconsistent Parquet files into a structured PostgreSQL warehouse. By implementing a **Schema Registry pattern**, the pipeline dynamically adapts to different journey types (Yellow, Green, FHV) while enforcing strict data types to minimize memory overhead and ensure "Silver-layer" data quality.

## 🛠️ Tech Stack
- **Language:** Python (Pandas/Polars)
- **Containerization:** Docker & Docker Compose
- **Database:** PostgreSQL 15 (Relational Storage)
- **Database UI:** pgAdmin 4 (Data Visualisation)
- **Architecture:** Medallion (Bronze & Silver Layers)
- **Environment Management:** Python-Dotenv

## 🏗️ Architecture
- `main.py`: The **Orchestrator**. Manages the end-to-end flow, from CLI argument parsing to triggering the transformation and load sequences.
- `src/ingest/`: The **Data Fetcher**. Programmatically retrieves monthly Parquet files from CloudFront and handles initial validation.
- `src/transform/`: The **Refinery**. Contains the logic for the Silver layer, including categorical mapping and memory-efficient type casting.
- `src/config/`: The **Control Plane**. Centralizes the Schema Registry and Mapping Dictionaries, ensuring the code is "Open-Closed" (open for new data types, closed to logic modification).
- `src/utils/`: The **Engine Room**. Houses the fast_postgres_upload utility using SQLAlchemy and psycopg2 for bulk-load efficiency.

## 🚀 Getting Started

### Prerequisites
- Docker Desktop installed.
- Python 3.10+ installed.

### Installation & Deployment
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/jdeglenholmes/nyc-cab-engine.git](https://github.com/jdeglenholmes/nyc-cab-engine.git)
   cd nyc-cab-engine

2. **Spin up the Infrastructure:**

  ```bash
  docker-compose up -d
  ```
  This initialises your Postgres database and pgAdmin web interface for managing processed NYC taxi data.

3. **Run the Pipeline:**
```bash
# Example: Ingest and process Yellow Taxi data for January 2026
python main.py --type yellow --year 2026 --month 1
```

### 🧠 Developer Story: Engineering for Scale
Transitioning this project from a Jupyter Notebook to a modular system allowed me to solve several "Production-Grade" engineering challenges.

| Feature | The "Prototype" (Analyst)  | The "Production"(Engineer) | Skill Demonstrated |
| :--- | :--- | :--- | :--- |
| **Schema Drift** | Hardcoded column names. | **Schema Registry Pattern** Dynamic config for Yellow/Green/FHV. | Scalability & Robustness |
| **Data Types** | Default  `Int64` / `Float64` | **Categorical Encoding:** Reduced disk footprint by ~40%. | Memory Optimisation |
| **Ingestion** | Row-by-row `to_sql` | **Bulk Copy / Fast Upload:** Optimised `psycopg2` buffer. | Performance Tuning |
| **Cleaning** | Manual ad-hoc filtering. | **Idempotent Logic:** Local sets to prevent config mutation. | Fault Tolerance | 
**Portability** | Hardcoded credentials | **Environment Injection:** Secure `.env` & Docker management. | Security & DevOps |


### 📊 Sample Gold Output
`yellow_tripdata_gold`
```
PICKUP_DATETIME      DROPOFF_DATETIME     PAYMENT_LABEL   VENDOR_LABEL   TOTAL_AMOUNT
2026-01-01 10:00     2026-01-01 10:15     Credit Card     VeriFone       15.50
2026-01-01 11:30     2026-01-01 11:45     Cash            CMT            12.00
```

### ❓ Troubleshooting
| Issue | Cause  | Solution |
| :--- | :--- | :--- |
| `ConnectionRefusedError`| Docker is not running. | Open Docker desktop and run `docker-compose up -d`. |
| `Database not found`| Volume not persisted | Ensure you didn't run `docker-compose down -v` (which deletes data) |