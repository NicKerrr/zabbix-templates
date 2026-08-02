# NanoKVM by SNMP

[English version](#english-version) | [Русская версия](#русская-версия)

---

## Русская версия

Шаблон Zabbix для мониторинга устройств NanoKVM через SNMP и ICMP.

Шаблон собирает доступность устройства, состояние SNMP, загрузку CPU, использование памяти, uptime, системную информацию, использование файловых систем и метрики сетевых интерфейсов.

## Возможности

* мониторинг доступности по ICMP;
* ICMP packet loss и response time;
* доступность SNMP agent;
* загрузка CPU;
* total, available, used, buffers, cached и shared memory;
* расчет memory utilization;
* system description;
* system name;
* system location;
* system object ID;
* hardware / network uptime;
* обнаружение перезагрузки;
* обнаружение файловых систем;
* total, used и used percentage для файловых систем;
* обнаружение сетевых интерфейсов;
* трафик интерфейсов в bps;
* скорость интерфейсов;
* operational status интерфейсов;
* входящие и исходящие ошибки интерфейсов.

## Требования

* Zabbix 7.0 или выше
* NanoKVM с версией image `1.4.0` или выше
* Включенный SNMP на NanoKVM
* Сетевой доступ от Zabbix Server или Zabbix Proxy к SNMP-порту NanoKVM
* Настроенный SNMP interface на хосте в Zabbix
* Настроенная SNMP community на NanoKVM

## Включение SNMP на NanoKVM

Подключитесь к NanoKVM по SSH.

Создайте конфигурационный файл SNMP:

```bash
cat > /etc/snmp/snmpd.conf <<'EOF'
rocommunity <public> <ip>

sysLocation <NanoKVM>
sysContact <admin>
dontLogTCPWrappersConnects yes
EOF
```

Замените:

* `<public>` на вашу SNMP community;
* `<ip>` на IP-адрес или подсеть, которой разрешен SNMP-доступ, например IP Zabbix Server или Zabbix Proxy;
* `<NanoKVM>` на расположение устройства;
* `<admin>` на контакт администратора.

Пример:

```bash
cat > /etc/snmp/snmpd.conf <<'EOF'
rocommunity nanokvm_monitor 192.168.1.10

sysLocation Server room
sysContact admin
dontLogTCPWrappersConnects yes
EOF
```

Создайте init-скрипт для запуска `snmpd`:

```bash
cat > /etc/init.d/S59snmpd <<'EOF'
#!/bin/sh

DAEMON="/usr/sbin/snmpd"
CONF="/etc/snmp/snmpd.conf"
ENDPOINT="udp:161"

case "$1" in
  start)
    echo "Starting snmpd..."
    $DAEMON -c $CONF $ENDPOINT
    ;;
  stop)
    echo "Stopping snmpd..."
    killall snmpd 2>/dev/null
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  status)
    ps | grep '[s]nmpd'
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0
EOF
```

Выдайте права на выполнение:

```bash
chmod +x /etc/init.d/S59snmpd
```

Запустите `snmpd`:

```bash
/etc/init.d/S59snmpd start
```

Проверьте статус:

```bash
/etc/init.d/S59snmpd status
```

Проверьте SNMP с Zabbix Server или Zabbix Proxy:

```bash
snmpwalk -v2c -c nanokvm_monitor 192.168.1.100 .1.3.6.1.2.1.1
```

Замените:

* `nanokvm_monitor` на вашу SNMP community;
* `192.168.1.100` на IP-адрес NanoKVM.

Если команда возвращает системную информацию, SNMP работает и шаблон можно привязывать к хосту в Zabbix.

Также можно проверить данные Host Resources MIB, которые используются в шаблоне:

```bash
snmpwalk -v2c -c nanokvm_monitor 192.168.1.100 .1.3.6.1.2.1.25.2.3.1
snmpwalk -v2c -c nanokvm_monitor 192.168.1.100 .1.3.6.1.2.1.2.2.1
```

## Установка

1. Импортируйте шаблон в Zabbix:

```text
Data collection → Templates → Import
```

2. Создайте хост для NanoKVM.
3. Добавьте SNMP interface с IP-адресом NanoKVM.
4. Укажите SNMP community или SNMPv3 credentials.
5. Привяжите шаблон:

```text
NanoKVM by SNMP
```

6. Проверьте, что ICMP и SNMP item’ы получают данные.
7. Дождитесь выполнения discovery rules для файловых систем и сетевых интерфейсов.

## Макросы

| Macro                           | Default | Description                                      |                                              |
| ------------------------------- | ------: | ------------------------------------------------ | -------------------------------------------- |
| `{$CPU.UTIL.CRIT}`              |    `90` | Порог загрузки CPU, %                            |                                              |
| `{$MEMORY.UTIL.MAX}`            |    `90` | Порог использования памяти, %                    |                                              |
| `{$ICMP_LOSS_WARN}`             |    `20` | Порог ICMP packet loss, %                        |                                              |
| `{$ICMP_RESPONSE_TIME_WARN}`    |  `0.15` | Порог ICMP response time, секунды                |                                              |
| `{$SNMP.TIMEOUT}`               |    `5m` | Интервал проверки доступности SNMP               |                                              |
| `{$IF.UTIL.MAX}`                |    `90` | Порог утилизации интерфейса, %                   |                                              |
| `{$IF.ERRORS.WARN}`             |     `2` | Порог ошибок интерфейса                          |                                              |
| `{$IFCONTROL}`                  |     `1` | Макрос контроля интерфейсов                      |                                              |
| `{$NET.IF.IFDESCR.MATCHES}`     |  `^.*$` | Фильтр включения интерфейсов в discovery         |                                              |
| `{$NET.IF.IFDESCR.NOT_MATCHES}` |   `^(lo | ip6+)`                                           | Фильтр исключения интерфейсов из discovery   |
| `{$NKVM.FS.DESCR.MATCHES}`      |    `^(/ | /boot)$`                                         | Фильтр включения файловых систем в discovery |
| `{$VFS.FS.PUSED.MAX.WARN}`      |    `80` | Warning-порог использования файловой системы, %  |                                              |
| `{$VFS.FS.PUSED.MAX.CRIT}`      |    `90` | Critical-порог использования файловой системы, % |                                              |

## Обнаружение

### Обнаружение файловых систем

Шаблон обнаруживает файловые системы из storage table Host Resources MIB.

По умолчанию обнаруживаются только:

```text
/
 /boot
```

Это поведение управляется макросом:

```text
{$NKVM.FS.DESCR.MATCHES}
```

Для каждой обнаруженной файловой системы создаются:

* allocation units;
* size blocks;
* used blocks;
* total space;
* used space;
* used space percentage.

Триггеры файловых систем:

* space is low;
* space is critically low.

### Обнаружение сетевых интерфейсов

Шаблон обнаруживает сетевые интерфейсы и фильтрует их по description.

По умолчанию исключаются loopback и IPv6-related interfaces:

```text
{$NET.IF.IFDESCR.NOT_MATCHES} = ^(lo|ip6+)
```

Для каждого обнаруженного интерфейса создаются:

* bits received;
* bits sent;
* interface speed;
* operational status;
* inbound errors;
* outbound errors.

Триггер сетевого интерфейса:

* link down.

## Используемые OID

Основные OID tree, которые использует шаблон:

```text
.1.3.6.1.2.1.1             # System information
.1.3.6.1.2.1.25.3.3.1.2    # CPU utilization
.1.3.6.1.2.1.25.2.3.1      # Memory and filesystem/storage information
.1.3.6.1.2.1.2.2.1         # Network interfaces
```

Примеры:

| OID                              | Description        |
| -------------------------------- | ------------------ |
| `.1.3.6.1.2.1.1.1.0`             | System description |
| `.1.3.6.1.2.1.1.2.0`             | System object ID   |
| `.1.3.6.1.2.1.1.3.0`             | System uptime      |
| `.1.3.6.1.2.1.1.5.0`             | System name        |
| `.1.3.6.1.2.1.1.6.0`             | System location    |
| `.1.3.6.1.2.1.25.3.3.1.2.196608` | CPU utilization    |
| `.1.3.6.1.2.1.25.2.3.1`          | Storage table      |
| `.1.3.6.1.2.1.2.2.1`             | Interface table    |

## Как это работает

Шаблон использует несколько master items с SNMP walk:

```text
system.info.walk
system.memory.walk
system.net.if.walk
```

Dependent items извлекают нужные значения через preprocessing `SNMP_WALK_VALUE`.

Low-level discovery rules используют `SNMP_WALK_TO_JSON` для обнаружения файловых систем и сетевых интерфейсов.

Memory utilization рассчитывается так:

```text
(total - available) / total * 100
```

Сетевой трафик рассчитывается из byte counters через `CHANGE_PER_SECOND` и умножается на `8`, чтобы получить значение в `bps`.

## Триггеры

Шаблон содержит триггеры для:

* недоступности по ICMP;
* высокого ICMP packet loss;
* высокого ICMP response time;
* отсутствия сбора данных по SNMP;
* высокой загрузки CPU;
* высокого использования памяти;
* изменения system name;
* перезагрузки устройства;
* малого свободного места на файловой системе;
* критически малого свободного места на файловой системе;
* link down на интерфейсе.

## Особенности

Item `NanoKVM: Available memory` использует значение size из Host Resources MIB для соответствующей записи available memory.

Item `NanoKVM: Used memory (including cache)` собирается отдельно и может включать cache в зависимости от того, как NanoKVM отдает данные памяти через SNMP.

Filesystem discovery по умолчанию ограничен `/` и `/boot`. Если нужно мониторить дополнительные mount points, переопределите `{$NKVM.FS.DESCR.MATCHES}`.

## Совместимость

Целевая версия:

```text
Zabbix 7.0+
```

Версия image NanoKVM:

```text
1.4.0+
```

Версия шаблона:

```text
0.7.1
```

Совместимость с другими версиями Zabbix или прошивками NanoKVM может требовать дополнительной проверки.

---

## English version

Zabbix template for monitoring NanoKVM devices via SNMP and ICMP.

The template collects device availability, SNMP status, CPU utilization, memory usage, uptime, system information, filesystem usage and network interface metrics.

## Features

* ICMP availability monitoring
* ICMP packet loss and response time
* SNMP agent availability
* CPU utilization
* Total, available, used, buffers, cached and shared memory
* Calculated memory utilization
* System description
* System name
* System location
* System object ID
* Hardware / network uptime
* Reboot detection
* Filesystem discovery
* Filesystem total, used and used percentage
* Network interface discovery
* Interface traffic in bps
* Interface speed
* Interface operational status
* Interface input/output errors

## Requirements

* Zabbix 7.0 or later
* NanoKVM image version `1.4.0` or later
* SNMP enabled on the NanoKVM device
* Network access from Zabbix Server or Zabbix Proxy to the NanoKVM SNMP port
* SNMP interface configured on the Zabbix host
* SNMP community configured on the NanoKVM device

## Enable SNMP on NanoKVM

Connect to the NanoKVM device via SSH.

Create the SNMP configuration file:

```bash
cat > /etc/snmp/snmpd.conf <<'EOF'
rocommunity <public> <ip>

sysLocation <NanoKVM>
sysContact <admin>
dontLogTCPWrappersConnects yes
EOF
```

Replace:

* `<public>` with your SNMP community;
* `<ip>` with the IP address or subnet allowed to query SNMP, for example Zabbix Server or Zabbix Proxy IP;
* `<NanoKVM>` with the device location;
* `<admin>` with the contact name or email.

Example:

```bash
cat > /etc/snmp/snmpd.conf <<'EOF'
rocommunity nanokvm_monitor 192.168.1.10

sysLocation Server room
sysContact admin
dontLogTCPWrappersConnects yes
EOF
```

Create the init script for `snmpd`:

```bash
cat > /etc/init.d/S59snmpd <<'EOF'
#!/bin/sh

DAEMON="/usr/sbin/snmpd"
CONF="/etc/snmp/snmpd.conf"
ENDPOINT="udp:161"

case "$1" in
  start)
    echo "Starting snmpd..."
    $DAEMON -c $CONF $ENDPOINT
    ;;
  stop)
    echo "Stopping snmpd..."
    killall snmpd 2>/dev/null
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  status)
    ps | grep '[s]nmpd'
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0
EOF
```

Make the script executable:

```bash
chmod +x /etc/init.d/S59snmpd
```

Start `snmpd`:

```bash
/etc/init.d/S59snmpd start
```

Check service status:

```bash
/etc/init.d/S59snmpd status
```

Check SNMP from Zabbix Server or Zabbix Proxy:

```bash
snmpwalk -v2c -c nanokvm_monitor 192.168.1.100 .1.3.6.1.2.1.1
```

Replace:

* `nanokvm_monitor` with your SNMP community;
* `192.168.1.100` with the NanoKVM IP address.

If the command returns system information, SNMP is working and the template can be linked to the host in Zabbix.

You can also check Host Resources MIB data used by the template:

```bash
snmpwalk -v2c -c nanokvm_monitor 192.168.1.100 .1.3.6.1.2.1.25.2.3.1
snmpwalk -v2c -c nanokvm_monitor 192.168.1.100 .1.3.6.1.2.1.2.2.1
```

## Installation

1. Import the template in Zabbix:

```text
Data collection → Templates → Import
```

2. Create a host for the NanoKVM device.
3. Add an SNMP interface with the NanoKVM IP address.
4. Configure SNMP community or SNMPv3 credentials.
5. Link the template:

```text
NanoKVM by SNMP
```

6. Check that ICMP and SNMP items receive data.
7. Wait for filesystem and network interface discovery rules to run.

## Macros

| Macro                           | Default | Description                            |                                     |
| ------------------------------- | ------: | -------------------------------------- | ----------------------------------- |
| `{$CPU.UTIL.CRIT}`              |    `90` | CPU utilization threshold, %           |                                     |
| `{$MEMORY.UTIL.MAX}`            |    `90` | Memory utilization threshold, %        |                                     |
| `{$ICMP_LOSS_WARN}`             |    `20` | ICMP packet loss threshold, %          |                                     |
| `{$ICMP_RESPONSE_TIME_WARN}`    |  `0.15` | ICMP response time threshold, seconds  |                                     |
| `{$SNMP.TIMEOUT}`               |    `5m` | SNMP availability check interval       |                                     |
| `{$IF.UTIL.MAX}`                |    `90` | Interface utilization threshold, %     |                                     |
| `{$IF.ERRORS.WARN}`             |     `2` | Interface error threshold              |                                     |
| `{$IFCONTROL}`                  |     `1` | Interface control macro                |                                     |
| `{$NET.IF.IFDESCR.MATCHES}`     |  `^.*$` | Interface discovery include filter     |                                     |
| `{$NET.IF.IFDESCR.NOT_MATCHES}` |   `^(lo | ip6+)`                                 | Interface discovery exclude filter  |
| `{$NKVM.FS.DESCR.MATCHES}`      |    `^(/ | /boot)$`                               | Filesystem discovery include filter |
| `{$VFS.FS.PUSED.MAX.WARN}`      |    `80` | Filesystem usage warning threshold, %  |                                     |
| `{$VFS.FS.PUSED.MAX.CRIT}`      |    `90` | Filesystem usage critical threshold, % |                                     |

## Discovery

### Filesystem discovery

The template discovers filesystems from Host Resources MIB storage data.

By default, only the following filesystems are discovered:

```text
/
 /boot
```

This behavior is controlled by:

```text
{$NKVM.FS.DESCR.MATCHES}
```

For each discovered filesystem, the template creates:

* allocation units;
* size blocks;
* used blocks;
* total space;
* used space;
* used space percentage.

Filesystem triggers:

* space is low;
* space is critically low.

### Network interface discovery

The template discovers network interfaces and filters them by interface description.

By default, it excludes loopback and IPv6-related interfaces:

```text
{$NET.IF.IFDESCR.NOT_MATCHES} = ^(lo|ip6+)
```

For each discovered interface, the template creates:

* bits received;
* bits sent;
* interface speed;
* operational status;
* inbound errors;
* outbound errors.

Network interface trigger:

* link down.

## Used OIDs

Main OID trees used by the template:

```text
.1.3.6.1.2.1.1             # System information
.1.3.6.1.2.1.25.3.3.1.2    # CPU utilization
.1.3.6.1.2.1.25.2.3.1      # Memory and filesystem/storage information
.1.3.6.1.2.1.2.2.1         # Network interfaces
```

Examples:

| OID                              | Description        |
| -------------------------------- | ------------------ |
| `.1.3.6.1.2.1.1.1.0`             | System description |
| `.1.3.6.1.2.1.1.2.0`             | System object ID   |
| `.1.3.6.1.2.1.1.3.0`             | System uptime      |
| `.1.3.6.1.2.1.1.5.0`             | System name        |
| `.1.3.6.1.2.1.1.6.0`             | System location    |
| `.1.3.6.1.2.1.25.3.3.1.2.196608` | CPU utilization    |
| `.1.3.6.1.2.1.25.2.3.1`          | Storage table      |
| `.1.3.6.1.2.1.2.2.1`             | Interface table    |

## How it works

The template uses several SNMP walk master items:

```text
system.info.walk
system.memory.walk
system.net.if.walk
```

Dependent items extract required values from these walks using `SNMP_WALK_VALUE`.

Low-level discovery rules use `SNMP_WALK_TO_JSON` to discover filesystems and network interfaces.

Memory utilization is calculated as:

```text
(total - available) / total * 100
```

Network traffic is calculated from byte counters using `CHANGE_PER_SECOND` and multiplied by `8` to show values in `bps`.

## Triggers

The template includes triggers for:

* unavailable by ICMP;
* high ICMP packet loss;
* high ICMP response time;
* no SNMP data collection;
* high CPU utilization;
* high memory utilization;
* system name changed;
* host restarted;
* filesystem space low;
* filesystem space critically low;
* interface link down.

## Notes

The memory item `NanoKVM: Available memory` uses the Host Resources MIB storage size value for the corresponding available-memory entry.

The item `NanoKVM: Used memory (including cache)` is collected separately and may include cache depending on how NanoKVM exposes memory data via SNMP.

Filesystem discovery is limited by default to `/` and `/boot`. Override `{$NKVM.FS.DESCR.MATCHES}` if you need to monitor additional mount points.

## Compatibility

Tested / target version:

```text
Zabbix 7.0+
```

NanoKVM image version:

```text
1.4.0+
```

Template version:

```text
0.7.1
```

Compatibility with other Zabbix versions or NanoKVM firmware versions may require additional testing.
