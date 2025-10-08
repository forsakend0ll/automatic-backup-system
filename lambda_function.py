import boto3
from datetime import datetime, timezone, timedelta

# ---------- CONFIGURATION ----------
buckets = [
    'documents-backup-cloudwithpaula',
    'photos-backup-cloudwithpaula',
    'database-backup-cloudwithpaula'
]

sns_topic_arn = 'arn:aws:sns:us-east-1:019511185150:BackupNotifications'

# Manila timezone offset (+8 hours)
manila_offset = timedelta(hours=8)

# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Placeholder content for demo backups
placeholder_content = {
    'documents-backup-cloudwithpaula': "This is a sample document backup.",
    'photos-backup-cloudwithpaula': "This is a sample photo backup.",
    'database-backup-cloudwithpaula': "This is a sample database backup."
}

# ---------- LAMBDA HANDLER ----------
def lambda_handler(event, context):
    successful_buckets = []

    for bucket in buckets:
        try:
            # Generate timestamped filename
            now_utc = datetime.now(timezone.utc)
            now_manila = now_utc + manila_offset
            timestamped_file = f"backup_{now_manila.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

            # Upload in-memory content as backup
            s3.put_object(
                Bucket=bucket,
                Key=timestamped_file,
                Body=placeholder_content[bucket]
            )

            print(f"[UTC {now_utc}] / [Manila {now_manila}] Uploaded backup to {bucket} as {timestamped_file}")
            successful_buckets.append(bucket)

        except Exception as e:
            print(f"Error uploading to {bucket}: {e}")

    # ---------- SNS NOTIFICATION ----------
    try:
        message = f"Backup Completed!\nBuckets backed up successfully: {', '.join(successful_buckets)}\nTime: {datetime.now(timezone.utc) + manila_offset}"
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='Automatic Backup Notification'
        )
        print("SNS notification sent successfully.")
    except Exception as e:
        print(f"Failed to send SNS notification: {e}")

    return {
        'statusCode': 200,
        'body': f"Backup finished. Buckets backed up: {successful_buckets}"
    }
