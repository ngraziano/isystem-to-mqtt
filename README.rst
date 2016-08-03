====================================
Interface for ISystem boiler to MQTT 
====================================

The poll_isystem_qtt.py poll the boiler and publish value to mqtt host.



Usage
-----

Installation 
::
    pip install --upgrade git+https://github.com/ngraziano/isystem-to-mqtt.git

Run
::
    poll_isystem_mqtt.py --user MQTTUSER --password MQTTPASSWORD --interval 60 --log DEBUG  mqtt.server.example.com

Mode Bimaitre (bimaster)
------------------------

Boiler may be configured in bismaster mode : it send query during 5s and wait query during 5s. 
If you have incorrect respond from the boiler you can try to add --bimaster flag to the command line to handle bimaster mode.

This mode is not well tested, ti may not work.


Hardware connection
-------------------

TODO

MQTT Topic
----------

Available mqtt topic can be found in isystem_to_mqtt/tables.py.

Variable READ_TABLE define topic exported to MQTT.

Variable WRITE_TABLE define topic subcribed to send data to boiler.

Main topic are:

=========================================== ======================================
TOPIC                                       Description
=========================================== ======================================
heating/zone-a/temperature                  Inside temperature
heating/outside/temperature                 Outsite temperature
heating/zone-a/day-target-temperature       Current day mode target temperature
heating/zone-a/day-target-temperature/SET   To set day mode target temperature
heating/zone-a/night-target-temperature     Currect night mode target temperature
heating/zone-a/night-target-temperature/SET To set night mode target temperature
=========================================== ======================================



