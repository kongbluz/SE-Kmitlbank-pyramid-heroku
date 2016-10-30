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
```
$ cd <this directory>
$ heroku create --stack cedar

$ git push heroku master

$ heroku addons:create heroku-postgresql:hobby-dev --as DATABASE_URL

$ heroku pg:promote <HEROKU_POSTGRESQL_NAME>

$ heroku run 'python -m bin.scripts.herokudb'
```
