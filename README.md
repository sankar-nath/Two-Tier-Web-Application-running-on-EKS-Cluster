Welcome to the final project for CLO835, a course we took at Seneca College. In this project, we will be deploying a Two Tier Web application on a Amazon EKS cluster.
The web application takes in employee details and stores it in a database. 
Both the app and the database have been containerized and will be running as a part of a deployment on a Amazon EKS cluster.
Our application will pull an image hosted on a private s3 server and serve it as the background image of the application. 

#Instructions
1.	Create ECR repositories and the security group using either the terraformCode folder or from the AWS console
2.	Create a private s3 bucket in the AWS console and add some images in there
3.	It is recommended to run the app locally first, then as docker containers and then on the EKS cluster
4.	Use the docker build command to build the database application from within the database folder. This db container needs to be running in the background for the app to work.
5.	To run the app locally, update app.py with your aws credentials, install the requirements and use “python app.py” to run the flask application. Use the public IP:Port of the cloud9 instance to access the web app. Here we use Port=81. The db container needs to be running in the background for the app to work.
6.	Use the docker build command to build the webapp application from within the webApp folder. Ensure environment variables are passed along for the app to work. Use the public IP:Port of the cloud9 instance to access the web app.
7.	From the repository, run the ecr.yml file to create docker images which will get pushed to the ECR repositories
8.	Set up the EKS cluster using the files in the EKS cluster folder. You may need to chmod the files or update the aws credentials
9.	Use kubectl apply on the yaml files to set up the pods, the services and the deployment. 
10.	The application can be accessed from the public IP of the EC2 instance once the loadBalancer has been exposed. You may need to modify the security group to achieve this.Use the public IP:Port of the ec2 instance to access the web app or use port-forwarding

# When running locally, install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip install -r requirements.txt
pip install boto3
pip install requests
sudo python app.py

# Building and running 2 tier web application locally
### Building mysql docker image 
```docker build -t my_db -f Dockerfile_mysql . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

### Running mysql
```docker run -d -e MYSQL_ROOT_PASSWORD=pw  my_db```


### Get the IP of the database and export it as DBHOST variable
```docker inspect <container_id>```


### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=127.0.0.1
export DBPORT=3307
```
### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=172.17.0.2
export DBPORT=3306
```
```
export DBUSER=root
export DATABASE=employees
export DBPWD=pw
export APP_COLOR=blue
export GROUPNAME='group5jaas'
export objectName='jello.jpg'
```
### Run the application, make sure it is visible in the browser
``` docker run -p 81:81  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD -e GROUPNAME=$GROUPNAME -e objectName=$objectName  app ```
