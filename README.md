<p align="center">
    <img alt="Badger Logo" src="https://raw.githubusercontent.com/Clivern/Badger/master/static/assets/images/logo.png" height="80" />
    <h3 align="center">Badger</h3>
    <p align="center">A Status and Incident Communication Tool.</p>
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

In order to run badger for development purposes, we will use `virtualenv`.

```bash
# Install virtualenv
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate

$ git clone https://github.com/Clivern/Badger.git badger
$ cd badger
$ cp .env.example .env

# Install dependencies
$ pip3 install -r requirements.txt

# Update .env file
$ python3 manage.py badger update_env DB_HOST=127.0.0.1
$ python3 manage.py badger update_env DB_PORT=3306
$ python3 manage.py badger update_env DB_DATABASE=badger
$ python3 manage.py badger update_env DB_USERNAME=root
$ python3 manage.py badger update_env DB_PASSWORD=
$ python3 manage.py badger update_app_key
$ python3 manage.py badger update_env DB_CONNECTION=mysql

# Migrate DB
$ python3 manage.py migrate

# Run Application
$ python3 manage.py runserver

# Exit the virtualenv
$ deactivate
```


## Badges

[![Build Status](https://travis-ci.org/Clivern/Badger.svg?branch=master)](https://travis-ci.org/Clivern/Badger)
[![GitHub license](https://img.shields.io/github/license/Clivern/Badger.svg)](https://github.com/Clivern/Badger/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/Version-Under%20Development-red.svg)](https://github.com/Clivern/Badger/releases)


## Changelog

* Version 1.0.0:
```
Initial Release.
```


## Acknowledgements

© 2018, Clivern. Released under [MIT License](https://opensource.org/licenses/mit-license.php).

**Badger** is authored and maintained by [@Clivern](http://github.com/clivern).
