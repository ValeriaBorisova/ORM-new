# ORM-new

Создаем виртуальное окружение

```python -m venv venv```

Активируем виртуальное окружение

```venv\Scripts\activate.bat``` - для Windows;

```source venv/bin/activate``` - для Linux и MacOS.

```pip install peewee``` - Установка Peewee

Запускаем flask сервер

```set FLASK_APP=main.py``` - для Windows

```export FLASK_APP=main.py``` - для mac

```flask run```

Проверяем, что сервер запустился 
``` * Serving Flask app 'main.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
/Users/user/PycharmProjects/New/venv/lib/python3.8/site-packages/flask_sqlalchemy/__init__.py:872: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  warnings.warn(FSADeprecationWarning(
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
