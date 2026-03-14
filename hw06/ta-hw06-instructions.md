Docker Instructions

cd HW06
docker build -t hw06-python-flask-ridgway-alex-acr22003 .
docker run -p 8000:8000 -v ${HOME}\.aws:/root/.aws:ro hw06-python-flask-ridgway-alex-acr22003
docker ps
docker logs <CONTAINER-ID>
docker stop <CONTAINER-ID>

HW06/taskdef-hw06.json is a copy of the ECS task definition.
GHA replaces the image field during deployment.