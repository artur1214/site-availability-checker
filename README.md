# Engilsh ReadMe (Russian is below):
## AVASITE
### Author:
[artur1214](https://github.com/artur1214)

[me at vk.com](https://vk.com/avartur92)

[Email me](mailto:artur.vinogradov1214@gmail.com)

[Or call me (better never do it)](tel:+79026785788)
## Site availability checker.

### Before we start: install reqiurements
```shell
pip install -r requirements.txt
```
#### NOTE: python 3.10 is required.

### usage (may be viewed by `-h` flag providing):
```
usage: avasite [-h] [--inp CONNECTION_STRING] [--inf] [--period PERIOD] [--skip_invalid]

Site availability checker

options:
  -h, --help            show this help message and exit
  --inp CONNECTION_STRING
                        Input string. looks like "con_type:path." Currently available protocols are: csv, json
                        E.G csv:input.csv or json:files/inp.json (DEFAULT: csv:input.csv)
  --inf                 Run program infinitely, till someone stop it.
  --period PERIOD       Period of availability check in seconds. Is used only with --inf.
  --skip_invalid        Skip invalid input. If provided, invalid values in input will be ignored
```
example:

##### input.csv

```text
Host;Ports
ya.ru;xzx1
localhost;
;80
yandex.ru;443
last.fm;80,443
172.16.3.1;53
192.168.1.210;53
```
##### app start:
```shell
python avasite.py --skip_invalid
#output:
Check results:
2023-02-27 17:34:54.184700 | localhost | 127.0.0.1 | 0.106 ms | ??? | Address pingable.
2023-02-27 17:34:56.188315 | localhost | 127.0.0.1 | 0.074 ms | ??? | Address pingable.
2023-02-27 17:34:56.248491 | yandex.ru | 77.88.55.55 | 46.489990234375 ms | 443 | opened
2023-02-27 17:34:56.297754 | yandex.ru | 5.255.255.80 | 49.067626953125 ms | 443 | opened
2023-02-27 17:34:56.349926 | yandex.ru | 5.255.255.88 | 51.8876953125 ms | 443 | opened
2023-02-27 17:34:56.400635 | yandex.ru | 77.88.55.50 | 50.462890625 ms | 443 | opened
2023-02-27 17:34:56.449522 | last.fm | 34.96.123.111 | 46.653564453125 ms | 80 | opened
2023-02-27 17:34:56.496403 | last.fm | 34.96.123.111 | 46.676025390625 ms | 443 | opened
2023-02-27 17:35:01.501965 | ??? | 172.16.3.1 | 0 ms | 53 | Closed
2023-02-27 17:35:06.507704 | ??? | 192.168.1.210 | 0 ms | 53 | Closed
```
### Note:
In linux might be needed `sudo` to be used with (because we need to create sockets, and on some systems this might require root privileges)

----------

# Русский
## AVASITE
### Автор:
[artur1214](https://github.com/artur1214)

[Я в контакте](https://vk.com/avartur92)

[Моя почта](mailto:artur.vinogradov1214@gmail.com)

[Позвонить: (лучше никогда этого не делать)](tel:+79026785788)
## Приложение для проверки доступности сайта. Выполнено в рамках выполнения задания для олимпиады "троектория будущего" [https://tbolimpiada.ru](https://tbolimpiada.ru)

### Перед началом, нужно установить зависимости:
```shell
pip install -r requirements.txt
```
#### ВАЖНО: необходим python 3.10+.

### usage (можно посмотреть, используя флаг `-h`):
```
usage: avasite [-h] [--inp CONNECTION_STRING] [--inf] [--period PERIOD] [--skip_invalid]

Site availability checker

options:
  -h, --help            show this help message and exit
  --inp CONNECTION_STRING
                        Input string. looks like "con_type:path." Currently available protocols are: csv, json
                        E.G csv:input.csv or json:files/inp.json (DEFAULT: csv:input.csv)
  --inf                 Run program infinitely, till someone stop it.
  --period PERIOD       Period of availability check in seconds. Is used only with --inf.
  --skip_invalid        Skip invalid input. If provided, invalid values in input will be ignored
```
Пример:

##### input.csv

```text
Host;Ports
ya.ru;xzx1
localhost;
;80
yandex.ru;443
last.fm;80,443
172.16.3.1;53
192.168.1.210;53
```
##### Использование приложения:
```shell
python avasite.py --skip_invalid
#Вывод:
Check results:
2023-02-27 17:34:54.184700 | localhost | 127.0.0.1 | 0.106 ms | ??? | Address pingable.
2023-02-27 17:34:56.188315 | localhost | 127.0.0.1 | 0.074 ms | ??? | Address pingable.
2023-02-27 17:34:56.248491 | yandex.ru | 77.88.55.55 | 46.489990234375 ms | 443 | opened
2023-02-27 17:34:56.297754 | yandex.ru | 5.255.255.80 | 49.067626953125 ms | 443 | opened
2023-02-27 17:34:56.349926 | yandex.ru | 5.255.255.88 | 51.8876953125 ms | 443 | opened
2023-02-27 17:34:56.400635 | yandex.ru | 77.88.55.50 | 50.462890625 ms | 443 | opened
2023-02-27 17:34:56.449522 | last.fm | 34.96.123.111 | 46.653564453125 ms | 80 | opened
2023-02-27 17:34:56.496403 | last.fm | 34.96.123.111 | 46.676025390625 ms | 443 | opened
2023-02-27 17:35:01.501965 | ??? | 172.16.3.1 | 0 ms | 53 | Closed
2023-02-27 17:35:06.507704 | ??? | 192.168.1.210 | 0 ms | 53 | Closed
```

### Небольшое уточнение:
На некоторых машинах с линуксом, может потребовать права `sudo`, потому что без них на некоторых компьютерах нельзя создавать сокеты.

