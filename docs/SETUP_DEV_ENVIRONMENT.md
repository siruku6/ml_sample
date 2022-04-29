# Setup Development Environement

## Filling out `.env`

```bash
$ cp .env.example .env
# Edit .env
$ vim .env
```

    |No|Name       |Value Example|Note                                   |
    |:-|:----------|:------------|:--------------------------------------|
    |1 |DEBUG      |True         |True => Display error detail on browser|
    |2 |SECRET_KEY |xxxxxx...    |It is for Django                       |
    |3 |DB_USER    |user         |It is username of your postgresql      |
    |4 |DB_PASSWORD|password     |It is password of your postgresql      |
    |5 |AWS_ACCESS_KEY_ID    |XXXXXX...|access key id for AWS            |
    |6 |AWS_SECRET_ACCESS_KEY|xxxxxx...|secret access key for AWS        |

    `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are used for downloading model file.

## Building container & Creating user for Django

```bash
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
