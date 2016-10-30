# KMITBANK

## how to run
```
$ cd <this directory>

$ python setup.py develop

$ initialize_bin_db development.ini

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
- Create Table
```
$ heroku run 'python -m bin.scripts.herokudb'
```
