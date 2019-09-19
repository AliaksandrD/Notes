## INSTALL
To install project from this branch do following
```bash
$ git clone https://github.com/AliaksandrD/Notes.git
$ cd Notes/
$ git fetch
$ git checkout fix_mistakes
```

For instalation need have docker-compose installed

```bash
$ docker-compose build
```

#### For app runing need to proceed migrations

```bash
$ docker-compose run web python Source/manage.py migrate
$ docker-compose run web python Source/manage.py makemigrations categories
```

rollup the new migrations to db
```bash
$ docker-compose run web python Source/manage.py migrate
```


##RUN Project

```bash
$ docker-compose up
```

After can open link in your web browser at http://0.0.0.0:8000