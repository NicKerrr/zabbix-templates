# Zabbix Templates

[English version](#english-version) | [Русская версия](#русская-версия)

---

## Русская версия

Пользовательские шаблоны Zabbix для мониторинга инфраструктурных сервисов, оборудования и сетевых устройств.

## Шаблоны

| Template                           | Описание                                                                                                                                                                                                       | Zabbix     |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `Lenovo Storage DE Series by HTTP` | Мониторинг Lenovo Storage DE Series / DE2000H через HTTP API: контроллеры, диски, тома, pools, блоки питания, вентиляторы, батареи, температурные датчики, Ethernet- и Fibre Channel-интерфейсы.               | 6.4 / 7.0+ |
| `Reg.ru by HTTP`                   | Мониторинг доменов и услуг хостинга Reg.ru через HTTP API. Обнаруживает домены и хостинги, собирает даты создания/окончания, состояние услуги и создает уведомления об окончании срока действия.               | 7.0+       |
| `VMware Replication`               | Мониторинг VMware Replication / vSphere Replication через REST API. Обнаруживает pairings, репликации ВМ и replication servers, контролирует статус репликации, метрики синхронизации и состояние VRM/vCenter. | 7.0+       |
| `LibreHardwareMonitor by HTTP`     | Мониторинг аппаратных датчиков Windows-хоста через HTTP API LibreHardwareMonitor: температуры CPU, GPU, NVMe, HDD/SSD и скорости вентиляторов.                                                                 | 7.0+       |
| `NVR Template`                     | Мониторинг NVR через внешний Python-скрипт и CGI API. Собирает информацию о системе, обнаруживает активные каналы и диски, контролирует статус каналов, состояние дисков и диапазон записи.                    | 7.0+       |
| `KeeneticOS by SNMP`               | Мониторинг роутеров Keenetic / KeeneticOS через SNMP: ICMP/SNMP-доступность, системная информация, uptime, CPU, память и сетевые интерфейсы.                                                                   | 7.0+       |
| `NanoKVM by SNMP`                  | Мониторинг устройств NanoKVM через SNMP и ICMP: доступность, CPU, память, uptime, файловые системы, системная информация и сетевые интерфейсы.                                                                 | 7.0+       |

## Требования

Разные шаблоны используют разные способы сбора данных:

| Template                 | Способ сбора                     | Примечание                                                         |
| ------------------------ | -------------------------------- | ------------------------------------------------------------------ |
| Lenovo Storage DE Series | HTTP API                         | Требуется доступ к API контроллера СХД                             |
| Reg.ru                   | HTTP API                         | Требуются учетные данные Reg.ru API                                |
| VMware Replication       | REST API                         | Требуется доступ к VMware Replication REST API                     |
| LibreHardwareMonitor     | HTTP API                         | Требуется веб-сервер LibreHardwareMonitor и аутентификация         |
| NVR                      | External Python script + CGI API | Требуется установка external script и Python-зависимостей          |
| KeeneticOS               | SNMP                             | Требуется включенный SNMP на роутере                               |
| NanoKVM                  | SNMP                             | Требуется NanoKVM image `1.4.0+` и ручное включение SNMP через SSH |

Для шаблонов, которые используют внешние API, убедитесь, что Zabbix Server или Zabbix Proxy имеет сетевой доступ к целевому устройству или сервису.

Для шаблона NVR необходимо поместить Python-скрипт в каталог external scripts Zabbix и установить необходимые Python-зависимости.

Для шаблона KeeneticOS необходимо включить SNMP на роутере. Шаблон использует числовые OID, но для диагностики через `snmpwalk` и `snmptranslate` рекомендуется использовать `SNMPv2-MIB.mib` и `UCD-SNMP-MIB.mib`.

Для шаблона NanoKVM требуется версия image `1.4.0` или выше. SNMP необходимо включить на устройстве вручную через SSH, создав `snmpd.conf` и init-скрипт для запуска `snmpd`. Перед привязкой шаблона проверьте SNMP с Zabbix Server или Zabbix Proxy.

## Совместимость

Шаблоны подготовлены и тестировались на разных версиях Zabbix. Перед импортом проверьте документацию конкретного шаблона.

Работа на других версиях Zabbix или других версиях прошивок устройств возможна, но может требовать дополнительного тестирования.

## Статус

Шаблоны используются на практике и продолжают дорабатываться.

Issues, pull requests и предложения приветствуются.

---

## English version

Custom Zabbix templates for monitoring infrastructure services, hardware and network devices.

## Templates

| Template                           | Description                                                                                                                                                                                       | Zabbix     |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `Lenovo Storage DE Series by HTTP` | Monitoring Lenovo Storage DE Series / DE2000H via HTTP API: controllers, drives, volumes, pools, power supplies, fans, batteries, temperature sensors, Ethernet and Fibre Channel interfaces.     | 6.4 / 7.0+ |
| `Reg.ru by HTTP`                   | Monitoring Reg.ru domains and hosting services via HTTP API. Discovers domains and hosting services, collects creation/expiration dates and service state, and creates expiration alerts.         | 7.0+       |
| `VMware Replication`               | Monitoring VMware Replication / vSphere Replication via REST API. Discovers pairings, VM replications and replication servers, monitors replication status, sync metrics and VRM/vCenter state.   | 7.0+       |
| `LibreHardwareMonitor by HTTP`     | Monitoring Windows hardware sensors via LibreHardwareMonitor HTTP API: CPU, GPU, NVMe, HDD/SSD temperatures and fan speeds.                                                                       | 7.0+       |
| `NVR Template`                     | Monitoring NVR devices via external Python script and CGI API. Collects system information, discovers active channels and drives, monitors channel status, drive status and recording time range. | 7.0+       |
| `KeeneticOS by SNMP`               | Monitoring Keenetic / KeeneticOS routers via SNMP: ICMP/SNMP availability, system information, uptime, CPU, memory and network interfaces.                                                        | 7.0+       |
| `NanoKVM by SNMP`                  | Monitoring NanoKVM devices via SNMP and ICMP: availability, CPU, memory, uptime, filesystem usage, system information and network interfaces.                                                     | 7.0+       |

## Requirements

Different templates use different collection methods:

| Template                 | Collection method                | Notes                                                             |
| ------------------------ | -------------------------------- | ----------------------------------------------------------------- |
| Lenovo Storage DE Series | HTTP API                         | Requires access to the storage controller API                     |
| Reg.ru                   | HTTP API                         | Requires Reg.ru API credentials                                   |
| VMware Replication       | REST API                         | Requires access to VMware Replication REST API                    |
| LibreHardwareMonitor     | HTTP API                         | Requires LibreHardwareMonitor web server and authentication       |
| NVR                      | External Python script + CGI API | Requires external script installation and Python dependencies     |
| KeeneticOS               | SNMP                             | Requires SNMP enabled on the router                               |
| NanoKVM                  | SNMP                             | Requires NanoKVM image `1.4.0+` and SNMP enabled manually via SSH |

For templates that use external APIs, make sure Zabbix Server or Zabbix Proxy has network access to the target device or service.

For the NVR template, place the Python script in the Zabbix external scripts directory and install the required Python dependencies.

For the KeeneticOS template, enable SNMP on the router. The template uses numeric OIDs, but `SNMPv2-MIB.mib` and `UCD-SNMP-MIB.mib` are recommended for troubleshooting with `snmpwalk` and `snmptranslate`.

For the NanoKVM template, use NanoKVM image version `1.4.0` or later. SNMP must be enabled on the device manually via SSH by creating `snmpd.conf` and an init script for `snmpd`. Check SNMP from Zabbix Server or Zabbix Proxy before linking the template.

## Compatibility

The templates were prepared and tested for different Zabbix versions. Check the documentation of each template before import.

Compatibility with other Zabbix versions or device firmware versions may require additional testing.

## Status

The templates are in practical use and under development.

Issues, pull requests and suggestions are welcome.
