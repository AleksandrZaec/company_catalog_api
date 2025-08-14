# Company Catalog API
REST API для справочника организаций, зданий и видов деятельности. Позволяет хранить и искать организации по зданиям, видам деятельности и геопозиции.

## Стек технологий

- **Python** 3.12
- **FastAPI**
- **Pydantic**
- **SQLAlchemy (async)**
- **Alembic**
- **PostgreSQL**
- **Docker & Docker Compose**
- **pytest / pytest-asyncio**

## Установка и запуск

### 1. Клонирование репозитория

```sh
 git clone https://github.com/AleksandrZaec/company_catalog_api.git
```

### 2. Настройка переменных окружения
В корне проекта создайте два файла окружения .env (основной файл конфигурации для запуска приложения), .env.test (файл с конфигурацией для тестовой базы данных) оба файла можно создать но основе env_example, затем отредактируйте переменные в .env.test, что бы они указывали на тестовую БД.

### 3. Запуск через Docker Compose

```sh
 docker-compose up -d --build
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000/`

Для запуска тестов используйте команду:

```sh
 docker-compose run --rm tests
```

### Документация
После запуска сервера документацию будет доступна по  адресу:

Swagger UI:
```sh
http://localhost:8000//docs/ 
```

Redoc:
```sh
http://localhost:8000/redoc
```