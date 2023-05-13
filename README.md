# One Wire Temperature

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ROS node for reading temperatures from different sensors and publishes them as `sensor_msgs/Temperature` messages. It is designed to work with DS18B20 1-wire temperature sensors, but also reads a Raspberry Pi's CPU temperature sensor if running on a Pi.

## Params

```xml
<node name="temperature_node" pkg="temperature_node" type="temperature_node.py" output="screen">

  <!-- 
  Comma-separated list of names for 1-wire sensors
  Example: "motor_left, motor_right"
  -->
	<param name="onewire_names" value=""/> 

  <!--
  Comma-separated list of addresses for 1-wire sensors
  Example "28-9809be0164ff, 28-a99dbd0164ff"
  -->
	<param name="onewire_addresses" value=""/> 

	<!-- Update rate in Hz -->
	<param name="rate" value="0.7"/>

</node>
```

## Published Topics

For each 1-wire sensor, this node will publish a `sensor_msgs/Temperature` message on a topic with the name `temp/<sensor_name>`, where `<sensor_name>` is replaced with the name of the sensor from the list.

- `/temp/cpu` (`sensor_msgs/Temperature`): The temperature of the Raspberry Pi's CPU.

- `/temp/<sensor_name>` (`sensor_msgs/Temperature`): The temperature of the 1-wire sensor with the given name. There will be one of these topics for each 1-wire sensor.

Note: The `sensor_msgs/Temperature` message includes fields for the temperature in Celsius and the variance. The variance field is currently not used and is set to 0.0 in all published messages. The header field is also not populated. Depending on your application, you might want to modify the node to populate these fields.
