Running App Locally (no docker)

cd hw06
python app.py
App available at: http://localhost:8000


Running App with docker

docker build -t hw06-python-flask-ridgway-alex-ridgw .
docker run -p 8000:8000 -v ${HOME}\.aws:/root/.aws:ro hw06-python-flask-ridgway-alex-acr22003
App available at: http://localhost:8000


Docker Commands

docker build -t hw06-app-repo .
docker tag hw06-app-repo:latest 338893091918.dkr.ecr.us-east-1.amazonaws.com/hw06-app-repo:latest
docker push 338893091918.dkr.ecr.us-east-1.amazonaws.com/hw06-app-repo:latest

hw06/taskdef-hw06.json is a copy of the ECS task definition. 
GHA replaces the image field during deployment.

GHA

Push to branch: feature-hw06
Triggers pipeline: Build Docker image, Push to ECR, Deploy to ECS


ECS Deployment

Cluster: hw06-cluster  
Service: hw06-service  
Port: 8000


DynamoDB

Table name: hw06-urls
Partition key: key