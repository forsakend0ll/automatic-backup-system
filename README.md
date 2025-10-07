# Automatic Backup System – AWS Project

## Overview
The **Automatic Backup System** is a serverless AWS project that automatically backs up data daily across multiple S3 buckets.  
It demonstrates **automation, cost optimization, and event-driven architecture** using AWS Lambda, EventBridge (CloudWatch Scheduler), S3 Lifecycle Rules, and optional SNS notifications.

---

## Problem Statement
Managing backups manually is time-consuming and prone to human error.  
This project automates backup creation, ensures **versioning**, and applies **lifecycle rules** to optimize storage costs.

---

## Architecture

![Architecture Diagram](images/architecture-diagram.gif)


---

## Workflow Summary
1. **EventBridge (CloudWatch Scheduler)** triggers the **AutoBackupUploader Lambda** every 24 hours (`rate(1 day)`).
2. **Lambda** generates a timestamped backup file (simulated `.txt`) and uploads it to three S3 buckets:
   - `documents-backup-cloudwithpaula`
   - `photos-backup-cloudwithpaula`
   - `database-backup-cloudwithpaula`
3. Each bucket has:
   - **Versioning enabled** to preserve file history  
   - **Lifecycle rules** to move older files into **Glacier Flexible Retrieval** or **Deep Archive** for cost optimization  
4. **SNS (optional)** sends an alert when backups succeed or fail.  
5. This process repeats automatically every day.

---

## Design Decisions
- **Daily Backup (1-day schedule):**  
  - Chosen to balance automation and cost-efficiency  
  - Ensures data is backed up regularly without creating excessive S3 storage or Lambda executions  
  - Fits naturally with S3 lifecycle transitions (Glacier/Deep Archive)  
  - Simulates realistic business backup frequency for a portfolio/demo  

- **Lifecycle rules:** Move old files to Glacier or Deep Archive to reduce costs while retaining historical data.  

- **SNS notifications:** Optional, to demonstrate event-driven alerting in a complete AWS architecture.

---

## Setup Instructions

### Prerequisites
- AWS account
- IAM user with permissions: Lambda, S3, EventBridge, SNS
- Python 3.12+ (for Lambda)

### Steps
1. Create three S3 buckets for `documents`, `photos`, and `database` backups.  
2. Enable **versioning** and configure **lifecycle rules**:
   - Documents: Glacier after 30 days, Deep Archive after 180 days  
   - Photos: Glacier after 30 days, Deep Archive after 180 days  
   - Database: Glacier after 7 days  
3. Create a Lambda function (`AutoBackupUploader`) in AWS:
   - Runtime: Python 3.12  
   - Attach IAM role with S3 write access (or AmazonS3FullAccess for demo)  
   - Add code to upload backup files to all three buckets  
4. Create an EventBridge rule:
   - Rule type: **Rate-based schedule**  
   - Rate: `1 day`  
   - Target: **AutoBackupUploader Lambda**  
5. (Optional) Configure SNS notifications in Lambda to send success/failure alerts.  
6. Test manually using Lambda → “Test” to confirm backups appear in all three buckets.  
7. Once confirmed, backups will run automatically daily.

---


