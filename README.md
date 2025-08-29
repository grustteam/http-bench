# HTTP Bench 
Консольная программа для тестирования доступности серверов по http протоколу.

## Требования 
- Python 3.10 +
- Библиотека requests

Установка библиотеки:
```bash
pip install requests
```

### Содержание 
Название файла  | Содержание файла
----------------|----------------------
bench.py        | Основной скрипт для тестирования доступности серверов
hosts.txt       | Список хостов для тестирования
readme.md       | Описание работы программы, инструкция по запуску и примеры вывода

### ЗАПУСК
```bash
# Запуск через список хостов:
python bench.py -H https://google.com,https://ya.ru -C 5

# Запуск через файл с хостами:
python bench.py -F hosts.txt -C 5

# Сохранение вывода в файл:
python bench.py -H https://google.com -O output.txt

# Попытка указать оба ключа (-H и -F):
usage: Bench [-h] [-C [COUNT]] [-H HOSTS] [-F FILE] [-O OUTPUT]
Bench: error: You can specify either only one argument (-H or -F)

# Пример вывода:

Host:    https://google.com
Success: 1
Failed:  0
Errors:  0
Min:     0.931684
Max:     0.931684
Avg:     0.931684
----------------------------------------
Incorrect input: htdtps://google.com || _EXPECTED_ https://example.com
----------------------------------------

# Формат файла hosts.txt:
https://google.com
htttps://ya.ru
https://store.steampowered.com
https://github.com
