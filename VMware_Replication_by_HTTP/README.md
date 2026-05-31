# VMware Replication Zabbix Template

[English version](#english-version) | [Русская версия](#русская-версия)

---

## Русская версия

# Шаблон Zabbix для мониторинга VMware Replication

Шаблон предназначен для контроля состояния репликаций виртуальных машин, pairings между площадками, состояния vCenter/VRM-компонентов и основных параметров синхронизации.

Шаблон использует JavaScript `SCRIPT` items в Zabbix, выполняет авторизацию в VMware Replication REST API, получает данные о pairings, репликациях и replication servers, после чего создает элементы данных и триггеры через low-level discovery.

## Возможности

Шаблон собирает информацию о VMware Replication и реплицируемых виртуальных машинах.

Мониторинг включает:

* автоматическое обнаружение pairings;
* автоматическое обнаружение репликаций виртуальных машин;
* состояние pairing между локальным и удаленным vCenter;
* состояние репликации каждой ВМ;
* состояние конфигурации репликации;
* текст ошибки конфигурации репликации;
* время последней синхронизации;
* длительность последней синхронизации;
* размер последней синхронизации;
* состояние network compression;
* состояние vCenter server;
* состояние VRM replication server;
* количество репликаций на VRM server;
* проверку ошибок получения данных из VMware Replication API.

## Триггеры

Шаблон содержит триггеры для следующих событий:

* ошибка получения информации из VMware Replication API;
* vCenter server находится в состоянии `WARNING`;
* vCenter server находится в состоянии `ERROR`;
* configuration state репликации находится в состоянии `UNKNOWN`;
* configuration state репликации находится в состоянии `ERROR`;
* статус репликации находится в состоянии `INITIAL_FULL_SYNC`;
* статус репликации находится в состоянии `ERROR_RPO_VIOLATION`;
* статус репликации находится в состоянии `ERROR`;
* статус репликации отличается от `OK`.

Для части триггеров настроены зависимости, чтобы уменьшить дублирование уведомлений при связанных событиях.

## Требования

* Zabbix 7.0 или выше
* Доступ Zabbix Server или Zabbix Proxy к VMware Replication appliance
* Доступ к VMware Replication REST API
* Учетная запись VMware с правами чтения информации о репликациях
* Настроенные VMware Replication pairings и репликации виртуальных машин

## Макросы

После импорта шаблона необходимо задать макросы на уровне хоста или шаблона:

| Macro                | Description                                                            |
| -------------------- | ---------------------------------------------------------------------- |
| `{$VRM.URL}`         | URL VMware Replication appliance, например `https://vrm.example.local` |
| `{$VMWARE.USERNAME}` | Имя пользователя VMware                                                |
| `{$VMWARE.PASSWORD}` | Пароль пользователя VMware                                             |

Пример:

```text
{$VRM.URL} = https://vrm.example.local
{$VMWARE.USERNAME} = monitor@example.local
{$VMWARE.PASSWORD} = your_password
```

## Используемый API

Шаблон использует VMware Replication REST API v2.

Основные endpoints:

```text
/api/rest/vr/v2/session
/api/rest/vr/v2/info/
/api/rest/vr/v2/pairings/
/api/rest/vr/v2/pairings/{pairing_id}/replications?extended_info=true
/api/rest/vr/v2/replication-servers/
```

## Как это работает

Шаблон выполняет следующие действия:

1. Авторизуется в VMware Replication API через endpoint `/api/rest/vr/v2/session`.
2. Получает session ID.
3. Использует заголовок `x-dr-session` для последующих запросов.
4. Получает список pairings.
5. Получает список репликаций для каждого pairing.
6. Получает общую информацию о VMware Replication и replication servers.
7. Создает обнаруженные объекты через low-level discovery.
8. Создает dependent items и triggers для каждой найденной репликации и серверов.

## Установка

1. Скачайте файл шаблона из репозитория.
2. В Zabbix откройте:

```text
Data collection → Templates → Import
```

3. Импортируйте файл шаблона.
4. Создайте хост для VMware Replication appliance.
5. Привяжите к хосту шаблон:

```text
VMware Replication
```

6. Укажите макросы `{$VRM.URL}`, `{$VMWARE.USERNAME}` и `{$VMWARE.PASSWORD}`.
7. Убедитесь, что Zabbix Server или Zabbix Proxy имеет сетевой доступ к VMware Replication appliance.
8. Дождитесь выполнения low-level discovery rules.

## Value map

Шаблон использует value map `Status Mapping`, который преобразует числовые значения в человекочитаемые статусы:

* `OK`
* `SYNC`
* `INITIAL_FULL_SYNC`
* `UNKNOWN`
* `NOT_ACTIVE`
* `IN_PROGRESS`
* `PAUSED`
* `FULL_SYNC`
* `RPO_VIOLATION`
* `SYNC_RPO_VIOLATION`
* `NOT_ACTIVE_RPO_VIOLATION`
* `FULL_SYNC_RPO_VIOLATION`
* `MOVING`
* `RECOVERING`
* `RECOVERED`
* `DISK_RESIZING`
* `CONFIGURING`
* `WARNING`
* `ERROR_RPO_VIOLATION`
* `ERROR`

## Безопасность

Рекомендуется использовать отдельную учетную запись VMware только для мониторинга и выдать ей минимально необходимые права на чтение.

Не храните реальные логины и пароли в репозитории.

## Совместимость

Шаблон подготовлен для Zabbix 7.0+.

Работа на других версиях Zabbix возможна, но требует отдельной проверки.

## Статус проекта

Текущая версия шаблона: `0.8.5`

Шаблон находится в процессе практического использования и доработки. Pull requests, issues и предложения приветствуются.

---

## English version

# Zabbix Template for VMware Replication Monitoring

This repository contains a Zabbix template for monitoring VMware Replication / VMware vSphere Replication via REST API.

The template is designed to monitor virtual machine replication status, site pairings, vCenter/VRM component status and main synchronization metrics.

The template uses Zabbix JavaScript `SCRIPT` items, authenticates against the VMware Replication REST API, retrieves pairings, replications and replication server information, and then creates items and triggers through low-level discovery.

## Features

The template collects information about VMware Replication and replicated virtual machines.

Monitoring includes:

* automatic pairing discovery;
* automatic virtual machine replication discovery;
* pairing status between local and remote vCenter;
* replication status for each VM;
* replication configuration state;
* replication configuration error message;
* last sync time;
* last sync duration;
* last sync size;
* network compression state;
* vCenter server status;
* VRM replication server connected state;
* replication count per VRM server;
* VMware Replication API data collection error check.

## Triggers

The template includes triggers for the following events:

* failed to get information from VMware Replication API;
* vCenter server status is `WARNING`;
* vCenter server status is `ERROR`;
* replication configuration state is `UNKNOWN`;
* replication configuration state is `ERROR`;
* replication status is `INITIAL_FULL_SYNC`;
* replication status is `ERROR_RPO_VIOLATION`;
* replication status is `ERROR`;
* replication status is not `OK`.

Some triggers include dependencies to reduce duplicate alerts for related events.

## Requirements

* Zabbix 7.0 or later
* Network access from Zabbix Server or Zabbix Proxy to the VMware Replication appliance
* Access to VMware Replication REST API
* VMware account with read permissions for replication information
* Configured VMware Replication pairings and virtual machine replications

## Macros

After importing the template, define the following macros at the host or template level:

| Macro                | Description                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| `{$VRM.URL}`         | VMware Replication appliance URL, for example `https://vrm.example.local` |
| `{$VMWARE.USERNAME}` | VMware username                                                           |
| `{$VMWARE.PASSWORD}` | VMware user password                                                      |

Example:

```text
{$VRM.URL} = https://vrm.example.local
{$VMWARE.USERNAME} = monitor@example.local
{$VMWARE.PASSWORD} = your_password
```

## API Endpoints

The template uses VMware Replication REST API v2.

Main endpoints:

```text
/api/rest/vr/v2/session
/api/rest/vr/v2/info/
/api/rest/vr/v2/pairings/
/api/rest/vr/v2/pairings/{pairing_id}/replications?extended_info=true
/api/rest/vr/v2/replication-servers/
```

## How It Works

The template performs the following steps:

1. Authenticates against the VMware Replication API using `/api/rest/vr/v2/session`.
2. Retrieves a session ID.
3. Uses the `x-dr-session` header for subsequent requests.
4. Retrieves the pairing list.
5. Retrieves the replication list for each pairing.
6. Retrieves VMware Replication and replication server information.
7. Creates discovered objects using low-level discovery.
8. Creates dependent items and triggers for each discovered replication and server.

## Installation

1. Download the template file from this repository.
2. In Zabbix, open:

```text
Data collection → Templates → Import
```

3. Import the template file.
4. Create a host for the VMware Replication appliance.
5. Link the following template to the host:

```text
VMware Replication
```

6. Configure the required macros: `{$VRM.URL}`, `{$VMWARE.USERNAME}` and `{$VMWARE.PASSWORD}`.
7. Make sure Zabbix Server or Zabbix Proxy can access the VMware Replication appliance.
8. Wait for the low-level discovery rules to run.

## Value Map

The template uses the `Status Mapping` value map to convert numeric values into readable statuses:

* `OK`
* `SYNC`
* `INITIAL_FULL_SYNC`
* `UNKNOWN`
* `NOT_ACTIVE`
* `IN_PROGRESS`
* `PAUSED`
* `FULL_SYNC`
* `RPO_VIOLATION`
* `SYNC_RPO_VIOLATION`
* `NOT_ACTIVE_RPO_VIOLATION`
* `FULL_SYNC_RPO_VIOLATION`
* `MOVING`
* `RECOVERING`
* `RECOVERED`
* `DISK_RESIZING`
* `CONFIGURING`
* `WARNING`
* `ERROR_RPO_VIOLATION`
* `ERROR`

## Security Notes

It is recommended to use a dedicated VMware account for monitoring and grant it only the minimum required read permissions.

Do not store real usernames or passwords in the repository.

## Compatibility

The template was prepared for Zabbix 7.0.

Compatibility with other Zabbix versions is possible but should be tested separately.

## Project Status

Current template version: `0.8.5`

The template is in practical use and under further development. Pull requests, issues and suggestions are welcome.
