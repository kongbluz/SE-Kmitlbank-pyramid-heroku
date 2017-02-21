# KMIT-BANK

## how to run
- Setting up
```
$ cd <this directory>

$ python setup.py develop
```
- Create Database
```
$ initialize_bin_db development.ini
```
- Serve on localhost
```
$ pserve development.ini
```
- and let fun

## how to run on heroku

- Create heroku App
```
$ cd <this directory>

$ heroku create --stack cedar

$ git push heroku master
```
- Create Postgesql
```
$ heroku addons:create heroku-postgresql:hobby-dev
```
- Establish primary DB
```
$ heroku pg:promote <HEROKU_POSTGRESQL_NAME>
```
- Config variable in heroku
```
$ heroku config:add DATABASE_URL = <HEROKU_POSTGRESQL_URL>
```
- Create Table
```
$ heroku run 'python -m bin.scripts.herokudb'
```
