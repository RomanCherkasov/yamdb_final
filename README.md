# API YAMDB
### Приложение для работы с API

- Для аутентификации используются JWT-токены.
- У неаутентифицированных пользователей доступ к API только на чтение
- Аутентифицированным пользователям разрешено изменение и удаление своего контента
### Для запуска приложения выполните
``` bash
git clone
docker-compose up -d --build
```
### Для остановки
``` bash
docker container ls

CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                                       NAMES
0de93f0fe431   nginx:1.19.3    "/docker-entrypoint.…"   14 seconds ago   Up 13 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp           infra_sp2_nginx_1
1ebeb89d341a   infra_sp2_web   "/bin/sh -c 'gunicor…"   15 seconds ago   Up 14 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   infra_sp2_web_1
490b785c4b4b   postgres:12.4   "docker-entrypoint.s…"   15 seconds ago   Up 14 seconds   5432/tcp                                    infra_sp2_db_1

docker container stop 0de9 1ebe 490b
```
(0de9 1ebe 490b - первые цифры CONTAINER ID)
### Для повторного запуска
``` bash
docker-compose up
```
### Применение миграций, сбор статики и создание суперпользователя
После запуска выполните поочередно следующие команды:
``` bash
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
### Для загрузки тестовых данных в базу
``` bash
docker-compose exec web python manage.py loaddata <fixturename>.json
```