# Topicator

Сервис для обработки MQTT событий

### Установка

#### Через центральный репозиторий

1. Обновить индекс - ```apt update```
2. Установить драйвер - ```apt install topicator```
3. проверить состояние службы - ```service topicator status```

#### Из оффлайн пакета

```
dpkg -i topicator-<version>-<platform>.deb
```

### Управление сервисом:
```
service topicator start    - запустить
service topicator stop     - остановить
service topicator restart  - перезапустить
service topicator status   - статус
```

## Основные положения по сервису:

1. Для корректной работы должен быть установлен и сконфигурирован брокер сообщений Mosquitto
<details>

```
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa.
sudo apt-get update.
sudo apt-get install mosquitto.
sudo apt-get install mosquitto-clients.
sudo apt clean
```

или, если пакет имеется в центральном репозитории:
```
sudo apt install -y mosquitto
```

для проверки работоспособности брокера можно выполнить комманду:
```
sudo systemctl status mosquitto
```
примерный вывод должен быть следующий:
```
● mosquitto.service - Mosquitto MQTT Broker
     Loaded: loaded (/lib/systemd/system/mosquitto.service; enabled; vendor pre>
     Active: active (running) since Tue 2024-05-07 14:02:34 +06; 1 day 3h ago
       Docs: man:mosquitto.conf(5)
             man:mosquitto(8)
   Main PID: 994 (mosquitto)
      Tasks: 1 (limit: 38373)
     Memory: 3.3M
        CPU: 35.176s
     CGroup: /system.slice/mosquitto.service
             └─994 /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf

мая 07 14:02:33 toor-SS systemd[1]: Starting Mosquitto MQTT Broker...
мая 07 14:02:34 toor-SS mosquitto[994]: 1715068954: Loading config file /etc/mo>
мая 07 14:02:34 toor-SS systemd[1]: Started Mosquitto MQTT Broker.
```
</details>

2. 


## Сборка пакета:

### Для инсталлятора в виде исполняемых файлов

- перейти в папку 'project/scripts'
- запустить скрипт build.sh с параметрами
    - адрес машины для сборки
    - порт для подключения ssh
    - пароль пользователя root

пример:
```
cd project/scripts
./build.sh 192.168.1.100 22 test
```

