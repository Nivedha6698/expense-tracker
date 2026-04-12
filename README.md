# Expense Tracker – DevOps Enabled Flask Application

##  Project Description

The **Expense Tracker** is a web-based application that allows users to manage and track their daily expenses efficiently. Users can add, view, filter, and export their expenses.

This project is enhanced with **DevOps practices**, including containerization, CI/CD automation, monitoring, and backup strategies.

---

## Tech Stack

### 🔹 Backend

* Python (Flask)
* SQLAlchemy (ORM)
* MySQL (AWS RDS)

### 🔹 Frontend

* HTML, CSS, Bootstrap

### 🔹 DevOps & Cloud

* Docker
* Jenkins (CI/CD)
* AWS EC2 (Deployment)
* AWS S3 (optional for backups)
* Prometheus (Monitoring)
* Grafana (Visualization)
* Node Exporter & cAdvisor

---

## Setup Instructions (Local Setup)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
DB_HOST=<your-db-host>
DB_USER=<username>
DB_PASSWORD=<password>
DB_NAME=<database-name>
JWT_SECRET_KEY=<your-secret>
```

---

### 5️⃣ Run Application

```bash
python app.py
```

👉 App will run on:

```
http://localhost:5000
```

---

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t expense-tracker .
```

### Run Container

```bash
docker run -d -p 5000:5000 --name expense-app expense-tracker
```

---

## CI/CD Pipeline (Jenkins)

### Flow Overview

1. Developer pushes code to GitHub
2. GitHub Webhook triggers Jenkins pipeline
3. Jenkins performs:

   * Install dependencies
   * Build Docker image
   * Push image to Docker Hub
   * Deploy container to EC2 via SSH
4. Application gets updated automatically

---

## Deployment Architecture

```text
GitHub → Jenkins → Docker → EC2
                          ↓
                    Expense Tracker App
```

---
## Monitoring Setup

* Prometheus collects metrics from:

  * Node Exporter (system metrics)
  * cAdvisor (container metrics)
* Grafana visualizes:

  * CPU usage
  * Memory usage
  * Container stats

---

## Backup & Automation

* Backup scripts created using shell scripting
* Scheduled via cron jobs
* Monthly backups stored locally (/backup directory)
* Old backups cleaned automatically

---

## Features

* Add & manage expenses
* Export expenses as CSV
* Secure authentication (JWT)
* Dockerized application
* CI/CD automation
* Monitoring & logging
* Backup & cleanup automation

---

## Future Enhancements

* Store backups in AWS S3
* Add alerting (Prometheus Alertmanager)
* Implement role-based access
* Add frontend framework (React)

---

##  Author

Nivedha Ramu

---

## License

This project is for educational and demonstration purposes.

