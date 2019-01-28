<p align="center">
    <img alt="Badger Logo" src="https://raw.githubusercontent.com/Clivern/Badger/master/static/assets/images/logo.png" height="80" />
    <h3 align="center">Badger</h3>
    <p align="center">A Status and Incident Communication Tool.</p>
</p>


## Documentation

### Config & Run The Application

Setting up badger on your development environment:

```bash
# Install virtualenv
$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate

$ git clone https://github.com/Clivern/Badger.git badger
$ cd badger
$ cp .env.example .env

# Install dependencies
$ pip install -r requirements.txt

# Update .env file
$ python manage.py badger update_env DB_HOST=127.0.0.1
$ python manage.py badger update_env DB_PORT=3306
$ python manage.py badger update_env DB_DATABASE=badger
$ python manage.py badger update_env DB_USERNAME=root
$ python manage.py badger update_env DB_PASSWORD=
$ python manage.py badger update_app_key
$ python manage.py badger update_env DB_CONNECTION=mysql

# Migrate DB
$ python manage.py migrate

# Run Application
$ python manage.py runserver

# Exit the virtualenv
$ deactivate
```


## Badges

[![Build Status](https://travis-ci.org/Clivern/Badger.svg?branch=master)](https://travis-ci.org/Clivern/Badger)
[![GitHub license](https://img.shields.io/github/license/Clivern/Badger.svg)](https://github.com/Clivern/Badger/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/Version-Under%20Development-red.svg)](https://github.com/Clivern/Badger/releases)


## Contributing

For guidance on setting up a development environment and how to make a contribution to Badger, see the [contributing guidelines](CONTRIBUTING.md)


## Acknowledgements

© 2018, Clivern. Released under [MIT License](https://opensource.org/licenses/mit-license.php).

**Badger** is authored and maintained by [@Clivern](http://github.com/clivern).
