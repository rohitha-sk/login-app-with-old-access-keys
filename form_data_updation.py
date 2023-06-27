from flask import Flask, render_template, request
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



def update_student_profile(email, data:dict):
    dynamodb = boto3.resource('dynamodb')
    st_tble = dynamodb.Table('etu_students')
    
    response = st_tble.update_item(
        #
       Key = {
          'email': email
         
        },
        AttributeUpdates={
            'full_name': {
              'Value'  : data['full_name'],
              'Action' : 'PUT' 
            },
            
            'reg_no': {
              'Value'  : data['reg_no'],
              'Action' : 'PUT' 
            },
            'current_gpa': {
              'Value'  : data['current_gpa'],
              'Action' : 'PUT' 
            },
            'deg_programme': {
              'Value'  : data['deg_programme'],
              'Action' : 'PUT' 
            },
            'contact_no': {
              'Value'  : data['contact_no'],
              'Action' : 'PUT' 
            },
            'intro': {
              'Value'  : data['intro'],
              'Action' : 'PUT' 
            },
            'skills': {
              'Value'  : data['skills'],
              'Action' : 'PUT' 
            }
            
        },
        
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    
    return response



       
