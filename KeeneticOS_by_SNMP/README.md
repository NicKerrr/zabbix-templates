# KeeneticOS Zabbix Template

[English version](#english-version) | [Русская версия](#русская-версия)

---

## Русская версия

# Шаблон Zabbix для мониторинга KeeneticOS по SNMP

Этот репозиторий содержит шаблон Zabbix для мониторинга роутеров Keenetic / KeeneticOS через SNMP.

Шаблон собирает базовую информацию об устройстве, состояние доступности, загрузку CPU, load average, использование памяти и статистику сетевых интерфейсов. Для сетевых интерфейсов используется low-level discovery.

Шаблон предназначен для мониторинга домашних, офисных и инфраструктурных роутеров Keenetic, где включен SNMP-доступ.

## Возможности

Мониторинг включает:

* доступность устройства по ICMP;
* потери ICMP-пакетов;
* время ответа ICMP;
* доступность SNMP agent;
* системное имя;
* системное описание;
* системную локацию;
* производителя;
* модель устройства;
* серийный номер;
* CID / UUID устройства;
* uptime устройства;
* изменение имени устройства;
* изменение системного описания;
* перезагрузку устройства;
* CPU load average за 1, 5 и 15 минут;
* raw CPU counters;
* расчет CPU utilization;
* total memory;
* available memory;
* shared memory;
* buffer memory;
* cached memory;
* расчет memory utilization;
* автоматическое обнаружение сетевых интерфейсов;
* входящий и исходящий трафик интерфейсов;
* скорость интерфейсов;
* administrative status интерфейсов;
* operational status интерфейсов;
* ошибки и discards на интерфейсах.

## Триггеры

Шаблон содержит триггеры для следующих событий:

* устройство недоступно по ICMP;
* высокий packet loss;
* высокое время ответа ICMP;
* отсутствует сбор данных по SNMP;
* устройство было перезагружено;
* изменилось системное имя;
* изменилось системное описание;
* высокая загрузка CPU;
* высокое использование памяти;
* интерфейс находится в состоянии Link down;
* высокая утилизация интерфейса;
* высокий уровень ошибок на интерфейсе.

Для части триггеров настроены зависимости, чтобы уменьшить количество дублирующихся уведомлений. Например, проблемы ICMP loss и SNMP collection зависят от доступности устройства по ICMP.

## Требования

* Zabbix 7.0 или выше
* Роутер Keenetic / KeeneticOS с включенным SNMP
* Сетевой доступ от Zabbix Server или Zabbix Proxy к SNMP-порту устройства
* Настроенный SNMP interface на хосте в Zabbix
* SNMP community или SNMPv3 credentials, в зависимости от настроек устройства
* MIB-файлы для удобной диагностики:

  * `UCD-SNMP-MIB.mib`
  * `SNMPv2-MIB.mib`

Важно: шаблон использует числовые OID, поэтому MIB-файлы не обязательны для импорта шаблона. Они нужны для удобной диагностики, проверки OID через `snmpwalk` / `snmptranslate` и ручной отладки SNMP.

## Настройка SNMP на Keenetic

Включите SNMP (https://support.keenetic.com/hero/kn-1012/en/51149-setting-up-snmp-server.html) на роутере Keenetic и разрешите доступ с IP-адреса Zabbix Server или Zabbix Proxy.

После настройки проверьте SNMP с Zabbix Server или Zabbix Proxy:

```bash id="kx0u5d"
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.2.1.1
```

Где:

* `public` — SNMP community;
* `192.168.1.1` — IP-адрес Keenetic.

Если команда возвращает системную информацию, SNMP-доступ работает.

Также можно проверить OID памяти и CPU, которые используются в шаблоне:

```bash id="l3de8r"
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.4.1.2021.4
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.4.1.2021.10
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.4.1.2021.11
```

## MIB-файлы

Шаблон основан на OID из следующих MIB:

```text id="ci8y7d"
SNMPv2-MIB.mib
UCD-SNMP-MIB.mib
```

`SNMPv2-MIB.mib` используется для системной информации, например `sysDescr`, `sysName`, `sysLocation`, `sysUpTime`.

`UCD-SNMP-MIB.mib` используется для метрик CPU, load average и памяти, например `memTotalReal`, `memAvailReal`, `laLoad`, `ssCpuRawUser`, `ssCpuRawSystem`, `ssCpuRawIdle`.

### Куда класть MIB-файлы

На Linux-сервере с Zabbix MIB-файлы обычно размещаются в каталоге:

```text id="gceiit"
/usr/share/snmp/mibs/
```

Скопируйте MIB-файлы:

```bash id="du306o"
sudo cp UCD-SNMP-MIB.mib /usr/share/snmp/mibs/
sudo cp SNMPv2-MIB.mib /usr/share/snmp/mibs/
```

Проверьте, что файлы появились в каталоге:

```bash id="eawigr"
ls -l /usr/share/snmp/mibs/ | grep -E 'UCD-SNMP-MIB|SNMPv2-MIB'
```

Проверьте, что MIB-файлы читаются корректно:

```bash id="k65wiv"
snmptranslate -On UCD-SNMP-MIB::memAvailReal.0
snmptranslate -On SNMPv2-MIB::sysDescr.0
```

Ожидаемые OID:

```text id="s41jk8"
UCD-SNMP-MIB::memAvailReal.0 -> .1.3.6.1.4.1.2021.4.6.0
SNMPv2-MIB::sysDescr.0      -> .1.3.6.1.2.1.1.1.0
```

Если команда `snmptranslate` не находит MIB, проверьте конфигурацию Net-SNMP:

```bash id="yp5f5x"
cat /etc/snmp/snmp.conf
```

В некоторых системах загрузка MIB может быть отключена строкой:

```text id="gl3as9"
mibs :
```

Для ручной проверки можно временно указать MIB через переменную окружения:

```bash id="jacyki"
MIBS=+SNMPv2-MIB:+UCD-SNMP-MIB snmptranslate -On UCD-SNMP-MIB::memAvailReal.0
```

### Перезапуск Zabbix

Если Zabbix установлен как systemd-сервис, после добавления MIB-файлов можно перезапустить Zabbix Server:

```bash id="bt5scm"
sudo systemctl restart zabbix-server
```

или Zabbix Proxy:

```bash id="zxzwth"
sudo systemctl restart zabbix-proxy
```

Для самого шаблона это обычно не требуется, так как используются числовые OID. Перезапуск полезен, если вы используете MIB-имена в ручной диагностике или в других SNMP item’ах.

## Импорт шаблона

1. Скачайте файл шаблона из репозитория.
2. В Zabbix откройте:

```text id="nveqnz"
Data collection → Templates → Import
```

3. Импортируйте файл шаблона.
4. Создайте хост для устройства Keenetic.
5. Добавьте SNMP interface с IP-адресом роутера.
6. Укажите SNMP community или SNMPv3 credentials.
7. Привяжите шаблон:

```text id="vixwpb"
KeeneticOS by SNMP
```

8. Проверьте получение данных по item’ам ICMP и SNMP.
9. Дождитесь выполнения discovery rule для сетевых интерфейсов.

## Макросы

Шаблон содержит следующие макросы:

| Macro                                 |                    Default | Description                                             |
| ------------------------------------- | -------------------------: | ------------------------------------------------------- |
| `{$CPU.UTIL.MAX}`                     |                       `90` | Порог высокой загрузки CPU, %                           |
| `{$MEMORY.UTIL.MAX}`                  |                       `90` | Порог высокого использования памяти, %                  |
| `{$ICMP_LOSS_WARN}`                   |                       `20` | Порог packet loss, %                                    |
| `{$ICMP_RESPONSE_TIME_WARN}`          |                     `0.15` | Порог времени ответа ICMP, секунды                      |
| `{$SNMP.TIMEOUT}`                     |                       `5m` | Интервал, за который проверяется доступность SNMP-сбора |
| `{$IF.UTIL.MAX}`                      |         не задан в шаблоне | Порог утилизации интерфейса, %                          |
| `{$IF.ERRORS.WARN}`                   |                        `2` | Порог ошибок на интерфейсе                              |
| `{$NET.IF.IFADMINSTATUS.MATCHES}`     |                      `^.*` | Фильтр discovery по admin status                        |
| `{$NET.IF.IFADMINSTATUS.NOT_MATCHES}` |                      `^2$` | Исключение интерфейсов с admin status down              |
| `{$NET.IF.IFALIAS.MATCHES}`           |                       `.*` | Фильтр discovery по alias                               |
| `{$NET.IF.IFALIAS.NOT_MATCHES}`       |         `CHANGE_IF_NEEDED` | Исключение по alias                                     |
| `{$NET.IF.IFDESCR.MATCHES}`           |                       `.*` | Фильтр discovery по description                         |
| `{$NET.IF.IFDESCR.NOT_MATCHES}`       |         `CHANGE_IF_NEEDED` | Исключение по description                               |
| `{$NET.IF.IFNAME.MATCHES}`            |                     `^.*$` | Фильтр discovery по имени интерфейса                    |
| `{$NET.IF.IFNAME.NOT_MATCHES}`        | loopback/docker/veth regex | Исключение служебных интерфейсов                        |
| `{$NET.IF.IFOPERSTATUS.MATCHES}`      |                     `^.*$` | Фильтр discovery по oper status                         |
| `{$NET.IF.IFOPERSTATUS.NOT_MATCHES}`  |                      `^6$` | Исключение notPresent интерфейсов                       |

Пример добавления порога утилизации интерфейсов на уровне хоста:

```text id="xzwy03"
{$IF.UTIL.MAX} = 90
```

Также можно задать контекстный макрос для конкретного интерфейса:

```text id="4pr5ki"
{$IF.UTIL.MAX:"GigabitEthernet0"} = 80
```

## Используемые OID

Шаблон использует стандартные SNMP OID, а также OID из `SNMPv2-MIB.mib` и `UCD-SNMP-MIB.mib`.

### System

```text id="s5vyiw"
.1.3.6.1.2.1.1
```

Используется для системного имени, описания, location и uptime.

Примеры:

| OID                  | Description        |
| -------------------- | ------------------ |
| `.1.3.6.1.2.1.1.1.0` | System Description |
| `.1.3.6.1.2.1.1.3.0` | System Uptime      |
| `.1.3.6.1.2.1.1.5.0` | System Name        |
| `.1.3.6.1.2.1.1.6.0` | System Location    |

### Hardware inventory

```text id="rmet65"
.1.3.6.1.2.1.47.1.1.1.1
```

Используется для производителя, модели, серийного номера и CID/UUID.

Примеры:

| OID                          | Description   |
| ---------------------------- | ------------- |
| `.1.3.6.1.2.1.47.1.1.1.1.11` | Serial Number |
| `.1.3.6.1.2.1.47.1.1.1.1.12` | Manufacturer  |
| `.1.3.6.1.2.1.47.1.1.1.1.13` | Model         |
| `.1.3.6.1.2.1.47.1.1.1.1.19` | CID / UUID    |

### Memory

```text id="dg6mjr"
.1.3.6.1.4.1.2021.4
```

Используется для total, available, shared, buffer и cached memory.

Примеры:

| OID                        | Description      |
| -------------------------- | ---------------- |
| `.1.3.6.1.4.1.2021.4.5.0`  | Total memory     |
| `.1.3.6.1.4.1.2021.4.6.0`  | Available memory |
| `.1.3.6.1.4.1.2021.4.13.0` | Shared memory    |
| `.1.3.6.1.4.1.2021.4.14.0` | Buffer memory    |
| `.1.3.6.1.4.1.2021.4.15.0` | Cached memory    |

### CPU load average

```text id="w3ihwm"
.1.3.6.1.4.1.2021.10
```

Используется для load average за 1, 5 и 15 минут.

Примеры:

| OID                          | Description      |
| ---------------------------- | ---------------- |
| `.1.3.6.1.4.1.2021.10.1.3.1` | Load average 1m  |
| `.1.3.6.1.4.1.2021.10.1.3.2` | Load average 5m  |
| `.1.3.6.1.4.1.2021.10.1.3.3` | Load average 15m |

### CPU raw counters

```text id="65r0ul"
.1.3.6.1.4.1.2021.11
```

Используется для расчета CPU utilization через raw counters user, nice, system и idle.

Примеры:

| OID                         | Description    |
| --------------------------- | -------------- |
| `.1.3.6.1.4.1.2021.11.50.0` | CPU raw user   |
| `.1.3.6.1.4.1.2021.11.51.0` | CPU raw nice   |
| `.1.3.6.1.4.1.2021.11.52.0` | CPU raw system |
| `.1.3.6.1.4.1.2021.11.53.0` | CPU raw idle   |

### Network interfaces

```text id="y6mvjn"
.1.3.6.1.2.1.2.2
.1.3.6.1.2.1.31.1.1.1
```

Используется для обнаружения интерфейсов, статусов, скорости, счетчиков трафика, ошибок и discarded packets.

## Как это работает

Шаблон использует несколько master items с `SNMP walk`, например:

```text id="w7zaj2"
keenetic.system.walk
keenetic.hardware.walk
keenetic.memory.walk
keenetic.cpu.load.walk
keenetic.cpu.walk
```

Dependent items извлекают конкретные значения из результатов walk с помощью preprocessing `SNMP_WALK_VALUE`.

Такой подход уменьшает количество отдельных SNMP-запросов к устройству и позволяет получать несколько метрик из одного SNMP walk.

CPU utilization рассчитывается calculated item’ом на основе изменения raw counters:

```text id="tcupkt"
user + nice + system / user + nice + system + idle
```

Memory utilization рассчитывается по формуле:

```text id="n8snqj"
100 - available / total * 100
```

## Network interfaces discovery

Шаблон автоматически обнаруживает сетевые интерфейсы через SNMP LLD.

Для каждого интерфейса создаются элементы:

* inbound traffic;
* outbound traffic;
* inbound errors;
* outbound errors;
* inbound discards;
* outbound discards;
* speed;
* admin status;
* operational status.

Discovery можно настроить через макросы фильтрации:

```text id="og7hkr"
{$NET.IF.IFNAME.MATCHES}
{$NET.IF.IFNAME.NOT_MATCHES}
{$NET.IF.IFALIAS.MATCHES}
{$NET.IF.IFALIAS.NOT_MATCHES}
{$NET.IF.IFDESCR.MATCHES}
{$NET.IF.IFDESCR.NOT_MATCHES}
{$NET.IF.IFADMINSTATUS.MATCHES}
{$NET.IF.IFADMINSTATUS.NOT_MATCHES}
{$NET.IF.IFOPERSTATUS.MATCHES}
{$NET.IF.IFOPERSTATUS.NOT_MATCHES}
```

## Value maps

### Interface admin status

| Value | Status  |
| ----- | ------- |
| `1`   | up      |
| `2`   | down    |
| `3`   | testing |

### Interface operational status

| Value | Status         |
| ----- | -------------- |
| `1`   | up             |
| `2`   | down           |
| `3`   | testing        |
| `4`   | unknown        |
| `5`   | dormant        |
| `6`   | notPresent     |
| `7`   | lowerLayerDown |

### zabbix.host.available

| Value | Status        |
| ----- | ------------- |
| `0`   | not available |
| `1`   | available     |
| `2`   | unknown       |

## Особенности

На разных версиях KeeneticOS набор доступных SNMP OID может отличаться. Если часть item’ов не получает данные, проверьте соответствующие OID через `snmpwalk`.

Некоторые интерфейсы могут быть скрыты фильтрами discovery. При необходимости измените макросы `MATCHES` / `NOT_MATCHES`.

Макрос `{$IF.UTIL.MAX}` используется в триггере высокой утилизации интерфейса, но может быть не задан в шаблоне. Рекомендуется задать его на уровне хоста или шаблона.

## Совместимость

Шаблон подготовлен для Zabbix 7.0.

Работа на других версиях Zabbix возможна, но требует отдельной проверки.

Совместимость зависит от версии KeeneticOS и набора SNMP OID, которые отдает устройство.

## Статус проекта

Текущая версия шаблона: `0.8.2`

Шаблон находится в процессе практического использования и доработки. Pull requests, issues и предложения приветствуются.

---

## English version

# Zabbix Template for KeeneticOS SNMP Monitoring

This repository contains a Zabbix template for monitoring Keenetic / KeeneticOS routers via SNMP.

The template collects basic device information, availability state, CPU load, load average, memory usage and network interface statistics. Network interfaces are discovered using low-level discovery.

The template is intended for monitoring home, office and infrastructure Keenetic routers with SNMP enabled.

## Features

Monitoring includes:

* device availability using ICMP;
* ICMP packet loss;
* ICMP response time;
* SNMP agent availability;
* system name;
* system description;
* system location;
* manufacturer;
* device model;
* serial number;
* CID / UUID;
* device uptime;
* system name change detection;
* system description change detection;
* device reboot detection;
* CPU load average for 1, 5 and 15 minutes;
* raw CPU counters;
* calculated CPU utilization;
* total memory;
* available memory;
* shared memory;
* buffer memory;
* cached memory;
* calculated memory utilization;
* automatic network interface discovery;
* inbound and outbound interface traffic;
* interface speed;
* administrative interface status;
* operational interface status;
* interface errors and discards.

## Triggers

The template includes triggers for the following events:

* device is unavailable by ICMP;
* high ICMP packet loss;
* high ICMP response time;
* no SNMP data collection;
* device has been restarted;
* system name has changed;
* system description has changed;
* high CPU utilization;
* high memory utilization;
* interface link down;
* high interface bandwidth usage;
* high interface error rate.

Some triggers include dependencies to reduce duplicate alerts. For example, ICMP loss and SNMP collection problems depend on ICMP availability.

## Requirements

* Zabbix 7.0 or later
* Keenetic / KeeneticOS router with SNMP enabled
* Network access from Zabbix Server or Zabbix Proxy to the device SNMP port
* SNMP interface configured on the Zabbix host
* SNMP community or SNMPv3 credentials, depending on device settings
* MIB files for easier troubleshooting:

  * `UCD-SNMP-MIB.mib`
  * `SNMPv2-MIB.mib`

Important: the template uses numeric OIDs, so MIB files are not required for importing the template. They are mainly useful for troubleshooting, OID checks with `snmpwalk` / `snmptranslate` and manual SNMP debugging.

## Keenetic SNMP Setup

Enable SNMP (https://support.keenetic.com/hero/kn-1012/en/51149-setting-up-snmp-server.html) on the Keenetic router and allow access from the Zabbix Server or Zabbix Proxy IP address.

After configuration, check SNMP from Zabbix Server or Zabbix Proxy:

```bash id="m1e8s0"
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.2.1.1
```

Where:

* `public` is the SNMP community;
* `192.168.1.1` is the Keenetic IP address.

If the command returns system information, SNMP access is working.

You can also check memory and CPU OIDs used by the template:

```bash id="jmypqn"
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.4.1.2021.4
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.4.1.2021.10
snmpwalk -v2c -c public 192.168.1.1 .1.3.6.1.4.1.2021.11
```

## MIB Files

The template is based on OIDs from the following MIBs:

```text id="w2438s"
SNMPv2-MIB.mib
UCD-SNMP-MIB.mib
```

`SNMPv2-MIB.mib` is used for system information such as `sysDescr`, `sysName`, `sysLocation`, `sysUpTime`.

`UCD-SNMP-MIB.mib` is used for CPU, load average and memory metrics such as `memTotalReal`, `memAvailReal`, `laLoad`, `ssCpuRawUser`, `ssCpuRawSystem`, `ssCpuRawIdle`.

### Where to Place MIB Files

On a Linux server with Zabbix, MIB files are usually stored in:

```text id="xls99h"
/usr/share/snmp/mibs/
```

Copy the MIB files:

```bash id="8f69h8"
sudo cp UCD-SNMP-MIB.mib /usr/share/snmp/mibs/
sudo cp SNMPv2-MIB.mib /usr/share/snmp/mibs/
```

Check that the files are present:

```bash id="dauuw8"
ls -l /usr/share/snmp/mibs/ | grep -E 'UCD-SNMP-MIB|SNMPv2-MIB'
```

Verify that the MIB files are loaded correctly:

```bash id="np9hlk"
snmptranslate -On UCD-SNMP-MIB::memAvailReal.0
snmptranslate -On SNMPv2-MIB::sysDescr.0
```

Expected OIDs:

```text id="s10jnz"
UCD-SNMP-MIB::memAvailReal.0 -> .1.3.6.1.4.1.2021.4.6.0
SNMPv2-MIB::sysDescr.0      -> .1.3.6.1.2.1.1.1.0
```

If `snmptranslate` cannot find the MIB, check the Net-SNMP configuration:

```bash id="02r10u"
cat /etc/snmp/snmp.conf
```

On some systems, MIB loading can be disabled by the following line:

```text id="qxgkc2"
mibs :
```

For manual testing, you can temporarily specify MIBs using an environment variable:

```bash id="sdlmji"
MIBS=+SNMPv2-MIB:+UCD-SNMP-MIB snmptranslate -On UCD-SNMP-MIB::memAvailReal.0
```

### Restart Zabbix

If Zabbix is installed as a systemd service, after adding MIB files you can restart Zabbix Server:

```bash id="i7ihr8"
sudo systemctl restart zabbix-server
```

or Zabbix Proxy:

```bash id="9nj4lv"
sudo systemctl restart zabbix-proxy
```

This is usually not required for the template itself because numeric OIDs are used. Restarting is useful if you use MIB names in manual diagnostics or other SNMP items.

## Template Import

1. Download the template file from this repository.
2. In Zabbix, open:

```text id="vkix7s"
Data collection → Templates → Import
```

3. Import the template file.
4. Create a host for the Keenetic device.
5. Add an SNMP interface with the router IP address.
6. Configure SNMP community or SNMPv3 credentials.
7. Link the template:

```text id="k0ah3m"
KeeneticOS by SNMP
```

8. Verify that ICMP and SNMP items receive data.
9. Wait for the network interface discovery rule to run.

## Macros

The template contains the following macros:

| Macro                                 |                    Default | Description                                        |
| ------------------------------------- | -------------------------: | -------------------------------------------------- |
| `{$CPU.UTIL.MAX}`                     |                       `90` | High CPU utilization threshold, %                  |
| `{$MEMORY.UTIL.MAX}`                  |                       `90` | High memory utilization threshold, %               |
| `{$ICMP_LOSS_WARN}`                   |                       `20` | Packet loss threshold, %                           |
| `{$ICMP_RESPONSE_TIME_WARN}`          |                     `0.15` | ICMP response time threshold, seconds              |
| `{$SNMP.TIMEOUT}`                     |                       `5m` | Time window for SNMP collection availability check |
| `{$IF.UTIL.MAX}`                      |        not set in template | Interface utilization threshold, %                 |
| `{$IF.ERRORS.WARN}`                   |                        `2` | Interface error threshold                          |
| `{$NET.IF.IFADMINSTATUS.MATCHES}`     |                      `^.*` | Discovery filter by admin status                   |
| `{$NET.IF.IFADMINSTATUS.NOT_MATCHES}` |                      `^2$` | Exclude interfaces with admin status down          |
| `{$NET.IF.IFALIAS.MATCHES}`           |                       `.*` | Discovery filter by alias                          |
| `{$NET.IF.IFALIAS.NOT_MATCHES}`       |         `CHANGE_IF_NEEDED` | Exclude by alias                                   |
| `{$NET.IF.IFDESCR.MATCHES}`           |                       `.*` | Discovery filter by description                    |
| `{$NET.IF.IFDESCR.NOT_MATCHES}`       |         `CHANGE_IF_NEEDED` | Exclude by description                             |
| `{$NET.IF.IFNAME.MATCHES}`            |                     `^.*$` | Discovery filter by interface name                 |
| `{$NET.IF.IFNAME.NOT_MATCHES}`        | loopback/docker/veth regex | Exclude service interfaces                         |
| `{$NET.IF.IFOPERSTATUS.MATCHES}`      |                     `^.*$` | Discovery filter by oper status                    |
| `{$NET.IF.IFOPERSTATUS.NOT_MATCHES}`  |                      `^6$` | Exclude notPresent interfaces                      |

Example host-level interface utilization threshold:

```text id="t0g4jj"
{$IF.UTIL.MAX} = 90
```

You can also define a context macro for a specific interface:

```text id="rv6q38"
{$IF.UTIL.MAX:"GigabitEthernet0"} = 80
```

## Used OIDs

The template uses standard SNMP OIDs and OIDs from `SNMPv2-MIB.mib` and `UCD-SNMP-MIB.mib`.

### System

```text id="82sejp"
.1.3.6.1.2.1.1
```

Used for system name, description, location and uptime.

Examples:

| OID                  | Description        |
| -------------------- | ------------------ |
| `.1.3.6.1.2.1.1.1.0` | System Description |
| `.1.3.6.1.2.1.1.3.0` | System Uptime      |
| `.1.3.6.1.2.1.1.5.0` | System Name        |
| `.1.3.6.1.2.1.1.6.0` | System Location    |

### Hardware inventory

```text id="hnnpbv"
.1.3.6.1.2.1.47.1.1.1.1
```

Used for manufacturer, model, serial number and CID/UUID.

Examples:

| OID                          | Description   |
| ---------------------------- | ------------- |
| `.1.3.6.1.2.1.47.1.1.1.1.11` | Serial Number |
| `.1.3.6.1.2.1.47.1.1.1.1.12` | Manufacturer  |
| `.1.3.6.1.2.1.47.1.1.1.1.13` | Model         |
| `.1.3.6.1.2.1.47.1.1.1.1.19` | CID / UUID    |

### Memory

```text id="q7d2sy"
.1.3.6.1.4.1.2021.4
```

Used for total, available, shared, buffer and cached memory.

Examples:

| OID                        | Description      |
| -------------------------- | ---------------- |
| `.1.3.6.1.4.1.2021.4.5.0`  | Total memory     |
| `.1.3.6.1.4.1.2021.4.6.0`  | Available memory |
| `.1.3.6.1.4.1.2021.4.13.0` | Shared memory    |
| `.1.3.6.1.4.1.2021.4.14.0` | Buffer memory    |
| `.1.3.6.1.4.1.2021.4.15.0` | Cached memory    |

### CPU load average

```text id="6msf8p"
.1.3.6.1.4.1.2021.10
```

Used for load average for 1, 5 and 15 minutes.

Examples:

| OID                          | Description      |
| ---------------------------- | ---------------- |
| `.1.3.6.1.4.1.2021.10.1.3.1` | Load average 1m  |
| `.1.3.6.1.4.1.2021.10.1.3.2` | Load average 5m  |
| `.1.3.6.1.4.1.2021.10.1.3.3` | Load average 15m |

### CPU raw counters

```text id="kdh0qv"
.1.3.6.1.4.1.2021.11
```

Used to calculate CPU utilization from raw user, nice, system and idle counters.

Examples:

| OID                         | Description    |
| --------------------------- | -------------- |
| `.1.3.6.1.4.1.2021.11.50.0` | CPU raw user   |
| `.1.3.6.1.4.1.2021.11.51.0` | CPU raw nice   |
| `.1.3.6.1.4.1.2021.11.52.0` | CPU raw system |
| `.1.3.6.1.4.1.2021.11.53.0` | CPU raw idle   |

### Network interfaces

```text id="k2eago"
.1.3.6.1.2.1.2.2
.1.3.6.1.2.1.31.1.1.1
```

Used for interface discovery, statuses, speed, traffic counters, errors and discarded packets.

## How It Works

The template uses several `SNMP walk` master items, for example:

```text id="a3x9d5"
keenetic.system.walk
keenetic.hardware.walk
keenetic.memory.walk
keenetic.cpu.load.walk
keenetic.cpu.walk
```

Dependent items extract specific values from walk results using `SNMP_WALK_VALUE` preprocessing.

This approach reduces the number of separate SNMP requests to the device and allows multiple metrics to be extracted from one SNMP walk.

CPU utilization is calculated from raw counter changes:

```text id="5rag7g"
user + nice + system / user + nice + system + idle
```

Memory utilization is calculated as:

```text id="5ifzv0"
100 - available / total * 100
```

## Network Interfaces Discovery

The template automatically discovers network interfaces using SNMP LLD.

For each interface, it creates:

* inbound traffic;
* outbound traffic;
* inbound errors;
* outbound errors;
* inbound discards;
* outbound discards;
* speed;
* admin status;
* operational status.

Discovery can be customized using filter macros:

```text id="n7ee2e"
{$NET.IF.IFNAME.MATCHES}
{$NET.IF.IFNAME.NOT_MATCHES}
{$NET.IF.IFALIAS.MATCHES}
{$NET.IF.IFALIAS.NOT_MATCHES}
{$NET.IF.IFDESCR.MATCHES}
{$NET.IF.IFDESCR.NOT_MATCHES}
{$NET.IF.IFADMINSTATUS.MATCHES}
{$NET.IF.IFADMINSTATUS.NOT_MATCHES}
{$NET.IF.IFOPERSTATUS.MATCHES}
{$NET.IF.IFOPERSTATUS.NOT_MATCHES}
```

## Value Maps

### Interface admin status

| Value | Status  |
| ----- | ------- |
| `1`   | up      |
| `2`   | down    |
| `3`   | testing |

### Interface operational status

| Value | Status         |
| ----- | -------------- |
| `1`   | up             |
| `2`   | down           |
| `3`   | testing        |
| `4`   | unknown        |
| `5`   | dormant        |
| `6`   | notPresent     |
| `7`   | lowerLayerDown |

### zabbix.host.available

| Value | Status        |
| ----- | ------------- |
| `0`   | not available |
| `1`   | available     |
| `2`   | unknown       |

## Notes

The set of available SNMP OIDs may differ between KeeneticOS versions. If some items do not receive data, check the corresponding OIDs using `snmpwalk`.

Some interfaces may be hidden by discovery filters. Adjust the `MATCHES` / `NOT_MATCHES` macros if needed.

The `{$IF.UTIL.MAX}` macro is used in the high interface utilization trigger but may not be defined in the template. It is recommended to define it at the host or template level.

## Compatibility

The template was prepared for Zabbix 7.0.

Compatibility with other Zabbix versions is possible but should be tested separately.

Compatibility depends on KeeneticOS version and the set of SNMP OIDs exposed by the device.

## Project Status

Current template version: `0.8.2`

The template is in practical use and under further development. Pull requests, issues and suggestions are welcome.
