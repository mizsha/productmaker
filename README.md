# productmaker

## Demo

- https://protected-savannah-03840.herokuapp.com/
- https://protected-savannah-03840.herokuapp.com/swagger/

## Services

### API Powered by

- sanic
- tortoise-orm

### Clock Powered by

- apscheduler

## How to Run

### Run in docker

- git clone https://github.com/mizsha/productmaker
- cd productmaker
- docker-compose build
- docker-compose up
- GOTO http://localhost:5000/swagger/

### Run in heroku local

- RUN PostgreSQL or CocroachDB instance and specify DATABASE_URL environment variable
- DATABASE_URL default is postgres://root@localhost:26257/productmaker
- git clone https://github.com/mizsha/productmaker
- cd productmaker
- heroku local
- GOTO http://localhost:5000/swagger/

## How to Test

### Install and run Robot Test Framework

- cd services/api/app/
- coverage api.py

- cd services/tests/api/
- pip install -r requirements.txt
- robot --variable SERVER:http://localhost:5000/v1/ --outputdir results atest/

### Install and run pytest

- cd services/tests/api-pytest/
- pip install -r requirements.txt
- pytest
