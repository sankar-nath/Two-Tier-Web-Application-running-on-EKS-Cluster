This repository was cloned from our professor's repo to complete the final project for CLO835
In this Project we deployed a containerized flask application on a K8s EKS cluster running on AWS. The web application takes in employee details and stores it in a database. Both the app and the database are being run as containers running on an EC2 instance.

Instructions
1. Run the docker containers locally from within application/webApp and application/database
2. From the repository, run the ecr.yml file to create docker images which will get pushed to the ECR repositories
3. Copy the manifests folder into the cluster
3. Log in to EC2 instance using ssh, set up the kind cluster using the init_kind.sh and kind.yaml files. You may need to chmod 777 the files.
4. Use kubectl apply on the yaml files to set up the pods, the replicasets and the deployment. 
5. The application can be accessed from the public IP of the EC2 instance once the NodePort has been exposed. You may need to modify the security group to achieve this.
4. Use the public IP:Port of the ec2 instance to access the web app

# Install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip3 install -r requirements.txt
sudo python3 app.py
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
```
### Run the application, make sure it is visible in the browser
```docker run -p 8080:8080  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD  my_app```
