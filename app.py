from flask import Flask, render_template, request
import key_config as keys
import boto3 
import dynamoDB_create_table as dynamodb_et
import form_data_updation as dynamodb_h
from decimal import Decimal


app = Flask(__name__)

dynamodb = boto3.resource(
    'dynamodb',
     aws_access_key_id = 'AKIA5CFUGMGXXVCEYSXL',
     aws_secret_access_key = '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',
     region_name         = 'us-east-1'
    )

from boto3.dynamodb.conditions import Key, Attr

#############################Table Creation#############################
@app.route('/')
def index():
        # dynamodb_et.establish_table()
        # return 'Table Created'
        return render_template('registration_form.html')
        
#############################Login function#############################

@app.route('/login')
def login():    
    return render_template('login.html')
    
#############################Student data storing in dynamodb Table#############################
    
@app.route('/signup', methods=['post'])
def signup():
    #if request.method == 'POST':
        full_name = request.form['full_name']
        reg_no= request.form['reg_no']
        email = request.form['email']
        deg_programme = request.form['deg_programme']
        contact_no = request.form['contact_no']
        current_gpa = request.form['current_gpa']
        intro = request.form['intro']
        skills = request.form['skills']
        password = request.form['password']
        
        
        table = dynamodb.Table('etu_students')
        
        table.put_item(
                Item={
        'full_name': full_name,
        'reg_no': int(reg_no),
        'email': email,
        'deg_programme':deg_programme,
        'contact_no':int(contact_no),
        'current_gpa':Decimal(current_gpa),
        'intro':intro,
        'skills':skills,
        'password':password
            }
        )
      
        msg = "Registration Complete. Please Login to your account !"
        return render_template('login.html',msg = msg)
        
        
#############################Checking user email and login#############################

@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table('etu_students')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        full_name = items[0]['full_name']
        reg_no = items[0]['reg_no']
        email = items[0]['email']
        
        current_gpa = items[0]['current_gpa']
        contact_no = items[0]['contact_no']
        intro = items[0]['intro']
        skills = items[0]['skills']
        deg_programme =items[0]['deg_programme']
        
        print(items[0]['password'])
        if password == items[0]['password']:
            
            return render_template("home.html",full_name = full_name,reg_no=reg_no,email=email,current_gpa=current_gpa,
            contact_no=contact_no,intro=intro,skills=skills,deg_programme=deg_programme)
    return render_template("login.html")
    
############################# User logout #############################

@app.route('/logout')
def system_logout():
    return render_template("login.html")
    

#############################Search for a specific student profile#############################
@app.route('/profile', methods=['POST'])
def query_by_index_key():

        email = request.form["email"]

        dynamodb = boto3.resource('dynamodb')
        st_tble = dynamodb.Table('etu_students')

        dynamodb = boto3.client("dynamodb")

        response = st_tble.get_item(
        Key = {
            'email': email
        },
        AttributesToGet = [
            'email','full_name','reg_no','deg_programme','contact_no','current_gpa','intro','skills'
        ]
        )
        
        items = response['Item']
        email = items['email']
        full_name = items['full_name']
        reg_no = items['reg_no']
        deg_programme = items['deg_programme']
        contact_no = items['contact_no']
        current_gpa = items['current_gpa']
        intro = items['intro']
        skills = items['skills']
        
        return render_template("profile-view.html",email=email,full_name=full_name,reg_no=reg_no,deg_programme=deg_programme,contact_no=contact_no,current_gpa=current_gpa,intro=intro,skills=skills)
        
        
        

############################# Update Student data #############################

    
@app.route('/update/<string:email>', methods=['PUT'])
def update_students_table(email):
    
    data = request.get_json()
    
    response = dynamodb_h.update_student_profile(email, data)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }       
    

 #############################  Query#############################
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')