# SmartCity: End-to-End Real-Time Data Engineering Pipeline

## Project Description
This repository contains a robust real-time data streaming architecture designed to ingest, process, and analyze high-velocity IoT telemetry data. The project simulates a Smart City environment, tracking diverse data streams including vehicle movement, GPS coordinates, traffic camera snapshots, weather conditions, and emergency incidents.

The implementation focuses on a decoupled architecture, leveraging modern streaming protocols and serverless cloud storage for scalable analytics.

---

## 🎥 Pipeline in Action


https://github.com/user-attachments/assets/0991dc94-9c29-4a50-b3cf-a3cd707a33e3



---

## System Architecture
The pipeline is designed using a multi-layered approach to ensure reliability and schema consistency across the flow.

### 1. Ingestion Layer
- **Producer:** Python-based simulation engine generating JSON-encoded IoT events.
- **Message Broker:** Apache Kafka running in **KRaft Mode**. The removal of Zookeeper simplifies metadata management and improves cluster performance.

### 2. Processing Layer
- **Stream Processing:** Apache Spark Structured Streaming.
- **Fault Tolerance:** Implemented through Checkpointing on S3 and **Watermarking** to handle late-arriving events.
- **Schema Enforcement:** Strict StructType definitions are applied to ensure data quality.

### 3. Storage Layer (Data Lake)
- **Sink:** Amazon S3.
- **Format:** Data is persisted in **Parquet** (Columnar format) to optimize storage costs and query performance.

### 4. Cataloging & Analytics
- **Metadata Management:** AWS Glue Crawlers for automated schema discovery.
- **Query Engine:** Amazon Athena (Serverless SQL) for ad-hoc queries over the S3 Data Lake.
- **Business Intelligence:** Power BI connected via ODBC for real-time dashboarding.

---

## Technical Stack
- **Streaming:** Apache Kafka (KRaft), Confluent-Kafka Python.
- **Processing:** Apache Spark 3.5.0, PySpark.
- **Cloud (AWS):** S3, Glue, Athena, IAM.
- **Infrastructure:** Docker, Docker Compose.
- **Format:** Parquet, JSON.

---

## Repository Structure
```text
.
├── .gitignore
├── README.md
├── docker-compose.yml       # Infrastructure orchestration (Kafka & Spark)
├── main.py                  # Spark Structured Streaming application
└── spark-city.py            # IoT data generation & Kafka producer
