# SmartCity: End-to-End Real-Time Data Engineering Pipeline

## Project Description
This repository contains a robust real-time data streaming architecture designed to ingest, process, and analyze high-velocity IoT telemetry data. The project simulates a Smart City environment, tracking diverse data streams including vehicle movement, GPS coordinates, traffic camera snapshots, weather conditions, and emergency incidents.

The implementation focuses on a decoupled architecture, leveraging modern streaming protocols and serverless cloud storage for scalable analytics.

---

## System Architecture
The pipeline is designed using a multi-layered approach to ensure reliability and schema consistency across the flow.



### 1. Ingestion Layer
- **Producer:** Python-based simulation engine generating JSON-encoded IoT events.
- **Message Broker:** Apache Kafka running in **KRaft Mode**. The removal of Zookeeper simplifies the metadata management and improves cluster startup performance.

### 2. Processing Layer
- **Stream Processing:** Apache Spark Structured Streaming.
- **Fault Tolerance:** Implemented through Checkpointing on S3 and **Watermarking** to handle late-arriving events and maintain stateful aggregations.
- **Schema Enforcement:** Strict StructType definitions are applied to ensure data quality before persistence.

### 3. Storage Layer (Data Lake)
- **Sink:** Amazon S3.
- **Format:** Data is persisted in **Parquet** (Columnar format) to optimize storage costs and enhance query performance for downstream analytics.

### 4. Cataloging & Analytics
- **Metadata Management:** AWS Glue Crawlers for automated schema discovery and Data Catalog maintenance.
- **Query Engine:** Amazon Athena (Serverless SQL) providing an ad-hoc query interface over the S3 Data Lake.
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
├── jobs/
│   ├── main.py              # Spark Structured Streaming application
│   └── spark-city.py        # IoT data generation & Kafka producer
├── docker-compose.yml       # Infrastructure orchestration
