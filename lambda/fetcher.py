import boto3


def get_api_token() -> str:
    client = boto3.client("ssm")
    response = client.get_parameter(
        Name="qld_fuel_token", WithDecryption=True)

    return response["Parameter"]["Value"]


def lambda_handler(event, context):
    api_token = get_api_token()
    return {
        'statusCode': 200,
        'body': 'Hello, World!',
        'tokie': str(api_token[-1])
    }
