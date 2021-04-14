# My_blog
My blog using django

First, clone the blog project
```
git clone https://github.com/athallahmaajid/My_blog.git
```

Create virtualenv:
```
virtualenv django_2 python=3.6
```
Install all the requirements:
```
pip install -r requirements.txt
```
Migrate the blog app
```
cd blog_app
python manage.py makemigrations
python manage.py migrate
```
Run the app:
```
python manage.py runserver
```
And, Voila! the blog app is run on 127.0.0:8000
