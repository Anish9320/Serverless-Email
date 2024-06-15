import boto3
from botocore.exceptions import ClientError
import json

def hello(event, context):
    receiver = ""
    body_text = ""
    subject = ""
    
    # Taking user input by URL
    if event.get('queryStringParameters'):
        receiver = event['queryStringParameters'].get('receiver', "")
        subject = event['queryStringParameters'].get('subject', "")
        body_text = event['queryStringParameters'].get('body', "")
    #condition, all information is provided or not  
    if receiver and subject and body_text:
        try:
            client = boto3.client('ses', region_name="us-east-1")
            
            sender = "anishdharnidhar07@gmail.com"
            
            email = client.send_email(
                Source=sender,
                Destination={
                    'ToAddresses': [
                        receiver
                    ]
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': body_text
                        }
                    },
                }
            )
            
            data = {
                'message': 'Email Sent!',
                'Message ID': email['MessageId'],
                'HTTPCode': email['ResponseMetadata']['HTTPStatusCode'],
                'DevelopedBy':'Anish Dharnidhar'
            }
            
            response = {
                'statusCode': 200,
                'body': json.dumps(data)
            }
            return response
        
        except ClientError as e:
            data = {
            'message': "Error while sending email: " + e.response['Error']['Message'],
            'HTTP Code': 500,
            'DevelopedBy':'Anish Dharnidhar'
        }
            response = {
                'statusCode': 500,
                'body': json.dumps(data)
            }
            return response
    else:
        data = {
            'message': 'Please provide full information',
            'HTTP Code': 400,
            'DevelopedBy':'Anish Dharnidhar'
        }
        response = {
            'statusCode': 400,
            'body': json.dumps(data)
        }
        return response
