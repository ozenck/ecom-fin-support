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