# ecom-fin-support

## Project setup

#### On local
```
<Create virtualenv>
$ mkdir venv && cd venv
$ virtualenv .
$ cd ..
$ source venv/Scripts/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py makemigrations account
$ python manage.py migrate
$ python manage.py runserver
```

#### Unit Tests & Coverage
```
coverage run --source=account manage.py test
coverage report -m
coverage html
```

#### Docker
```
docker-compose up -d
```