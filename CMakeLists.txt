cmake_minimum_required(VERSION 2.8.3)
project(ezpkg_onewiretemp)

find_package(catkin REQUIRED COMPONENTS
	roscpp
	rospy
	message_generation
	std_msgs
	geometry_msgs
)

catkin_package(
	CATKIN_DEPENDS std_msgs message_runtime 
)
