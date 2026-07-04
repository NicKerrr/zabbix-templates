# NVR Zabbix Template

[English version](#english-version) | [Русская версия](#русская-версия)

---

## Русская версия

# Шаблон Zabbix для мониторинга NVR

Этот репозиторий содержит шаблон Zabbix и внешний Python-скрипт для мониторинга NVR-видеорегистраторов через CGI API.

Шаблон получает данные с NVR с помощью external check, обрабатывает JSON-ответ скрипта и создает элементы данных для мониторинга общей информации устройства, активных каналов и дисков.

Шаблон предназначен для мониторинга состояния видеорегистраторов, подключенных камер и накопителей.

## Возможности

Мониторинг включает:

* доступность NVR через ICMP;
* получение общей информации о системе;
* версию программного обеспечения;
* build time прошивки;
* hardware ID;
* product ID;
* serial number / cloud ID;
* время работы устройства;
* количество цифровых каналов;
* автоматическое обнаружение активных каналов;
* текущий статус каждого активного канала;
* текущее разрешение канала;
* автоматическое обнаружение дисков;
* тип диска / раздела;
* статус диска;
* общий размер диска;
* время начала записи;
* время окончания записи.

## Триггеры

Шаблон содержит триггеры для следующих событий:

* канал находится в состоянии `Offline`;
* канал находится в состоянии `Login Failed`;
* канал находится не в состоянии `Connected`;
* диск находится в состоянии `Error`.

Для статусов используются value maps, чтобы числовые значения отображались в Zabbix в человекочитаемом виде.

## Требования

* Zabbix 7.0 или выше
* Python 3 на Zabbix Server или Zabbix Proxy
* Возможность выполнять external scripts в Zabbix
* Сетевой доступ от Zabbix Server или Zabbix Proxy к NVR
* Учетная запись NVR с правами чтения информации
* Установленный Python-модуль `pycryptodomex`
* Импортированный стандартный шаблон `ICMP Ping`

## Установка Python-зависимостей

На Zabbix Server или Zabbix Proxy установите зависимость:

```bash
pip3 install pycryptodomex
```

Если используется системный Python и установка через `pip3` запрещена политиками ОС, можно использовать пакетный менеджер или virtualenv. Главное, чтобы скрипт запускался тем Python, который доступен Zabbix external scripts.

## Установка скрипта

Скопируйте файл `nvr.raw.data.py` в каталог external scripts Zabbix.

Обычно это один из путей:

```text
/usr/lib/zabbix/externalscripts/
```

или:

```text
/usr/local/share/zabbix/externalscripts/
```

Точный путь можно проверить в конфигурации Zabbix Server или Proxy:

```bash
grep -i ExternalScripts /etc/zabbix/zabbix_server.conf
```

или:

```bash
grep -i ExternalScripts /etc/zabbix/zabbix_proxy.conf
```

Скопируйте скрипт:

```bash
sudo cp nvr.raw.data.py /usr/lib/zabbix/externalscripts/
```

Выдайте права на выполнение:

```bash
sudo chmod +x /usr/lib/zabbix/externalscripts/nvr.raw.data.py
```

Проверьте владельца и права:

```bash
ls -l /usr/lib/zabbix/externalscripts/nvr.raw.data.py
```

## Проверка скрипта вручную

Проверку лучше выполнять от пользователя `zabbix`, чтобы убедиться, что Zabbix сможет запустить скрипт самостоятельно.

Пример:

```bash
sudo -u zabbix /usr/lib/zabbix/externalscripts/nvr.raw.data.py \
  --host 192.168.1.100 \
  --user admin \
  --password 'your_password' \
  --port 80
```

Если все настроено правильно, скрипт вернет JSON примерно такой структуры:

```json
{
  "system": {},
  "channels": [],
  "disks": [],
  "errors": []
}
```

Если в поле `errors` есть ошибки, нужно проверить доступность NVR, логин, пароль, порт и совместимость API.

## Макросы

После импорта шаблона необходимо задать макросы на уровне хоста:

| Macro             | Description                |
| ----------------- | -------------------------- |
| `{$NVR.USER}`     | Имя пользователя NVR       |
| `{$NVR.PASSWORD}` | Пароль пользователя NVR    |
| `{$NVR.PORT}`     | HTTP-порт NVR, обычно `80` |

Пример:

```text
{$NVR.USER} = admin
{$NVR.PASSWORD} = your_password
{$NVR.PORT} = 80
```

IP-адрес NVR берется из интерфейса хоста Zabbix через `{HOST.CONN}`.

## Импорт шаблона

1. Откройте Zabbix.
2. Перейдите в:

```text
Data collection → Templates → Import
```

3. Импортируйте файл шаблона.
4. Создайте хост для NVR.
5. Укажите IP-адрес NVR в интерфейсе хоста.
6. Привяжите шаблон:

```text
NVR Template
```

7. Укажите макросы:

```text
{$NVR.USER}
{$NVR.PASSWORD}
{$NVR.PORT}
```

8. Проверьте, что item `Get Raw Data` получает JSON.
9. Дождитесь выполнения low-level discovery rules.

## Как это работает

Шаблон использует master item:

```text
Get Raw Data
```

Тип элемента данных:

```text
External check
```

Ключ:

```text
nvr.raw.data.py["--host","{HOST.CONN}","--user","{$NVR.USER}","--password","{$NVR.PASSWORD}","--port","{$NVR.PORT}"]
```

Скрипт подключается к NVR по CGI API, авторизуется, собирает данные и возвращает JSON.

Шаблон дальше использует dependent items и JSONPath preprocessing для извлечения нужных значений.

## Low-level discovery

Шаблон содержит два правила обнаружения:

### Get Channels

Обнаруживает активные каналы, у которых `active = true`.

Для каждого канала создаются элементы:

* current resolution;
* channel status.

Статусы каналов преобразуются через value map `Channel Status`.

### Get Drives

Обнаруживает диски NVR.

Для каждого диска создаются элементы:

* drive type;
* drive status;
* total space;
* record start time;
* record end time.

Статус диска преобразуется через value map `Drive Status`.

## Value maps

### Channel Status

| Value | Status       |
| ----- | ------------ |
| `0`   | Offline      |
| `1`   | Unknown      |
| `2`   | None         |
| `3`   | Login Failed |
| `4`   | No Login     |
| `5`   | No Connect   |
| `6`   | No Config    |
| `10`  | Connected    |

### Drive Status

| Value | Status |
| ----- | ------ |
| `0`   | Normal |
| `1`   | Error  |

### Dirver Type

| Value | Type       |
| ----- | ---------- |
| `0`   | Read/Write |
| `1`   | Read Only  |
| `2`   | Event      |
| `3`   | Redundancy |
| `4`   | Snapshot   |

## Особенности

Скрипт пробует несколько вариантов запросов для получения информации о дисках, так как разные NVR могут возвращать данные в разных разделах API.

Используемые варианты включают:

```text
StorageInfo
HddInfo
HDDInfo
DiskInfo
Storage.StorageInfo
Storage.HddInfo
Storage.HDDInfo
Storage.DiskInfo
Record.Storage
Record.HDD
```

Если один вариант не возвращает данные, скрипт пробует следующий.

## Совместимость

Шаблон подготовлен для Zabbix 7.0.

Работа с другими версиями Zabbix возможна, но требует отдельной проверки.

Совместимость с конкретными моделями NVR зависит от поддержки CGI API и структуры ответов устройства.

## Статус проекта

Текущая версия шаблона: `0.8.0`

Шаблон находится в процессе практического использования и доработки. Pull requests, issues и предложения приветствуются.

---

## English version

# Zabbix Template for NVR Monitoring

This repository contains a Zabbix template and an external Python script for monitoring NVR devices via CGI API.

The template collects data from the NVR using an external check, processes the JSON returned by the script and creates items for system information, active channels and drives.

The template is designed for monitoring NVR device state, connected camera channels and storage drives.

## Features

Monitoring includes:

* NVR availability using ICMP;
* system information;
* software version;
* firmware build time;
* hardware ID;
* product ID;
* serial number / cloud ID;
* device runtime;
* total digital channels;
* automatic active channel discovery;
* current status of each active channel;
* current channel resolution;
* automatic drive discovery;
* drive / partition type;
* drive status;
* total drive space;
* record start time;
* record end time.

## Triggers

The template includes triggers for the following events:

* channel status is `Offline`;
* channel status is `Login Failed`;
* channel status is not `Connected`;
* drive status is `Error`.

Value maps are used to display numeric status values in a readable form.

## Requirements

* Zabbix 7.0 or later
* Python 3 on Zabbix Server or Zabbix Proxy
* External scripts enabled in Zabbix
* Network access from Zabbix Server or Zabbix Proxy to the NVR
* NVR account with read permissions
* Installed Python module `pycryptodomex`
* Imported standard `ICMP Ping` template

## Python Dependencies

Install the required dependency on Zabbix Server or Zabbix Proxy:

```bash
pip3 install pycryptodomex
```

If system-wide `pip3` installation is restricted by the operating system policy, use your package manager or a virtual environment. The important point is that the script must be executable by the Python environment available to Zabbix external scripts.

## Script Installation

Copy `nvr.raw.data.py` to the Zabbix external scripts directory.

Typical paths are:

```text
/usr/lib/zabbix/externalscripts/
```

or:

```text
/usr/local/share/zabbix/externalscripts/
```

You can check the exact path in the Zabbix Server or Proxy configuration:

```bash
grep -i ExternalScripts /etc/zabbix/zabbix_server.conf
```

or:

```bash
grep -i ExternalScripts /etc/zabbix/zabbix_proxy.conf
```

Copy the script:

```bash
sudo cp nvr.raw.data.py /usr/lib/zabbix/externalscripts/
```

Make it executable:

```bash
sudo chmod +x /usr/lib/zabbix/externalscripts/nvr.raw.data.py
```

Check permissions:

```bash
ls -l /usr/lib/zabbix/externalscripts/nvr.raw.data.py
```

## Manual Script Test

It is recommended to run the test as the `zabbix` user to make sure Zabbix can execute the script.

Example:

```bash
sudo -u zabbix /usr/lib/zabbix/externalscripts/nvr.raw.data.py \
  --host 192.168.1.100 \
  --user admin \
  --password 'your_password' \
  --port 80
```

If everything is configured correctly, the script returns JSON with the following structure:

```json
{
  "system": {},
  "channels": [],
  "disks": [],
  "errors": []
}
```

If the `errors` field contains errors, check NVR connectivity, username, password, port and API compatibility.

## Macros

After importing the template, define the following macros at the host level:

| Macro             | Description                 |
| ----------------- | --------------------------- |
| `{$NVR.USER}`     | NVR username                |
| `{$NVR.PASSWORD}` | NVR user password           |
| `{$NVR.PORT}`     | NVR HTTP port, usually `80` |

Example:

```text
{$NVR.USER} = admin
{$NVR.PASSWORD} = your_password
{$NVR.PORT} = 80
```

The NVR IP address is taken from the Zabbix host interface using `{HOST.CONN}`.

## Template Import

1. Open Zabbix.
2. Go to:

```text
Data collection → Templates → Import
```

3. Import the template file.
4. Create a host for the NVR.
5. Set the NVR IP address in the host interface.
6. Link the template:

```text
NVR Template
```

7. Configure the required macros:

```text
{$NVR.USER}
{$NVR.PASSWORD}
{$NVR.PORT}
```

8. Make sure the `Get Raw Data` item receives JSON.
9. Wait for low-level discovery rules to run.

## How It Works

The template uses a master item:

```text
Get Raw Data
```

Item type:

```text
External check
```

Key:

```text
nvr.raw.data.py["--host","{HOST.CONN}","--user","{$NVR.USER}","--password","{$NVR.PASSWORD}","--port","{$NVR.PORT}"]
```

The script connects to the NVR using CGI API, authenticates, collects data and returns JSON.

The template then uses dependent items and JSONPath preprocessing to extract the required values.

## Low-level Discovery

The template contains two discovery rules:

### Get Channels

Discovers active channels where `active = true`.

For each channel, the template creates:

* current resolution;
* channel status.

Channel statuses are converted using the `Channel Status` value map.

### Get Drives

Discovers NVR drives.

For each drive, the template creates:

* drive type;
* drive status;
* total space;
* record start time;
* record end time.

Drive status is converted using the `Drive Status` value map.

## Value Maps

### Channel Status

| Value | Status       |
| ----- | ------------ |
| `0`   | Offline      |
| `1`   | Unknown      |
| `2`   | None         |
| `3`   | Login Failed |
| `4`   | No Login     |
| `5`   | No Connect   |
| `6`   | No Config    |
| `10`  | Connected    |

### Drive Status

| Value | Status |
| ----- | ------ |
| `0`   | Normal |
| `1`   | Error  |

### Dirver Type

| Value | Type       |
| ----- | ---------- |
| `0`   | Read/Write |
| `1`   | Read Only  |
| `2`   | Event      |
| `3`   | Redundancy |
| `4`   | Snapshot   |

## Notes

The script tries multiple API query names to get disk information because different NVR devices may expose storage data in different API sections.

The query names include:

```text
StorageInfo
HddInfo
HDDInfo
DiskInfo
Storage.StorageInfo
Storage.HddInfo
Storage.HDDInfo
Storage.DiskInfo
Record.Storage
Record.HDD
```

If one query does not return disk data, the script tries the next one.

## Compatibility

The template was prepared for Zabbix 7.0.

Compatibility with other Zabbix versions is possible but should be tested separately.

Compatibility with specific NVR models depends on CGI API support and response structure.

## Project Status

Current template version: `0.8.0`

The template is in practical use and under further development. Pull requests, issues and suggestions are welcome.
