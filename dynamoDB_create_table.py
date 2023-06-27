import boto3
import key_config as keys


dynamodb_client = boto3.client(
   'dynamodb',
    aws_access_key_id = 'AKIA5CFUGMGXXVCEYSXL',
    aws_secret_access_key = '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',
    region_name         = 'us-east-1'
    )
dynamodb_resource = boto3.resource(
    'dynamodb',
    aws_access_key_id = 'AKIA5CFUGMGXXVCEYSXL',
    aws_secret_access_key = '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',
    region_name         = 'us-east-1'
    )


def establish_table():
   table = dynamodb_resource.create_table(
       TableName = 'etu_students', # Name of the table
       KeySchema = [
           {
               'AttributeName': 'email',
               'KeyType'      : 'HASH' #RANGE = sort key, HASH = partition key
           }

       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'email', # Name of the attribute
               'AttributeType': 'S'   # N = Number (B= Binary, S = String)
           }

       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 10,
           'WriteCapacityUnits': 10
       }
   )
   return table