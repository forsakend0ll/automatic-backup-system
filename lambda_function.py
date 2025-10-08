import boto3
import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    buckets = [
        'documents-backup-cloudwithpaula',
        'photos-backup-cloudwithpaula',
        'database-backup-cloudwithpaula'
    ]
    
    for bucket in buckets:
        file_name = f"{bucket}_backup_{timestamp}.txt"
        content = f"Automatic backup for {bucket} created at {timestamp}."
        
        s3.put_object(
            Bucket=bucket,
            Key=file_name,
            Body=content
        )
    
    return {
        'statusCode': 200,
        'body': f"Backups created successfully for {len(buckets)} buckets."
    }
