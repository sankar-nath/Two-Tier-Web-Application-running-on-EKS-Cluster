from flask import Flask, render_template, request, render_template, request
import boto3
from pymysql import connections
import os
import random
import requests
import argparse


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
DBPORT = int(os.environ.get("DBPORT")) or 3306
groupclo835 = os.environ.get("GROUPNAME") or "defaultGroup"
bucket_name= "group5jaas2"
#image_url="https://group5jaas2.s3.amazonaws.com/new.jpg"


fileName= "jello.jpg"
objectName= os.environ.get("objectName") or "jello.jpg"
directory = "static"


def download_image(image_url, image_path):
    response = requests.get(image_url)
    #imagePath = os.path.join(image_path, "jello.jpg")
    if response.status_code == 200:
        with open(os.path.join('static', 'jello.jpg'), 'wb') as f:
            f.write(response.content)
            return image_path
    else:
        return image_path

#Download the Image from s3 bucket
def download_file(fileName, bucket_name):
    
    
    if os.path.exists(directory) and os.path.isdir(directory):
        print("Directory exists")
    else:
        os.makedirs(directory)
    imagePath = os.path.join(directory, fileName)
    print(imagePath)
    print(bucket_name)
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource("s3",
            aws_access_key_id='ASIAVHRCFEULOAIJMXP7',
            aws_secret_access_key='2chPlsE6ofETP5pW8EzWC5mGc6YCeglFXWTdXac/',
            aws_session_token='FwoGZXIvYXdzEGAaDOTvwznig53agvpzhyLGAWE3FBC4qk8O/q4HaFcwkxuxBpfr5C6g+6XV9f4Uq+L2gAWcoI+8jDBoWncEGcNEfPylllw5Idpk+SC62ycKkIEMlGUyKCO0oVPqnt0Fwe0SxT03BxoLhXP0H7bzdS6f0XdHn5EJhA9UVkDOVkHWHMLJBxpk9/3cLELlR9Px9fVVbIRkA2tWvR37/RrnYT9XcLcAu4hfLVCQqVMviXQNADj8XakgsbAdH25Sy1K+Hn8ingFrxyb+z/bShIQcLeuTUD/GJ8X+0yifsfWhBjIt0wFA3OgkEyiyeOPeX7uVjtd6unM3wDLuUwO4Oq/AiyOsDq4M+ZPBFBBkd5AM'
            )
    print(bucket_name)
    s3.Bucket(bucket_name).download_file(objectName,imagePath)
    return imagePath



# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

# Define the supported color codes
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}


# Create a string of supported colors
SUPPORTED_COLORS = ",".join(color_codes.keys())

# Generate a random color
COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', color=color_codes[COLOR], group=groupclo835)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', color=color_codes[COLOR], group=groupclo835)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, color=color_codes[COLOR], group=groupclo835)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", color=color_codes[COLOR], group=groupclo835)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], color=color_codes[COLOR], group=groupclo835)

if __name__ == '__main__':
    #image=download_image('https://group5jaas.s3.amazonaws.com/jello.jpg', '/static/jello.jpg')
    image=download_file(fileName, bucket_name)
    print(image)
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precendence.")
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    app.run(host='0.0.0.0',port=81,debug=True)