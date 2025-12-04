# 🚀 SpaceX ETL Pipeline (Python + PostgreSQL)

A complete end-to-end ETL pipeline that ingests live data from the SpaceX REST API, transforms it into a structured relational format, and loads it into a PostgreSQL database.

This project demonstrates core data engineering skills including API ingestion, data normalization, relational modeling, and automated loading using Python and SQLAlchemy.

---

## 📦 Features

### ✔ Extraction
- Pulls fresh data from:
  - `/v4/rockets`
  - `/v4/payloads`
  - `/v5/launches`
- Handles HTTP errors gracefully

### ✔ Transformation
- Normalizes nested JSON using `pandas.json_normalize`
- Converts list fields for PostgreSQL array storage
- Cleans boolean & timestamp formats
- Maps payloads and rockets correctly to launches

### ✔ Loading
- Pushes all cleaned tables into PostgreSQL
- Safe truncation using `TRUNCATE ... CASCADE`
- Converts Python lists → PostgreSQL arrays automatically
- Uses SQLAlchemy engine for connection management

---

## 🗂 Project Structure

```
project_1_etl/
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│
├── config.py
├── main.py
├── README.md
└── requirements.txt
```

---

## 🛠 Installation & Setup

### 1. Clone this repository

```bash
git clone https://github.com/<your-username>/spacex-etl-pipeline.git
cd spacex-etl-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the database connection  
Edit `config.py`:

```python
DB_CONNECTION_STRING = "postgresql+psycopg2://postgres:<password>@localhost:5432/spacex"
```

### 4. Create database tables  
Run this SQL in pgAdmin:

```sql
CREATE TABLE rockets (
    rocket_id   TEXT PRIMARY KEY,
    name        TEXT,
    type        TEXT,
    active      BOOLEAN,
    stages      INT,
    boosters    INT,
    company     TEXT,
    country     TEXT
);

CREATE TABLE payloads (
    payload_id     TEXT PRIMARY KEY,
    name           TEXT,
    type           TEXT,
    mass_kg        FLOAT,
    orbit          TEXT,
    customers      TEXT[],
    manufacturers  TEXT[]
);

CREATE TABLE launches (
    launch_id     TEXT PRIMARY KEY,
    name          TEXT,
    date_utc      TIMESTAMP,
    rocket_id     TEXT REFERENCES rockets(rocket_id),
    success       BOOLEAN,
    upcoming      BOOLEAN,
    flight_number INT
);
```

---

## ▶️ How to Run

```bash
python main.py
```

This will:

1. Extract fresh SpaceX data  
2. Clean & transform the datasets  
3. Load them into PostgreSQL  

Check your results in pgAdmin.

---

## 📝 Requirements

```
requests
pandas
SQLAlchemy
psycopg2-binary
```

---
