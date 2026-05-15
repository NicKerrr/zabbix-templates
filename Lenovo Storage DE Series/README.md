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

## Требования

- Zabbix 6.4, 7.0 и выше
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


Данный шаблон подготовлен для системы хранения данных Lenovo Storage DE2000H.

Он также может работать с другими системами Lenovo серии DE, если они используют совместимый REST API и аналогичную структуру данных. Совместимость с другими моделями не гарантируется и требует тестирования.

Шаблон был протестирован с версиями программного обеспечения для систем хранения данных Lenovo серии DE: 11.70, 11.80 и 11.90.

Шаблон находится в процессе практического использования и продолжает дорабатываться. Приветствуются запросы на добавление изменений, сообщения об ошибках и предложения.

## English version


# Zabbix Template for Lenovo Storage DE2000H / DE Series

This repository contains a Zabbix template for monitoring Lenovo Storage DE Series storage systems, primarily Lenovo DE2000H, via the controller HTTP API.

The template is designed for Zabbix 7.0 and may also work with Zabbix 6.4, 7.0 and later versions. It uses HTTP agent items, dependent items, low-level discovery rules and triggers to monitor the state of the main storage system components.

## Features

The template collects inventory, operational and health metrics from Lenovo DE Series storage systems.

Monitoring includes:

- general system information;
- storage system model, name, serial number and WWN;
- firmware component versions;
- system CPU utilization;
- total power consumption;
- controllers;
- batteries;
- power supplies;
- fans;
- thermal sensors;
- drives;
- SSD wear / health statistics;
- storage pools;
- volumes;
- Ethernet management interfaces;
- Fibre Channel interfaces;
- read and write metrics for drives, volumes and FC interfaces.

## Requirements

- Zabbix 6.4, 7.0 or later
- Network access from Zabbix Server or Zabbix Proxy to the storage management IP
- Access to the Lenovo DE Series REST API
- Storage system account with read permissions
- Imported standard `ICMP Ping` template

## Macros

After importing the template, define the following macros at the host or template level:

| Macro | Description |
|---|---|
| `{$URL}` | Storage controller API URL, for example `https://192.168.1.100` |
| `{$USERNAME}` | Username for HTTP Basic authentication |
| `{$PASSWORD}` | User password |

The template was prepared for Lenovo Storage DE2000H.

It may also work with other Lenovo DE Series systems if they use a compatible REST API and similar data structure. Compatibility with other models is not guaranteed and requires testing.

The template has been tested with Lenovo DE Series storage software versions 11.70, 11.80 and 11.90.

The template is in practical use and under further development. Pull requests, issues and suggestions are welcome.