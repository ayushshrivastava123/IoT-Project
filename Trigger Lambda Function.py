import json
import boto3

print('Loading function')

# Get the dynamodb service resource.
dynamodb = boto3.resource('dynamodb')

#Get the SNS client
client = boto3.client('sns')

#Get the IoT client
iotdataclient = boto3.client('iot-data')

iotclient = boto3.client('iot')

def lambda_handler(event, context):

    table = dynamodb.Table('Reading')

    # Print out some data about the table.
    print(table.creation_date_time)
    
    
    
    #IoT control (optional)
    response = iotclient.describe_endpoint(
        endpointType='iot:Data-ATS'
    )
    print(response)
    
    #IoT Data publish
    message = {}
    message['message'] = "Normal Temperature"
    message['sequence'] = "1"
    messageJson = json.dumps(message)
    iotdataclient.publish(
        topic="normalTemp",
        qos=1,
        payload=messageJson #b'0101'
    )

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
