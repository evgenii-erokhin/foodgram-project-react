# praktikum_new_diplom
# Учебный проект: Foodgram -- продуктовый помошник
### Описание:
Foodgram это веб сервис с помощью которого, пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список(в формате .txt) продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
### Используемые технологии:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
### Как запустить проект:
#### API Foodgram локально:
1. Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:evgenii-erokhin/foodgram-project-react.git
```
```
cd foodgram-project-react
```
2. Cоздать и активировать виртуальное окружение:

* Если у вас Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
* Если у вас Linux или macOS:
```
python3 -m venv venv
```
```
source venv/bib/activate
```
3. Перейти в дерикторию `backend` выполнить миграции и создать супер пользователя:
```
cd backend
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
4. Запустить сервер разработки:
```
python manage.py runserver
```
### Контакты:



