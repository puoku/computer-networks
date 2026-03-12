## 1) Запуск PostgreSQL

```bash
brew services start postgresql@16
```

## 2) Создание базы данных (один раз)

```bash
psql postgres -c "CREATE DATABASE parser_db;"
```

## 3) Запуск API

```bash
uvicorn main:app --reload --port 8001
```

- Swagger UI: `http://127.0.0.1:8001/docs#/`

## 4) Проверка через curl

Во втором терминале:

```bash
curl "http://127.0.0.1:8001/parse?url=https://en.wikipedia.org/wiki/Category:Food_and_drink&max_pages=2"
```

Ожидаемый ответ:
- `{"saved":60}` или другое число

Потом чтение из таблицы БД:

```bash
curl -s "http://127.0.0.1:8001/items?limit=10" | python -m json.tool
```

## 5) Остановка после работы

Остановить API:
- в терминале с uvicorn нажать `Ctrl + C`

Остановить PostgreSQL:

```bash
brew services stop postgresql@16
```
