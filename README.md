## NotesAPI


##### REST API для управления заметками с аунтетификацией пользователей.
##### Проект написан на Django Rest Framework, покрыт тестами и подключен CD.

### Возможности

    - Регистрация и аутентификация пользователей
    - JWT-аунтетицикация
    - CRUD для заметок и пользователей
    - Покрытие API тестами (pytest)
    - Автоматический запуск тестов через GitHub Actions
    - Документация API через Swagger/OpenAPI

### Технологии 

    - Python 3.12
    - Django 6.0
    - Djnago Rest Framework
    - SimpleJWT
    - PostgreSQL
    - Pytest
    - GitHub Actions (CI)

### API документация

    Документация доступна после запуска проекта:

    /doc/

### Как запустить локально

##### 1. Клонировать репозиторий
        
    git clone <repository_link>
    cd NotesAPI

##### 2. Установка зависимостей

    pip install -r requirements.txt

##### 3. Установка БД

    Для продакшен-деплоя: PostgreSQL
    Для локального использования: SQLite3

    В файле settings/settings.py заменяете DATABASE = {...}
    на этот код 

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }

##### 4. Применить миграции
    
    python manage.py migrate

##### 5. Запустить сервер

    python manage.py runserver

##### 6. Открыть в браузере 

    http://127.0.0.1:8000/doc/


### Тесты

##### Запуск тестов
    
    В терминале: pytest