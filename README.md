# Real-Time-Anomaly-Detection


This project demonstrates a fully containerized, real‑time streaming analytics pipeline that mimics a production‑grade monitoring system. We simulate IoT sensor data, send it through Apache Kafka, process it continuously with PySpark Structured Streaming, and detect statistical outliers on the fly. Whenever a sensor reading exceeds its rolling mean by more than three standard deviations, the system automatically pushes an alert into your chosen Slack channel.

Behind the scenes, Docker Compose orchestrates three services—Zookeeper, Kafka, and Spark—so you can spin up the entire stack with a single command. A lightweight Python producer script generates synthetic readings, while the Spark job computes sliding‐window aggregates and invokes a simple HTTP POST to your Slack Incoming Webhook URL for each anomaly detected. This end‑to‑end flow highlights core data‑engineering patterns: message queuing, stream processing, anomaly detection logic, and alerting integration.

You’ll get hands‑on experience with:
1. Kafka & Zookeeper for durable, high‑throughput messaging
2. PySpark Structured Streaming for fault‑tolerant, windowed computation
3. Docker & Docker Compose for local infrastructure orchestration
4. Slack Webhooks for real‑time notifications

By the end, you’ll have a runnable system that you can tweak—adjust window sizes, threshold multipliers, or the data distribution—to explore different streaming analytics scenarios.



