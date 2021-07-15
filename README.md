# Web Service Coding Test

<br>

## Setup

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br>

## Run the unit tests

```
$ cd src
$ pytest
```

<br>

## Spin up the server

### 1. Create the database file

```
$ cd src
$ DATABASE_URL="sqlite:///path/to/db.sqlite" alembic upgrade head
```


### 2. Run the server

```
$ cd src
$ DATABASE_URL="sqlite:///path/to/db.sqlite" uvicorn main:app
```

### 3. Make requests

In your browser, go to
 - [Docs](http://127.0.0.1:8000/docs)
 - [Redoc](http://127.0.0.1:8000/docs)
 - [OpenAPI file](http://127.0.0.1:8000/openapi.json)
