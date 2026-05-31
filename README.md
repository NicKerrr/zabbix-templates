# Zabbix Templates

[English version](#english-version) | [Русская версия](#русская-версия)

---

## Русская версия

# Шаблоны Zabbix для мониторинга инфраструктуры

Этот репозиторий содержит набор пользовательских шаблонов Zabbix для мониторинга инфраструктурных сервисов и систем.

В текущий набор входят шаблоны для:

* Lenovo Storage DE Series / DE2000H;
* Reg.ru доменов и услуг хостинга;
* VMware Replication / VMware vSphere Replication.

Шаблоны используют HTTP API, REST API, JavaScript preprocessing, dependent items, low-level discovery rules и триггеры для автоматического обнаружения объектов и контроля их состояния.

## Список шаблонов

| Template                           | Description                                                                                          |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `Lenovo Storage DE Series by HTTP` | Мониторинг СХД Lenovo Storage DE Series, в первую очередь Lenovo DE2000H, через HTTP API контроллера |
| `Reg.ru by HTTP`                   | Мониторинг доменов и услуг хостинга Reg.ru через HTTP API                                            |
| `VMware Replication`               | Мониторинг VMware Replication / VMware vSphere Replication через REST API                            |

## Lenovo Storage DE Series / DE2000H

Шаблон предназначен для мониторинга СХД Lenovo Storage DE Series, в первую очередь Lenovo DE2000H, через HTTP API контроллера.

Мониторинг включает:

* общую информацию о системе;
* модель, имя, серийный номер и WWN СХД;
* версии компонентов прошивки;
* загрузку CPU системы;
* общее энергопотребление;
* контроллеры;
* батареи;
* блоки питания;
* вентиляторы;
* температурные датчики;
* диски;
* SSD wear / health statistics;
* storage pools;
* volumes;
* Ethernet management interfaces;
* Fibre Channel interfaces;
* показатели чтения и записи по дискам, томам и FC-интерфейсам.

### Требования

* Zabbix 6.4, 7.0 и выше
* Доступ Zabbix Server или Zabbix Proxy к management IP СХД
* Доступ к Lenovo DE Series REST API
* Учетная запись на СХД с правами чтения
* Импортированный стандартный шаблон `ICMP Ping`

### Макросы

| Macro         | Description                                               |
| ------------- | --------------------------------------------------------- |
| `{$URL}`      | URL API контроллера СХД, например `https://192.168.1.100` |
| `{$USERNAME}` | Имя пользователя для HTTP Basic authentication            |
| `{$PASSWORD}` | Пароль пользователя                                       |

Шаблон подготовлен для Lenovo Storage DE2000H.

Он также может работать с другими системами Lenovo серии DE, если они используют совместимый REST API и аналогичную структуру данных. Совместимость с другими моделями не гарантируется и требует тестирования.

Шаблон был протестирован с версиями программного обеспечения Lenovo DE Series: 11.70, 11.80 и 11.90.

## Reg.ru by HTTP

Шаблон предназначен для мониторинга доменов и услуг хостинга Reg.ru через HTTP API.

Он получает список услуг Reg.ru, автоматически обнаруживает домены и хостинги, создает элементы данных для даты создания, даты окончания и состояния услуги, а также формирует триггеры по приближению срока окончания.

Мониторинг включает:

* автоматическое обнаружение доменов;
* автоматическое обнаружение услуг хостинга;
* дату создания домена;
* дату окончания домена;
* состояние домена;
* дату создания услуги хостинга;
* дату окончания услуги хостинга;
* состояние услуги хостинга;
* уведомления об окончании срока действия через 60, 30 и 7 дней.

### Требования

* Zabbix 7.4 или выше
* Доступ Zabbix Server или Zabbix Proxy к `https://api.reg.ru`
* Учетная запись Reg.ru
* Доступ к Reg.ru API
* Логин и пароль/API password для выполнения API-запросов

### Макросы

| Macro             | Description                                 |
| ----------------- | ------------------------------------------- |
| `{$USERNAME}`     | Имя пользователя Reg.ru                     |
| `{$API.PASSWORD}` | Пароль или API password пользователя Reg.ru |

### Используемый API

```text
https://api.reg.ru/api/regru2/service/get_list
```

Для доменов используется параметр:

```text
servtype=domain
```

Для услуг хостинга используется параметр:

```text
servtype=srv_hosting_ispmgr
```

## VMware Replication

Шаблон предназначен для мониторинга VMware Replication / VMware vSphere Replication через REST API.

Он авторизуется в VMware Replication REST API, получает pairings, список репликаций, информацию о VRM/vCenter и replication servers, после чего создает элементы данных и триггеры через low-level discovery.

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

### Требования

* Zabbix 7.0 или выше
* Доступ Zabbix Server или Zabbix Proxy к VMware Replication appliance
* Доступ к VMware Replication REST API
* Учетная запись VMware с правами чтения информации о репликациях
* Настроенные VMware Replication pairings и репликации виртуальных машин

### Макросы

| Macro                | Description                                                            |
| -------------------- | ---------------------------------------------------------------------- |
| `{$VRM.URL}`         | URL VMware Replication appliance, например `https://vrm.example.local` |
| `{$VMWARE.USERNAME}` | Имя пользователя VMware                                                |
| `{$VMWARE.PASSWORD}` | Пароль пользователя VMware                                             |

### Используемый API

```text
/api/rest/vr/v2/session
/api/rest/vr/v2/info/
/api/rest/vr/v2/pairings/
/api/rest/vr/v2/pairings/{pairing_id}/replications?extended_info=true
/api/rest/vr/v2/replication-servers/
```

## Установка

1. Скачайте нужный файл шаблона из репозитория.
2. В Zabbix откройте:

```text
Data collection → Templates → Import
```

3. Импортируйте файл шаблона.
4. Создайте хост для соответствующей системы или сервиса.
5. Привяжите нужный шаблон к хосту.
6. Укажите необходимые макросы.
7. Убедитесь, что Zabbix Server или Zabbix Proxy имеет сетевой доступ к API целевой системы.
8. Дождитесь выполнения low-level discovery rules.

## Безопасность

Не храните реальные логины, пароли, API keys или API passwords в репозитории.

Рекомендуется использовать отдельные учетные записи только для мониторинга и выдавать им минимально необходимые права на чтение.

Для production-среды рекомендуется предварительно протестировать шаблоны на отдельном хосте или тестовом окружении.

## Совместимость

| Template                         | Tested / Target Zabbix Version |
| -------------------------------- | ------------------------------ |
| Lenovo Storage DE Series by HTTP | Zabbix 7.0 и выше              |
| Reg.ru by HTTP                   | Zabbix 7.0 и выше              |
| VMware Replication               | Zabbix 7.0 и выше              |

Работа на других версиях Zabbix возможна, но требует отдельной проверки.

## Статус проекта

Шаблоны находятся в процессе практического использования и доработки.

Pull requests, issues и предложения приветствуются.

---

## English version

# Zabbix Templates for Infrastructure Monitoring

This repository contains a collection of custom Zabbix templates for monitoring infrastructure systems and services.

The current set includes templates for:

* Lenovo Storage DE Series / DE2000H;
* Reg.ru domains and hosting services;
* VMware Replication / VMware vSphere Replication.

The templates use HTTP API, REST API, JavaScript preprocessing, dependent items, low-level discovery rules and triggers to automatically discover monitored objects and check their state.

## Template List

| Template                           | Description                                                                            |
| ---------------------------------- | -------------------------------------------------------------------------------------- |
| `Lenovo Storage DE Series by HTTP` | Monitoring Lenovo Storage DE Series, primarily Lenovo DE2000H, via controller HTTP API |
| `Reg.ru by HTTP`                   | Monitoring Reg.ru domains and hosting services via HTTP API                            |
| `VMware Replication`               | Monitoring VMware Replication / VMware vSphere Replication via REST API                |

## Lenovo Storage DE Series / DE2000H

This template is designed for monitoring Lenovo Storage DE Series systems, primarily Lenovo DE2000H, via the controller HTTP API.

Monitoring includes:

* general system information;
* storage system model, name, serial number and WWN;
* firmware component versions;
* system CPU utilization;
* total power consumption;
* controllers;
* batteries;
* power supplies;
* fans;
* thermal sensors;
* drives;
* SSD wear / health statistics;
* storage pools;
* volumes;
* Ethernet management interfaces;
* Fibre Channel interfaces;
* read and write metrics for drives, volumes and FC interfaces.

### Requirements

* Zabbix 6.4, 7.0 or later
* Network access from Zabbix Server or Zabbix Proxy to the storage management IP
* Access to Lenovo DE Series REST API
* Storage system account with read permissions
* Imported standard `ICMP Ping` template

### Macros

| Macro         | Description                                                     |
| ------------- | --------------------------------------------------------------- |
| `{$URL}`      | Storage controller API URL, for example `https://192.168.1.100` |
| `{$USERNAME}` | Username for HTTP Basic authentication                          |
| `{$PASSWORD}` | User password                                                   |

The template was prepared for Lenovo Storage DE2000H.

It may also work with other Lenovo DE Series systems if they use a compatible REST API and similar data structure. Compatibility with other models is not guaranteed and requires testing.

The template has been tested with Lenovo DE Series storage software versions 11.70, 11.80 and 11.90.

## Reg.ru by HTTP

This template is designed for monitoring Reg.ru domains and hosting services via HTTP API.

It retrieves the Reg.ru service list, automatically discovers domains and hosting services, creates items for creation date, expiration date and service state, and creates triggers for upcoming expiration.

Monitoring includes:

* automatic domain discovery;
* automatic hosting service discovery;
* domain creation date;
* domain expiration date;
* domain state;
* hosting service creation date;
* hosting service expiration date;
* hosting service state;
* alerts for expiration in 60, 30 and 7 days.

### Requirements

* Zabbix 7.4 or later
* Network access from Zabbix Server or Zabbix Proxy to `https://api.reg.ru`
* Reg.ru account
* Access to Reg.ru API
* Username and password/API password for API requests

### Macros

| Macro             | Description                          |
| ----------------- | ------------------------------------ |
| `{$USERNAME}`     | Reg.ru username                      |
| `{$API.PASSWORD}` | Reg.ru user password or API password |

### API Endpoint

```text
https://api.reg.ru/api/regru2/service/get_list
```

The following parameter is used for domains:

```text
servtype=domain
```

The following parameter is used for hosting services:

```text
servtype=srv_hosting_ispmgr
```

## VMware Replication

This template is designed for monitoring VMware Replication / VMware vSphere Replication via REST API.

It authenticates against the VMware Replication REST API, retrieves pairings, replications, VRM/vCenter information and replication servers, and then creates items and triggers using low-level discovery.

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

### Requirements

* Zabbix 7.0 or later
* Network access from Zabbix Server or Zabbix Proxy to the VMware Replication appliance
* Access to VMware Replication REST API
* VMware account with read permissions for replication information
* Configured VMware Replication pairings and virtual machine replications

### Macros

| Macro                | Description                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| `{$VRM.URL}`         | VMware Replication appliance URL, for example `https://vrm.example.local` |
| `{$VMWARE.USERNAME}` | VMware username                                                           |
| `{$VMWARE.PASSWORD}` | VMware user password                                                      |

### API Endpoints

```text
/api/rest/vr/v2/session
/api/rest/vr/v2/info/
/api/rest/vr/v2/pairings/
/api/rest/vr/v2/pairings/{pairing_id}/replications?extended_info=true
/api/rest/vr/v2/replication-servers/
```

## Installation

1. Download the required template file from this repository.
2. In Zabbix, open:

```text
Data collection → Templates → Import
```

3. Import the template file.
4. Create a host for the corresponding system or service.
5. Link the required template to the host.
6. Configure the required macros.
7. Make sure Zabbix Server or Zabbix Proxy has network access to the target system API.
8. Wait for the low-level discovery rules to run.

## Security Notes

Do not store real usernames, passwords, API keys or API passwords in the repository.

It is recommended to use dedicated monitoring accounts and grant them only the minimum required read permissions.

For production environments, test the templates on a separate host or test environment before using them widely.

## Compatibility

| Template                         | Tested / Target Zabbix Version |
| -------------------------------- | ------------------------------ |
| Lenovo Storage DE Series by HTTP | Zabbix 7.0 or later            |
| Reg.ru by HTTP                   | Zabbix 7.0 or later            |
| VMware Replication               | Zabbix 7.0 or later            |

Compatibility with other Zabbix versions is possible but should be tested separately.

## Project Status

The templates are in practical use and under further development.

Pull requests, issues and suggestions are welcome.
