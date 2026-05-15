# Lenovo Storage DE Series / DE2000H Zabbix Template

[English version](#english) | [Русская версия](#русская-версия)

---

## Русская версия

# Шаблон Zabbix для мониторинга Lenovo Storage DE2000H / DE Series

Этот репозиторий содержит шаблон Zabbix для мониторинга СХД Lenovo Storage DE Series, в первую очередь Lenovo DE2000H, через HTTP API контроллера.

Шаблон предназначен для Zabbix 7.0 и использует HTTP agent items, dependent items, low-level discovery rules и триггеры для контроля состояния основных компонентов системы хранения.

## Возможности

Шаблон собирает инвентаризационные, эксплуатационные и health-метрики СХД Lenovo DE Series.

Мониторинг включает:

- общую информацию о системе;
- модель, имя, серийный номер и WWN СХД;
- версии компонентов прошивки;
- загрузку CPU системы;
- общее энергопотребление;
- контроллеры;
- батареи;
- блоки питания;
- вентиляторы;
- температурные датчики;
- диски;
- SSD wear / health statistics;
- storage pools;
- volumes;
- Ethernet management interfaces;
- Fibre Channel interfaces;
- показатели чтения и записи по дискам, томам и FC-интерфейсам.

## Поддерживаемые компоненты

Шаблон использует LLD-обнаружение для следующих объектов:

- Batteries
- Controllers
- Fans
- Ethernet interfaces
- Fibre Channel interfaces
- Power supplies
- Drives
- Storage pools
- Thermal sensors
- Volumes

## Основные триггеры

Шаблон содержит триггеры для следующих событий:

- контроллер перезапущен;
- контроллер находится не в оптимальном состоянии;
- контроллер переведен в Service Mode;
- контроллер находится в Error Mode;
- батарея не в оптимальном состоянии;
- батарея проходит learn cycle;
- вентилятор не в оптимальном состоянии;
- блок питания не в оптимальном состоянии;
- диск offline;
- диск removed;
- диск не в optimal state;
- диск сообщает PFA reason / SSD End of Life;
- высокая температура диска;
- storage pool offline;
- storage pool не в complete state;
- RAID status storage pool не optimal;
- volume offline;
- volume state не optimal;
- смена текущего контроллера у volume;
- Ethernet interface down;
- FC interface down;
- отсутствие данных от обнаруженных компонентов в течение часа.

## Требования

- Zabbix 7.0
- Доступ Zabbix Server или Zabbix Proxy к management IP СХД
- Доступ к Lenovo DE Series REST API
- Учетная запись на СХД с правами чтения
- Импортированный стандартный шаблон `ICMP Ping`

## Макросы

После импорта шаблона необходимо задать макросы на уровне хоста или шаблона:

| Macro | Description |
|---|---|
| `{$URL}` | URL API контроллера СХД, например `https://192.168.1.100` |
| `{$USERNAME}` | Имя пользователя для HTTP Basic authentication |
| `{$PASSWORD}` | Пароль пользователя |

## Используемые API endpoints

Шаблон обращается к REST API Lenovo DE Series, включая следующие endpoints:

/devmgr/v2/storage-systems/1/about
/devmgr/v2/storage-systems/1/controllers
/devmgr/v2/storage-systems/1/live-statistics
/devmgr/v2/storage-systems/1/hardware-inventory
/devmgr/v2/storage-systems/1/drives
/devmgr/v2/storage-systems/1/drives/drive-health-history?all-history=false
/devmgr/v2/storage-systems/1/drive-statistics?usecache=false
/devmgr/v2/storage-systems/1/interfaces?interfaceType=fc
/devmgr/v2/storage-systems/1/interface-statistics?usecache=false
/devmgr/v2/storage-systems/1/storage-pools
/devmgr/v2/storage-systems/1/volumes
/devmgr/v2/storage-systems/1/volume-statistics?usecache=false
/devmgr/v2/storage-systems/1/diagnostic-data/power-input-data
/devmgr/v2/storage-systems/1/analysed-system-statistics
/devmgr/v2/firmware/embedded-firmware/1/versions

## Установка
Скачайте файл шаблона из репозитория.
В Zabbix откройте:
Data collection → Templates → Import
Импортируйте YAML/JSON-файл шаблона.
Создайте хост для СХД Lenovo DE Series.
Привяжите к хосту шаблон:
Lenovo Storage DE Series by HTTP
Укажите макросы {$URL}, {$USERNAME}, {$PASSWORD}.
Проверьте, что Zabbix может подключиться к API СХД по HTTPS/HTTP.
Дождитесь выполнения LLD discovery rules.
Особенности

Шаблон использует комбинированный подход:

HTTP agent items получают JSON-данные из API;
dependent items извлекают нужные значения через JSONPath;
JavaScript preprocessing используется для обработки некоторых вложенных структур;
LLD автоматически обнаруживает компоненты СХД;
value map Status Mapping преобразует числовые значения статусов в человекочитаемые состояния.
Совместимость

Шаблон был подготовлен для Lenovo Storage DE2000H.

Также он может работать с другими системами Lenovo DE Series, если они используют совместимый REST API и аналогичную структуру данных. Совместимость с другими моделями не гарантируется и требует проверки.

Известные ограничения
Шаблон использует Basic authentication.
URL API задается вручную через макрос {$URL}.
Некоторые проверки зависят от структуры JSON-ответов конкретной версии прошивки.
Для production-среды рекомендуется предварительно протестировать шаблон на отдельном хосте.
Пороговые значения температуры и логика отдельных триггеров могут потребовать адаптации под конкретную инфраструктуру.
Рекомендации по безопасности

Создайте отдельного пользователя СХД только для мониторинга и выдайте ему минимально необходимые права на чтение.

Не храните реальные пароли в репозитории.

Статус проекта

Текущая версия шаблона: 0.9.4

Шаблон находится в стадии практического использования и доработки. Pull requests, issues и предложения приветствуются.

## English
Zabbix Template for Lenovo Storage DE2000H / DE Series

This repository contains a Zabbix template for monitoring Lenovo Storage DE Series systems, primarily Lenovo DE2000H, through the controller HTTP API.

The template is designed for Zabbix 7.0 and uses HTTP agent items, dependent items, low-level discovery rules, value maps, preprocessing and triggers to monitor the health and performance of the storage system.

Features

The template collects inventory, operational and health metrics from Lenovo DE Series storage systems.

Monitoring includes:

general system information;
system model, name, serial number and WWN;
firmware and software component versions;
system CPU utilization;
total power consumption;
controllers;
batteries;
power supplies;
fans;
thermal sensors;
drives;
SSD wear and health statistics;
storage pools;
volumes;
Ethernet management interfaces;
Fibre Channel interfaces;
read and write statistics for drives, volumes and FC interfaces.
Discovered Components

The template uses low-level discovery for:

Batteries
Controllers
Fans
Ethernet interfaces
Fibre Channel interfaces
Power supplies
Drives
Storage pools
Thermal sensors
Volumes
Main Triggers

The template includes triggers for the following conditions:

controller restarted;
controller is not in optimal state;
controller switched to Service Mode;
controller switched to Error Mode;
battery is not optimal;
battery learn cycle;
fan is not optimal;
power supply is not optimal;
drive is offline;
drive is removed;
drive state is not optimal;
drive PFA reason / SSD End of Life;
high drive temperature;
storage pool is offline;
storage pool state is not complete;
storage pool RAID status is not optimal;
volume is offline;
volume state is not optimal;
volume current controller has changed;
Ethernet interface is down;
Fibre Channel interface is down;
no data from discovered components for one hour.
Requirements
Zabbix 7.0
Network access from Zabbix Server or Zabbix Proxy to the storage management IP
Lenovo DE Series REST API access
Read-only storage user account
Standard ICMP Ping template imported in Zabbix
Macros

After importing the template, configure the following macros on the host or template level:

Macro	Description
{$URL}	Storage controller API URL, for example https://192.168.1.100
{$USERNAME}	Username for HTTP Basic authentication
{$PASSWORD}	Password for HTTP Basic authentication

API Endpoints

The template uses Lenovo DE Series REST API endpoints such as:

/devmgr/v2/storage-systems/1/about
/devmgr/v2/storage-systems/1/controllers
/devmgr/v2/storage-systems/1/live-statistics
/devmgr/v2/storage-systems/1/hardware-inventory
/devmgr/v2/storage-systems/1/drives
/devmgr/v2/storage-systems/1/drives/drive-health-history?all-history=false
/devmgr/v2/storage-systems/1/drive-statistics?usecache=false
/devmgr/v2/storage-systems/1/interfaces?interfaceType=fc
/devmgr/v2/storage-systems/1/interface-statistics?usecache=false
/devmgr/v2/storage-systems/1/storage-pools
/devmgr/v2/storage-systems/1/volumes
/devmgr/v2/storage-systems/1/volume-statistics?usecache=false
/devmgr/v2/storage-systems/1/diagnostic-data/power-input-data
/devmgr/v2/storage-systems/1/analysed-system-statistics
/devmgr/v2/firmware/embedded-firmware/1/versions
Installation
Download the template file from this repository.
In Zabbix, open:
Data collection → Templates → Import
Import the YAML/JSON template file.
Create a host for your Lenovo DE Series storage system.
Link the following template to the host:
Lenovo Storage DE Series by HTTP
Configure the required macros: {$URL}, {$USERNAME}, {$PASSWORD}.
Make sure Zabbix can access the storage API over HTTPS/HTTP.
Wait for the low-level discovery rules to create items and triggers.
How It Works

The template uses the following approach:

HTTP agent items collect raw JSON data from the storage API;
dependent items extract values using JSONPath preprocessing;
JavaScript preprocessing is used for some nested interface data;
low-level discovery automatically creates items and triggers for storage components;
the Status Mapping value map converts numeric status values into readable states.
Compatibility

This template was prepared for Lenovo Storage DE2000H.

It may also work with other Lenovo DE Series systems if they provide a compatible REST API and similar JSON response structure. Compatibility with other models is not guaranteed and should be tested before production use.

Known Limitations
The template uses Basic authentication.
The API URL must be configured manually through the {$URL} macro.
Some checks depend on the JSON structure returned by a specific firmware version.
It is recommended to test the template on a separate host before using it in production.
Temperature thresholds and some trigger expressions may need adjustment for your environment.
Security Notes

Create a dedicated read-only monitoring user on the storage system.

Do not store real credentials in the repository.

Project Status

Current template version: 0.9.4

The template is in practical use and under active improvement. Pull requests, issues and suggestions are welcome. 