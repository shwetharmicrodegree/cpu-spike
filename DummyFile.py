import boto3
import time
import random

def put_dummy_logs(log_group, log_stream, num_messages=10):
    client = boto3.client("logs")

    # Ensure the log group exists
    try:
        client.create_log_group(logGroupName=log_group)
        print(f"Created log group: {log_group}")
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    # Ensure the log stream exists
    try:
        client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
        print(f"Created log stream: {log_stream}")
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    sequence_token = None

    for i in range(num_messages):
        message = f"Dummy log message {i+1} - Status: {random.choice(['OK', 'WARN', 'ERROR'])}"
        timestamp = int(time.time() * 1000)

        log_event = {
            'logGroupName': log_group,
            'logStreamName': log_stream,
            'logEvents': [
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ]
        }

        if sequence_token:
            log_event['sequenceToken'] = sequence_token

        response = client.put_log_events(**log_event)
        sequence_token = response['nextSequenceToken']

        print(f"Sent log: {message}")
        time.sleep(1)  # small delay between logs

if __name__ == "__main__":
    log_group_name = "DummyLogGroup"
    log_stream_name = "TestStream"

    put_dummy_logs(log_group_name, log_stream_name, num_messages=15)
