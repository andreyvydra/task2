Чтобы запустить сервер нужно сделать несколько шагов 
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. Предварительно нужно настроить файл .env в папке app для подключения к базе данных
5. python manage.py runserver 8080
