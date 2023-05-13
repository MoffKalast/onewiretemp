#!/usr/bin/env python3
import rospy
import time
import os

from sensor_msgs.msg import Temperature

RPI_CPU_PATH = "/sys/class/thermal/thermal_zone0/temp"
ONEWIRE_PATH = "/sys/bus/w1/devices"

class TemperatureNode:
	def __init__(self):
		rospy.init_node('temperature_node')

		self.onewires = {}
		self.onewire_names = rospy.get_param("~onewire_names", "").split(",")
		self.onewire_addrs = rospy.get_param("~onewire_addresses", "").split(",")
		
		for i in range(len(self.onewire_names)):
			name = self.onewire_names[i].strip()
			addr = self.onewire_addrs[i].strip()

			if len(name) != 0 and len(addr) != 0:
				self.onewires[name] = addr

		self.onewire_pub = {}
		for key in self.onewires:
			self.onewire_pub[key] = self.pub = rospy.Publisher('temp/'+key, Temperature, queue_size=1)


		self.cpu_pub = rospy.Publisher('temp/cpu', Temperature, queue_size=1)

	def read_temperature(self, path):
		val = 0.0
		with open(path, 'r') as file:
			for line in file:
				val = float(line.strip()) / 1000.0
				break
		return val


	def update(self):
		if os.path.exists(RPI_CPU_PATH):
			temp_msg = Temperature()
			temp_msg.temperature = self.read_temperature(RPI_CPU_PATH)
			temp_msg.variance = 0.0
			self.cpu_pub.publish(temp_msg)

		for key in self.onewires:
			path = ONEWIRE_PATH+"/"+self.onewires[key]+"/temperature"

			if os.path.exists(path):
				temp_msg = Temperature()
				temp_msg.temperature = self.read_temperature(path)
				temp_msg.variance = 0.0
				self.onewire_pub[key].publish(temp_msg)


try:

	temp = TemperatureNode()
	rate = rospy.Rate(0.7)
	while not rospy.is_shutdown():
		temp.update()
		rate.sleep()

except rospy.ROSInterruptException:
	print("Script interrupted", file=sys.stderr)
