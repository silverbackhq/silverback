<p align="center">
    <img alt="Silverback Logo" src="https://raw.githubusercontent.com/Clivern/Silverback/master/static/assets/images/logo.png" height="80" />
    <h3 align="center">Silverback</h3>
    <p align="center">A Status and Incident Communication Tool.</p>
    <p align="center">
        <img src="https://travis-ci.org/Clivern/Silverback.svg?branch=master">
        <img src="https://img.shields.io/github/license/Clivern/Silverback.svg">
        <img src="https://img.shields.io/badge/Version-Under%20Development-red.svg">
    </p>
</p>

## Overview

- Auto Installer.
- Asynchronous workers for notifications with ability to run any number to scale.


## Requirements

- Python 3 or later
- A supported database: MySQL, PostgreSQL.
- Redis Server.
- RabbitMQ Server.


## Installation

### Production

### Docker

### Development

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


## Contributing

For guidance on setting up a development environment and how to make a contribution to Silverback, see the [contributing guidelines](CONTRIBUTING.md)


## Acknowledgements

© 2019, Silverback. Released under [MIT License](https://opensource.org/licenses/mit-license.php).

**Silverback** is authored and maintained by [@silverbackhq](https://github.com/silverbackhq).
