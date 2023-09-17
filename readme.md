Дипломный проект. Сайт медицинской компании

1. Для запуска приложения необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью команд:
    Команда для Windows:
    1- python -m venv venv
    2- venv\Scripts\activate
    3- pip install -r requirement.txt

    Команда для Unix:
    1- python3 -m venv venv
    2- source venv/bin/activate 
    3- pip install -r requirement.txt

2. Для запуска redis:
    Redis официально не поддерживается в Windows: 
    1- Установите WSL2, Ubuntu. Подробности смотрите тут https://redis.io/docs/getting-started/installation/install-redis-on-windows/
    2- sudo apt-get update
    3- sudo service redis-server start
    4- redis-cli
    5- ping

    Ответом от сервиса должно быть PONG. Это означает что Redis подключен

    Команда для Unix:
    1- redis-cli

3. Создать БД
    1- Выполнить вход
    sudo -u postgres psql
    2- Cоздать базу данных с помощью следующей команды:
    CREATE DATABASE medical;
    3- Выйти
    \q

4. Применить миграции:
    1-  python manage.py makemigrations
    2-  python manage.py migrate

 
 
5. Для заполнения моделей данными необходимо выполнить следующую команду:
    Команда для Windows:
    1-  python manage.py loaddata blog.json  
    Команда для Unix:
    1- python3 manage.py loaddata blog.json
    
6. Для работы с переменными окружениями необходимо заполнить файл .env на основе .env.sample

7. Для создания администратора (createsuperuser)
   - заполните поля email, PASSWORD. users/management/commands/csu.py
   Команда для Windows
   1- python manage.py csu

    Команда для Unix
   1- python3 manage.py csu
8. Для запуска приложения:
   Команда для Windows:
      - python manage.py runserver
   Команда для Unix:
      - python3 manage.py runserver
8. Для запуска celery:
   1- celery -A config worker -l info
   2- celery -A core beat -l INFO     
10. Доступ к сайту осуществляется по IP-адресу: http://127.0.0.1:8000/  
11. Доступ к административной панели: http://127.0.0.1:8000/admin/











