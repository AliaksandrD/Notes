## INSTALL

```bash
$ pipenv install --dev
```

#### true way to create new migrations

```bash
$ ./manage.py makemigrations login
$ ./manage.py makemigrations categories
```

rollup the new migrations to db
```bash
$ ./manage.py migrate
```


##RUN Project

```bash
$ ./manage.py runserver
```

After can open link in your web browser 