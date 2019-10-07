## Install for Development Purposes


### Requirements

- Python 3 or later
- A Supported Database: MySQL, PostgreSQL.
- Redis Server (optional for notifications).
- RabbitMQ Server (optional for notifications).


### Steps

In order to run silverback for development purposes, we will use `virtualenv`.

```bash
# Install virtualenv
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate

# Clone silverback
$ git clone https://github.com/Clivern/Silverback.git silverback
$ cd silverback
$ cp .env.example .env

# Install dependencies
$ pip3 install -r requirements.txt

# Update .env file from command line or your favourite IDE
# DB connection configs
$ python3 manage.py silverback update_env DB_HOST=127.0.0.1
$ python3 manage.py silverback update_env DB_PORT=3306
$ python3 manage.py silverback update_env DB_DATABASE=silverback
$ python3 manage.py silverback update_env DB_USERNAME=root
$ python3 manage.py silverback update_env DB_PASSWORD=
$ python3 manage.py silverback update_env DB_CONNECTION=mysql

# Create a random key
$ python3 manage.py silverback update_app_key

# Migrate DB
$ python3 manage.py migrate
# Run Application
$ python3 manage.py runserver

# Exit the virtualenv
$ deactivate
```

### FAQ

- **Error while installing `requirements.txt` `mysql_config: command not found`:**

Edit the `/bin/activate` file from the virtualenv directory and update the following lines:
```bash
_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
PATH="$PATH:/usr/local/mysql/bin/"
export PATH
```
