## Requirements

- Python 3 or later
- A supported database: MySQL, PostgreSQL.
- Redis Server.
- RabbitMQ Server.


## Development

In order to run silverback for development purposes, we will use `virtualenv`.

```bash
# Install virtualenv
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate

$ git clone https://github.com/Clivern/Silverback.git silverback
$ cd silverback
$ cp .env.example .env

# Install dependencies
$ pip3 install -r requirements.txt

# Update .env file
$ python3 manage.py silverback update_env DB_HOST=127.0.0.1
$ python3 manage.py silverback update_env DB_PORT=3306
$ python3 manage.py silverback update_env DB_DATABASE=silverback
$ python3 manage.py silverback update_env DB_USERNAME=root
$ python3 manage.py silverback update_env DB_PASSWORD=
$ python3 manage.py silverback update_app_key
$ python3 manage.py silverback update_env DB_CONNECTION=mysql

# Migrate DB
$ python3 manage.py migrate

# Run Application
$ python3 manage.py runserver

# Exit the virtualenv
$ deactivate
```


## Production


## Run with Docker


```

```