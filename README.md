# ChatGPT Client
## Описание
**ChatGPT Client** - телеграм бот, позволяющий получить доступ к ChatGPT напрямую из телеграма по своему API ключу
## Установка
1. Скопировать репозиторий ```$ git clone https://github.com/zhohov/ChatGPT-Bot.git```
2. Создать .env файл с данными
    ```
    token = 'telegram token'
    opneai_token_api = ''
    admin_id = 
    payments_provider_token = ''
    
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_PORT=5432
    POSTGRES_HOST=db
    ```
3. Изменить ссылку на базу данных в ```alembic.ini``` по примеру
    ```
    sqlalchemy.url = postgresql+asyncpg://name:password@db/db_name
    ```
4. Ввести данные в ```docker-compose.yml```
   ```
   environment:
      POSTGRES_USER: 
      POSTGRES_PASSWORD: 
      POSTGRES_DB: 
   ```
5. Выполнить ```docker-compose up -d```