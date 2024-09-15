# Real-time Election Voting System

This project demonstrates the design and implementation of a **Real-time Election Voting System** using a distributed environment powered by Python, Kafka, Spark Streaming, Postgres, and Streamlit. The system enables real-time voting data processing and visualization, ensuring efficiency, transparency, and accuracy in vote tallying.

## Table of Contents
- [Introduction](#introduction)
- [System Design](#system-design)
- [Technical Requirements](#technical-requirements)
- [Installation](#installation)
- [Running the System](#running-the-system)
- [System Components](#system-components)
- [Additional Configuration](#additional-configuration)
- [License](#license)

## Introduction

The Real-time Election Voting System tackles the challenges faced by traditional voting methods, such as human counting errors and delays in transmitting results. By utilizing real-time streaming data technologies like Kafka and Spark Streaming, this system speeds up the voting process and provides accurate and timely results.

## System Design

### Key Components:
- **Kafka**: A centralized data streaming platform that handles real-time data ingestion.
- **Zookeeper**: Manages and coordinates Kafka brokers, ensuring fault tolerance.
- **Spark Streaming**: Processes the real-time data and performs aggregation for advanced analytics.
- **Postgres**: Serves as the permanent storage solution for essential data (voters, candidates, votes).
- **Streamlit**: Creates an interactive dashboard for real-time monitoring and visualization of voting trends.

The system is containerized using Docker and managed via Docker Compose, making it easier to deploy in a distributed environment.

## Technical Requirements

To run the project, ensure that you have the following software installed:
- **Python 3.9 or higher**
- **Docker** and **Docker Compose**

### Prerequisites:
- Docker Compose installed on your machine.
- Docker installed on your machine.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/election-voting-system.git
   cd election-voting-system
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up -d
   ```
   This command starts the Zookeeper, Kafka, and Postgres containers in detached mode. Kafka will be available at `localhost:9092`, and Postgres at `localhost:5432`.

## Running the System

### Steps to Run:

1. **Install the necessary Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create necessary tables in Postgres and generate voter information in Kafka:**
   ```bash
   python main.py
   ```

3. **Generate and consume voting data:**
   - First, consume voter information from Kafka, generate voting data, and produce the results to a Kafka topic:
   ```bash
   python voting.py
   ```

4. **Process and enrich the data with Spark Streaming:**
   - Consume voting data from Kafka, enrich it with data from Postgres, and produce the results to specific Kafka topics:
   ```bash
   python spark-streaming.py
   ```

5. **Run the Streamlit dashboard:**
   - Launch the interactive real-time dashboard:
   ```bash
   streamlit run streamlit-app.py
   ```

This setup ensures efficient deployment and management of a distributed real-time environment for election voting.

## System Components

The **Real-time Election Voting System** integrates several components to provide a modern solution for election operations. The system leverages **Kafka** and **Spark Streaming** for scalable, real-time streaming data management and **Postgres** for data integrity. **Docker Compose** is used to coordinate the setup of services, ensuring seamless operation.

Key features include:
- **Kafka** and **Spark Streaming** for real-time data processing.
- **Postgres** for durable storage of voter, vote, and result data.
- **Streamlit** for user-friendly dashboards, enabling election officials to visualize and monitor real-time voting trends.
- **Zookeeper** for managing Kafka clusters, enhancing scalability and fault tolerance.
- **Docker Compose** for simplified deployment in a distributed environment.

### Result and Analysis

This system is designed to maintain responsiveness during high-traffic periods, providing real-time insights into election data. The interactive dashboard allows election officials to track voting trends, demographics, and results dynamically. Additionally, Kafka’s security features ensure the confidentiality and integrity of election data, preventing fraud and unauthorized access.

The system provides the following advantages:
- **Efficiency**: Real-time processing speeds up vote tallying and result reporting.
- **Scalability**: Kafka and Spark Streaming allow the system to handle large-scale elections.
- **Transparency**: The system improves visibility into election processes with real-time monitoring and dashboards.
- **Security**: Kafka's built-in features ensure the protection of election data.

In addition, you can easily monitor the health and performance of your distributed components. For example, a **MongoDB Cluster Status Dashboard** provides insights into the health and performance of the MongoDB cluster, tracking metrics like CPU usage, memory utilization, and disk I/O.

### Python Script Workflow

- **main.py**: Interacts with Kafka to load raw voter data into Kafka topics.
- **voting.py**: Consumes voter information from Kafka, generates voting data, and sends it back to Kafka topics.
- **spark-streaming.py**: Handles real-time processing of voting data from Kafka and enriches the data by merging it with voter details from Postgres.
- **streamlit-app.py**: Visualizes real-time voting trends and results using the data processed by Spark Streaming and stored in Postgres.

The system's architecture is built for **fault tolerance** and **scalability**. Kafka and Spark Streaming are inherently distributed, ensuring that the system remains responsive and scalable as the load increases.
