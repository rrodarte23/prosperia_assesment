# prosperia_assesment
CRUD operations in MongoDB user model using FASTAPI and swagger
# Prerequisites
* Python 3.11
* Docker
* Docker-compose

# How to run?
Inside the root path run:
```bash
docker-compose up --build
```
# Create a new user
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "New Item", "price": 10.0}' http://localhost:8000/items/
```


# Endpoint Descriptions

Just open: http://localhost:8000/docs

# Problems to connect to mongo or connection refused error?
Try this
```bash
docker exec -it prosperia_assesment-app-1 bash
apt-get update
apt-get install inetutils-ping
apt-get install inetutils-telnet
telnet mongodb 27017
```
You will see something like this:
```bash
Trying 172.18.0.2...
Connected to mongodb.
Escape character is '^]'.
```
The host of your mongodb is the ip after trying word
Replace on mongo_db_utils.py file and  run again:
```bash
docker-compose up --build
```