# LibreHardwareMonitor Zabbix Template

[English version](#english-version) | [Русская версия](#русская-версия)

---

## Русская версия

# Шаблон Zabbix для мониторинга LibreHardwareMonitor

Этот репозиторий содержит шаблон Zabbix для мониторинга аппаратных датчиков Windows-компьютера через LibreHardwareMonitor.

Шаблон получает данные из встроенного веб-сервера LibreHardwareMonitor по HTTP API, автоматически обнаруживает доступные датчики и создает элементы данных для мониторинга температуры CPU, GPU, NVMe, HDD/SSD и скорости вентиляторов.

Шаблон предназначен для мониторинга физических Windows-серверов, рабочих станций и домашних лабораторий, где требуется получать аппаратные метрики без установки Zabbix Agent с дополнительными скриптами.

## Возможности

Шаблон собирает данные из `data.json`, который отдает встроенный веб-сервер LibreHardwareMonitor.

Мониторинг включает:

* температуру CPU;
* температуру GPU;
* температуру NVMe-накопителей;
* температуру HDD/SSD;
* скорость вентиляторов;
* автоматическое обнаружение поддерживаемых датчиков;
* фильтрацию вентиляторов по регулярному выражению;
* триггеры по температурным порогам CPU;
* триггеры по температурным порогам GPU;
* триггеры по температурным порогам NVMe;
* триггеры по температурным порогам HDD/SSD.

## Требования

* Zabbix 7.4 или выше
* Windows-хост с установленным LibreHardwareMonitor
* Включенный встроенный веб-сервер LibreHardwareMonitor
* Доступ Zabbix Server или Zabbix Proxy к HTTP-порту LibreHardwareMonitor
* Включенная HTTP-аутентификация в LibreHardwareMonitor

## Макросы

После импорта шаблона необходимо задать макросы на уровне хоста или шаблона:

| Macro                        | Description                                                               |
| ---------------------------- | ------------------------------------------------------------------------- |
| `{$LHM.URL}`                 | URL веб-сервера LibreHardwareMonitor, например `http://192.168.1.10:8085` |
| `{$LHM.USER}`                | Имя пользователя для Basic authentication                                 |
| `{$LHM.PASSWORD}`            | Хеш пароля из конфигурационного файла LibreHardwareMonitor                |
| `{$LHM.FAN.EXCLUDE.MATCHES}` | Регулярное выражение для исключения вентиляторов из обнаружения           |
| `{$CPU.TEMP.WARNING}`        | Warning-порог температуры CPU                                             |
| `{$CPU.TEMP.AVERAGE}`        | Average-порог температуры CPU                                             |
| `{$CPU.TEMP.HIGH}`           | High-порог температуры CPU                                                |
| `{$GPU.TEMP.WARNING}`        | Warning-порог температуры GPU                                             |
| `{$GPU.TEMP.AVERAGE}`        | Average-порог температуры GPU                                             |
| `{$GPU.TEMP.HIGH}`           | High-порог температуры GPU                                                |
| `{$NVME.TEMP.WARNING}`       | Warning-порог температуры NVMe                                            |
| `{$NVME.TEMP.AVERAGE}`       | Average-порог температуры NVMe                                            |
| `{$NVME.TEMP.HIGH}`          | High-порог температуры NVMe                                               |
| `{$DRIVE.TEMP.WARNING}`      | Warning-порог температуры HDD/SSD                                         |
| `{$DRIVE.TEMP.AVERAGE}`      | Average-порог температуры HDD/SSD                                         |
| `{$DRIVE.TEMP.HIGH}`         | High-порог температуры HDD/SSD                                            |

Пример:

```text
{$LHM.URL} = http://192.168.1.10:8085
{$LHM.USER} = zabbix
{$LHM.PASSWORD} = password_hash_from_lhm_config
```

Пороговые значения по умолчанию:

| Macro                   | Default |
| ----------------------- | ------- |
| `{$CPU.TEMP.WARNING}`   | `75`    |
| `{$CPU.TEMP.AVERAGE}`   | `85`    |
| `{$CPU.TEMP.HIGH}`      | `95`    |
| `{$GPU.TEMP.WARNING}`   | `75`    |
| `{$GPU.TEMP.AVERAGE}`   | `85`    |
| `{$GPU.TEMP.HIGH}`      | `95`    |
| `{$NVME.TEMP.WARNING}`  | `65`    |
| `{$NVME.TEMP.AVERAGE}`  | `75`    |
| `{$NVME.TEMP.HIGH}`     | `80`    |
| `{$DRIVE.TEMP.WARNING}` | `45`    |
| `{$DRIVE.TEMP.AVERAGE}` | `50`    |
| `{$DRIVE.TEMP.HIGH}`    | `55`    |

## Настройка LibreHardwareMonitor

1. Скачайте LibreHardwareMonitor.
2. Распакуйте архив, например в каталог:

```text
C:\LibreHardwareMonitor
```

3. Запустите `LibreHardwareMonitor.exe`.
4. Включите встроенный веб-сервер LibreHardwareMonitor.
5. Включите аутентификацию.
6. Задайте логин и пароль.
7. Проверьте, что страница веб-сервера доступна с Zabbix Server или Zabbix Proxy.
8. Откройте endpoint:

```text
http://host:port/data.json
```

Если JSON открывается, LibreHardwareMonitor готов к подключению Zabbix.

## Настройка автозапуска через Планировщик заданий Windows

Для стабильной работы мониторинга LibreHardwareMonitor должен запускаться автоматически после включения компьютера.

Рекомендуемые параметры задачи:

### Общие

* Имя задачи: `LibreHardwareMonitor`
* Выполнять для всех пользователей
* Выполнять с наивысшими правами
* Не сохранять пароль, если используются только локальные ресурсы
* Настроить для: `Windows Vista™, Windows Server™ 2008` или более новая доступная версия

### Триггеры

Создайте триггер:

```text
При запуске компьютера
```

### Действия

Добавьте действие:

```text
Запуск программы
```

Путь к программе:

```text
C:\LibreHardwareMonitor\LibreHardwareMonitor.exe
```

Если LibreHardwareMonitor находится в другом каталоге, укажите свой путь.

### Условия

Рекомендуется отключить дополнительные условия запуска, которые могут помешать автоматическому старту:

* не запускать только при простое компьютера;
* не запускать только при питании от электросети;
* не требовать конкретного сетевого подключения.

### Параметры

Рекомендуемые параметры:

* разрешить выполнение задачи по требованию;
* немедленно запускать задачу, если пропущен плановый запуск;
* при сбое выполнения перезапускать через `1 мин.`;
* количество попыток перезапуска: `3`;
* если задача уже выполняется, не запускать новый экземпляр.

## Настройка Zabbix

1. Импортируйте шаблон в Zabbix:

```text
Data collection → Templates → Import
```

2. Создайте хост для Windows-компьютера.
3. Привяжите шаблон:

```text
LibreHardwareMonitor by HTTP
```

4. Укажите макросы:

```text
{$LHM.URL}
{$LHM.USER}
{$LHM.PASSWORD}
```

5. В макрос `{$LHM.PASSWORD}` укажите не исходный пароль, а хеш пароля из конфигурационного файла LibreHardwareMonitor.
6. Проверьте, что item `LHM Raw Data` получает данные.
7. Дождитесь выполнения low-level discovery rules.

## Как это работает

Шаблон использует один основной HTTP item:

```text
lhm.raw.data
```

Он получает JSON-данные из:

```text
{$LHM.URL}/data.json
```

Далее dependent discovery rules разбирают JSON-структуру LibreHardwareMonitor и создают элементы данных для найденных датчиков.

Используемые discovery rules:

* `Get CPU`
* `Get GPU`
* `Get Nvme`
* `Get Drive`
* `Get Fans`

Температурные значения очищаются от единиц измерения, запятая заменяется на точку, после чего Zabbix сохраняет значение как числовую метрику.

## Триггеры

Шаблон содержит триггеры для температурных порогов:

* CPU temperature warning / average / high;
* GPU temperature warning / average / high;
* NVMe temperature warning / average / high;
* HDD/SSD temperature warning / average / high.

Для части триггеров настроены зависимости, чтобы при срабатывании более высокого уровня не дублировались менее критичные уведомления.

## Особенности

Для CPU основные температурные триггеры создаются только для следующих датчиков:

| Sensor | CPU |
|---|---|
| `CPU Package` | Intel CPU |
| `Core (Tctl/Tdie)` | AMD CPU |

То есть для Intel-процессоров триггеры создаются по датчику `CPU Package`, а для AMD-процессоров — по датчику `Core (Tctl/Tdie)`.

Для NVMe основные температурные триггеры создаются для датчика:

```text
Composite Temperature
```

Датчики `Warning Temperature` и `Critical Temperature` могут создаваться как элементы данных без включения температурных триггеров.

Для вентиляторов используется макрос исключения:

```text
{$LHM.FAN.EXCLUDE.MATCHES}
```

По умолчанию исключаются некоторые вентиляторы вида:

```text
Fan #3
Fan #4
...
Fan #10
```

## Безопасность

Не публикуйте реальные логины, пароли и хеши паролей в репозитории.

Если веб-сервер LibreHardwareMonitor доступен по сети, ограничьте доступ к нему с помощью firewall и разрешите подключения только с Zabbix Server или Zabbix Proxy.

## Совместимость

Шаблон подготовлен для Zabbix 7.4.

Работа на других версиях Zabbix возможна, но требует отдельной проверки.

## Статус проекта

Текущая версия шаблона: `0.8.0`

Шаблон находится в процессе практического использования и доработки. Pull requests, issues и предложения приветствуются.

---

## English version

# Zabbix Template for LibreHardwareMonitor

This repository contains a Zabbix template for monitoring Windows hardware sensors via LibreHardwareMonitor.

The template collects data from the built-in LibreHardwareMonitor web server over HTTP API, automatically discovers available sensors and creates items for CPU, GPU, NVMe, HDD/SSD temperatures and fan speeds.

The template is suitable for monitoring physical Windows servers, workstations and homelab systems where hardware metrics are required without using additional Zabbix Agent scripts.

## Features

The template collects data from the `data.json` endpoint provided by the LibreHardwareMonitor web server.

Monitoring includes:

* CPU temperature;
* GPU temperature;
* NVMe temperature;
* HDD/SSD temperature;
* fan speed;
* automatic sensor discovery;
* fan filtering using a regular expression;
* CPU temperature threshold triggers;
* GPU temperature threshold triggers;
* NVMe temperature threshold triggers;
* HDD/SSD temperature threshold triggers.

## Requirements

* Zabbix 7.4 or later
* Windows host with LibreHardwareMonitor installed
* Enabled LibreHardwareMonitor built-in web server
* Network access from Zabbix Server or Zabbix Proxy to the LibreHardwareMonitor HTTP port
* Enabled HTTP authentication in LibreHardwareMonitor

## Macros

After importing the template, define the following macros at the host or template level:

| Macro                        | Description                                                                 |
| ---------------------------- | --------------------------------------------------------------------------- |
| `{$LHM.URL}`                 | LibreHardwareMonitor web server URL, for example `http://192.168.1.10:8085` |
| `{$LHM.USER}`                | Username for Basic authentication                                           |
| `{$LHM.PASSWORD}`            | Password hash from the LibreHardwareMonitor configuration file              |
| `{$LHM.FAN.EXCLUDE.MATCHES}` | Regular expression for excluding fans from discovery                        |
| `{$CPU.TEMP.WARNING}`        | CPU warning temperature threshold                                           |
| `{$CPU.TEMP.AVERAGE}`        | CPU average temperature threshold                                           |
| `{$CPU.TEMP.HIGH}`           | CPU high temperature threshold                                              |
| `{$GPU.TEMP.WARNING}`        | GPU warning temperature threshold                                           |
| `{$GPU.TEMP.AVERAGE}`        | GPU average temperature threshold                                           |
| `{$GPU.TEMP.HIGH}`           | GPU high temperature threshold                                              |
| `{$NVME.TEMP.WARNING}`       | NVMe warning temperature threshold                                          |
| `{$NVME.TEMP.AVERAGE}`       | NVMe average temperature threshold                                          |
| `{$NVME.TEMP.HIGH}`          | NVMe high temperature threshold                                             |
| `{$DRIVE.TEMP.WARNING}`      | HDD/SSD warning temperature threshold                                       |
| `{$DRIVE.TEMP.AVERAGE}`      | HDD/SSD average temperature threshold                                       |
| `{$DRIVE.TEMP.HIGH}`         | HDD/SSD high temperature threshold                                          |

Example:

```text
{$LHM.URL} = http://192.168.1.10:8085
{$LHM.USER} = zabbix
{$LHM.PASSWORD} = password_hash_from_lhm_config
```

Default threshold values:

| Macro                   | Default |
| ----------------------- | ------- |
| `{$CPU.TEMP.WARNING}`   | `75`    |
| `{$CPU.TEMP.AVERAGE}`   | `85`    |
| `{$CPU.TEMP.HIGH}`      | `95`    |
| `{$GPU.TEMP.WARNING}`   | `75`    |
| `{$GPU.TEMP.AVERAGE}`   | `85`    |
| `{$GPU.TEMP.HIGH}`      | `95`    |
| `{$NVME.TEMP.WARNING}`  | `65`    |
| `{$NVME.TEMP.AVERAGE}`  | `75`    |
| `{$NVME.TEMP.HIGH}`     | `80`    |
| `{$DRIVE.TEMP.WARNING}` | `45`    |
| `{$DRIVE.TEMP.AVERAGE}` | `50`    |
| `{$DRIVE.TEMP.HIGH}`    | `55`    |

## LibreHardwareMonitor Setup

1. Download LibreHardwareMonitor.
2. Extract it, for example to:

```text
C:\LibreHardwareMonitor
```

3. Start `LibreHardwareMonitor.exe`.
4. Enable the built-in web server.
5. Enable authentication.
6. Set username and password.
7. Make sure the web server page is accessible from Zabbix Server or Zabbix Proxy.
8. Open the endpoint:

```text
http://host:port/data.json
```

If the JSON response is available, LibreHardwareMonitor is ready for Zabbix monitoring.

## Windows Task Scheduler Setup

LibreHardwareMonitor should start automatically when the computer starts.

Recommended task settings:

### General

* Task name: `LibreHardwareMonitor`
* Run whether user is logged on or not
* Run with highest privileges
* Do not store password if only local computer resources are used
* Configure for: `Windows Vista™, Windows Server™ 2008` or a newer available version

### Triggers

Create a trigger:

```text
At startup
```

### Actions

Create an action:

```text
Start a program
```

Program path:

```text
C:\LibreHardwareMonitor\LibreHardwareMonitor.exe
```

If LibreHardwareMonitor is located in another directory, specify your own path.

### Conditions

It is recommended to disable additional conditions that may prevent automatic startup:

* do not require computer idle state;
* do not require AC power;
* do not require a specific network connection.

### Settings

Recommended settings:

* allow task to be run on demand;
* run task as soon as possible after a scheduled start is missed;
* restart every `1 minute` on failure;
* restart attempt count: `3`;
* if the task is already running, do not start a new instance.

## Zabbix Setup

1. Import the template in Zabbix:

```text
Data collection → Templates → Import
```

2. Create a host for the Windows computer.
3. Link the template:

```text
LibreHardwareMonitor by HTTP
```

4. Configure the required macros:

```text
{$LHM.URL}
{$LHM.USER}
{$LHM.PASSWORD}
```

5. In `{$LHM.PASSWORD}`, specify the password hash from the LibreHardwareMonitor configuration file, not the plain text password.
6. Make sure the `LHM Raw Data` item receives data.
7. Wait for the low-level discovery rules to run.

## How It Works

The template uses one master HTTP item:

```text
lhm.raw.data
```

It collects JSON data from:

```text
{$LHM.URL}/data.json
```

Dependent discovery rules then parse the LibreHardwareMonitor JSON structure and create items for discovered sensors.

Discovery rules:

* `Get CPU`
* `Get GPU`
* `Get Nvme`
* `Get Drive`
* `Get Fans`

Temperature values are cleaned from units, comma is replaced with a dot, and then Zabbix stores the result as a numeric metric.

## Triggers

The template includes temperature threshold triggers for:

* CPU temperature warning / average / high;
* GPU temperature warning / average / high;
* NVMe temperature warning / average / high;
* HDD/SSD temperature warning / average / high.

Some triggers include dependencies to avoid duplicate alerts when a higher severity threshold is reached.

## Notes

For CPU, main temperature triggers are created only for the following sensors:

| Sensor | CPU |
|---|---|
| `CPU Package` | Intel CPU |
| `Core (Tctl/Tdie)` | AMD CPU |

For Intel CPUs, triggers are created for the `CPU Package` sensor.  
For AMD CPUs, triggers are created for the `Core (Tctl/Tdie)` sensor.

For NVMe, main temperature triggers are created for:

```text
Composite Temperature
```

`Warning Temperature` and `Critical Temperature` sensors may be created as regular items without temperature triggers.

Fan discovery uses the exclusion macro:

```text
{$LHM.FAN.EXCLUDE.MATCHES}
```

By default, some fan names are excluded, for example:

```text
Fan #3
Fan #4
...
Fan #10
```

## Security Notes

Do not publish real usernames, passwords or password hashes in the repository.

If the LibreHardwareMonitor web server is reachable over the network, restrict access with a firewall and allow connections only from Zabbix Server or Zabbix Proxy.

## Compatibility

The template was prepared for Zabbix 7.4.

Compatibility with other Zabbix versions is possible but should be tested separately.

## Project Status

Current template version: `0.8.0`

The template is in practical use and under further development. Pull requests, issues and suggestions are welcome.
