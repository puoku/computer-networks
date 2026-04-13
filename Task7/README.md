# Task7

В этом задании редирект для российских IP реализован на уровне сервера через `nginx`.

Логика:

- `nginx` принимает запрос
- проверяет IP клиента по списку российских подсетей
- если IP попадает под блокировку, делает редирект на `/denied.html`
- если не попадает, проксирует запрос в приложение


## Запуск

Все команды выполнять из папки `Task7`.

### 1. Создать сеть

```bash
docker network create task7-network
```

### 2. Запустить PostgreSQL

```bash
docker run -d \
  --name task7-db \
  --network task7-network \
  -e POSTGRES_DB=parser_db \
  -e POSTGRES_USER=parser_user \
  -e POSTGRES_PASSWORD=parser_password \
  -p 5432:5432 \
  postgres:16
```

### 3. Собрать образ приложения

```bash
docker build -f Dockerfile.app -t task7-app .
```

### 4. Запустить приложение

```bash
docker run -d \
  --name task7-app \
  --network task7-network \
  -e DB_NAME=parser_db \
  -e DB_USER=parser_user \
  -e DB_PASSWORD=parser_password \
  -e DB_HOST=task7-db \
  -e DB_PORT=5432 \
  -p 8001:8001 \
  task7-app
```

### 5. Собрать образ nginx

```bash
docker build -t task7-nginx .
```

### 6. Запустить nginx

```bash
docker run -d \
  --name task7-nginx \
  --network task7-network \
  -p 80:80 \
  task7-nginx
```

## Проверка

Проверить контейнеры:

```bash
docker ps
```

Проверить приложение:

```text
http://127.0.0.1:8001/docs
```

Проверить задачу:

```text
http://127.0.0.1/
```

Ожидаемое поведение:

- если IP попадает под блокировку, открывается `denied.html`
- если IP не попадает под блокировку, запрос уходит в приложение

## Полезные команды

Логи nginx:

```bash
docker logs task7-nginx
```

Логи приложения:

```bash
docker logs task7-app
```

Логи базы:

```bash
docker logs task7-db
```
