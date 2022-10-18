# REST API интерфейс для проекта YaMDb™

![api-yamdb workflow](https://github.com/ayavrik/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Описание

Учебный проект YaMDb - приложение, где пользователи могут оставить отзыв и оценить
произведение. Проект можно посмотреть по ссылке: https://freeyamdb.ddns.net/

### Технологии

- Python 3.7
- Django 2.2.16
- Django Rest Framework 3.12.4

### Запуск проекта в dev-режиме с помощью Docker compose

Клонируйте репозиторий и перейдите в папку с проектом.

```bash
$ git clone https://github.com/ayavrik/yamdb_final.git
$ cd yamdb_final
```

Создайте `.env` файл с параметрами подключения к БД в директории `infra`

```txt
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=username
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django secret key
```

Для сборки контейнеров и запуска всех сервисов (Django, Postgres, Nginx)
перейдите в директорию с файлом `docker-compose.yaml` и выполните команду `docker-compose up --build`

```bash
$ cd infra
$ docker-compose up --build
```

Проверить статус контейнеров можно командой

```bash
$ docker ps -a
```

После запуска контейнеров выполните миграции

```bash
$ docker-compose exec web python manage.py migrate
```

Создайте супер пользователя

```bash
$ docker-compose exec web python manage.py createsuperuser
```

Для отображения статики выполните команду

```bash
$ docker-compose exec web python manage.py collectstatic --no-input
```

Загрузить демо данные в базу можно командой `loaddemodata`.

```bash
$ docker-compose exec web python manage.py loaddemodata
```

После запуска проект будет доступен по ссылке http://localhost/

### Авторы

- Станислав Орловский
- Алексей Исаков
- Евгений Сандалкин
