# Task9

Контейнеры работают в одной сети с IPv4 и IPv6:

- `task9-server`: `172.30.0.10`, `fd00:1234::10`
- `task9-client`: `172.30.0.20`, `fd00:1234::20`

## Запуск

Из папки `Task9`:

```bash
docker compose up -d --build
```

## Проверка

```bash
docker compose ps
```

Ожидаемый результат:

- контейнер `task9-server` запущен
- контейнер `task9-client` запущен

## Проверка IPv4

Пинг:

```bash
docker exec task9-client ping -c 4 172.30.0.10
```

HTTP-запрос:

```bash
docker exec task9-client curl http://172.30.0.10
```

Ожидаемый результат:

- `ping` проходит без потерь
- `curl` возвращает HTML-страницу `Task9 IPv4/IPv6 Lab`

## Проверка IPv6

Пинг:

```bash
docker exec task9-client ping -6 -c 4 fd00:1234::10
```

HTTP-запрос:

```bash
docker exec task9-client curl "http://[fd00:1234::10]"
```

Ожидаемый результат:

- `ping -6` проходит без потерь
- `curl` возвращает ту же HTML-страницу

## Проверка через Wireshark

### 1. Снять IPv4-пакеты

В первом терминале:

```bash
docker exec -it task9-client tcpdump -i eth0 -n -w /tmp/ipv4.pcap icmp
```

Во втором терминале:

```bash
docker exec task9-client ping -c 4 172.30.0.10
```

После завершения `ping`:

1. Остановить `tcpdump` через `Ctrl+C`
2. Убедиться, что в выводе есть `packets captured`

Скопировать дамп:

```bash
docker cp task9-client:/tmp/ipv4.pcap ./ipv4.pcap
```

### 2. Снять IPv6-пакеты

В первом терминале:

```bash
docker exec -it task9-client tcpdump -i eth0 -n -w /tmp/ipv6.pcap icmp6
```

Во втором терминале:

```bash
docker exec task9-client ping -6 -c 4 fd00:1234::10
```

После завершения `ping`:

1. Остановить `tcpdump` через `Ctrl+C`
2. Убедиться, что в выводе есть `packets captured`

Скопировать дамп:

```bash
docker cp task9-client:/tmp/ipv6.pcap ./ipv6.pcap
```

### 3. Открыть дампы в Wireshark

```bash
open -a Wireshark ipv4.pcap
open -a Wireshark ipv6.pcap
```

## Остановка стенда

```bash
docker compose down
```

Если используется старый compose:

```bash
docker-compose down
```
