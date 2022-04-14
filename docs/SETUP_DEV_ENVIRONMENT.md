# Setup Development Environement

```bash
$ cp .env.example .env
# Edit .env
$ vim .env

$ docker-compose build
$ docker-compose up -d
$ docker attach life_recorder_web_1
$ docker-compose exec web bash
# python manage.py createsuperuser
>> ** Input information of your superuser! **
```

Then, you can access

- Django Admin  
`localhost:8000/admin`
- App Top  
`localhost:8000`
