from flask import Flask, render_template, request, redirect, url_for, jsonify
import boto3
import pymysql

app = Flask(__name__)

# MySQL database connection details
DB_HOST = 'database-project4.cbiug4o8eoqu.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'admin1234'
DB_NAME = 'database-project4'

# Amazon S3 credentials and configuration
S3_BUCKET = 'projectbuck123'
AWS_REGION = 'N.Virginia'
AWS_ACCESS_KEY_ID = 'AKIAW3MD62E7DNTY34GF'
AWS_SECRET_ACCESS_KEY = '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'

# Connect to MySQL database
def connect_to_db():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Upload file to Amazon S3 bucket
def upload_to_s3(file, filename):
    s3 = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.upload_fileobj(file, S3_BUCKET, filename)

# Retrieve employee data by ID
def get_employee_by_id(emp_id):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM employee WHERE id = %s", (emp_id,))
        employee = cursor.fetchone()
    conn.close()
    return employee

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        name = request.form['name']
        age = request.form['age']
        location = request.form['location']
        photo = request.files['photo']

        # Connect to MySQL database
        conn = connect_to_db()

        # Insert employee data into MySQL database
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO employee (name, age, location) VALUES (%s, %s, %s)", (name, age, location))
            conn.commit()

        # Upload photo to Amazon S3 bucket
        if photo:
            upload_to_s3(photo, photo.filename)

        # Close MySQL connection
        conn.close()

        return 'Employee added successfully!'
    except Exception as e:
        return str(e)

@app.route('/employee/<int:emp_id>')
def get_employee(emp_id):
    employee = get_employee_by_id(emp_id)
    if employee:
        return jsonify(employee)
    else:
        return 'Employee not found'

if __name__ == '__main__':
    app.run(debug=True)
