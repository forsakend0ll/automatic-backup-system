# Automatic Backup System – AWS Lambda & S3

This project demonstrates how to build an **automated backup system** using AWS services under the **Free Tier**.  
It includes **daily backups**, **versioning**, **lifecycle rules for cost optimization**, and **notifications** via SNS.

---

## Architecture Overview

![Architecture Diagram](architecture-diagram.gif)

---

## Deployed Backup System Preview
The system automatically uploads timestamped backup files to **three S3 buckets**:  

- `documents-backup-cloudwithpaula`  
- `photos-backup-cloudwithpaula`  
- `database-backup-cloudwithpaula`  

Example:  
A backup file `backup_2025-10-08_14-45-08.txt` uploaded automatically by Lambda.

---

## AWS Services Used

- **AWS Lambda** – Runs Python script (`AutoBackupUploader`) to create and upload backup files  
- **Amazon S3** – Stores backup files with versioning and lifecycle rules for Glacier/Deep Archive  
- **Amazon EventBridge (CloudWatch Scheduler)** – Triggers the Lambda function on a daily schedule  
- **Amazon SNS** – Sends notifications when backups succeed or fail  
- **CloudWatch Logs** – Monitors Lambda execution and logs any errors  

---

## Example Backup Behavior

- Daily scheduled backup triggered at **00:00 UTC** (or configured time)  
- Each bucket has **versioning** enabled to preserve file history  
- Lifecycle rules automatically move files to **Glacier Flexible Retrieval** or **Deep Archive** after configured days:  
  - Documents: Glacier after 30 days, Deep Archive after 180 days  
  - Photos: Glacier after 30 days, Deep Archive after 180 days  
  - Database: Glacier after 7 days  
- For **demonstration purposes**, these transitions can be temporarily set to 1 day so the behavior can be observed immediately in the project demo.

---

## Step-by-Step Setup Summary

### 1️⃣ Create S3 Buckets
- Create three buckets for `documents`, `photos`, and `database`  
- Enable **versioning**  
- Configure **lifecycle rules** to move older backups to Glacier/Deep Archive  

### 2️⃣ Create Lambda Function
- Runtime: **Python 3.12**  
- Attach IAM role with **S3 write access**  
- Add the `AutoBackupUploader` Python script to upload backup files to all three buckets  

### 3️⃣ Create EventBridge Rule
- Schedule type: **Rate-based schedule**  
- Frequency: **1 day**  
- Target: **AutoBackupUploader Lambda**  
- Enables automated daily backups  

### 4️⃣ (Optional) SNS Notifications
- Configure Lambda to send success/failure alerts via SNS  

### 5️⃣ Test & Verify
- Run Lambda manually via **“Test”** to confirm files are uploaded to all three buckets  
- Monitor execution and logs in **CloudWatch**

---

## Design Decisions

- **Daily backup schedule:** Balances automation with cost-efficiency and ensures consistent backup without excessive S3/Lambda usage.  
- **Lifecycle rules:** Normally, S3 transitions to **Glacier** or **Deep Archive** after longer periods (30–180 days). For **demonstration purposes**, these transitions are configured to occur after 1 day, allowing the automated backup and cost-optimization behavior to be visible immediately.  
- **SNS notifications:** to demonstrate event-driven alerting.  
- **Versioning enabled:** Ensures historical backups are preserved and not accidentally overwritten.  

---

## Repository Structure

```plaintext
automatic-backup-system/
│
├── README.md                      ← this documentation  
├── architecture-diagram.gif       ← architecture diagram 
├── lambda_function.py             ← Lambda Python script  
└── sample-backups/                ← example backup files 
```
---
### Author
**Paula Kim**  
Cloud & AI Enthusiast  
