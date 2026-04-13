# Task10

## Проверка вручную

Список доменов лежит в domains.txt

### 1. Выполнить DNS-запросы

```bash
nslookup google.com
nslookup github.com
nslookup vk.com
nslookup ozon.ru
nslookup wildberries.ru
```

или:

```bash
dig +short google.com
dig +short github.com
dig +short vk.com
dig +short ozon.ru
dig +short wildberries.ru
```

### 2. Выполнить traceroute для найденных IP

После того как получили IP-адреса, выполнить:

```bash
traceroute -m 5 -w 1 IP_АДРЕС
```

Пример:

```bash
traceroute -m 5 -w 1 142.250.185.206
```

### 3. Сохранить результат в CSV

CSV можно оформить в таком виде:

```csv
domain,ip,hop,hop_ip,raw_line
google.com,142.250.185.206,1,192.168.1.1,"1  192.168.1.1 ..."
```

## Проверка скриптом

Из папки `Task10`:

```bash
python3 task10.py
```

После выполнения появится файл:

```text
results.csv
```

Скрипт запускает `traceroute` в коротком режиме:

- максимум `5` hop-ов
- ожидание `1` секунда на hop

## Проверка результата

Открыть CSV:

```bash
cat results.csv
```

или:

```bash
head results.csv
```

Ожидаемый результат:

- для каждого домена есть IP-адрес
- для каждого IP есть hop-ы traceroute
- всё сохранено в `results.csv`

## Если `traceroute` не установлен

macOS:

```bash
traceroute google.com
```

Linux:

```bash
sudo apt install traceroute
```
