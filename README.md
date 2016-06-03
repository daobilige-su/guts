# guts
repository for the ROS package used in our GUTS project

This is a ROS package for our project GUTS plus the arduino codes for microcontroller used in the system hardware.

# how to use 
+ For microcontrollers: use Arduino SDK to write codes into related microcontrollers. Arduino codes are in the "arduino_code" folder. Specifically,
+ write "guts_vod" code into the POD attached to the user.
+ write "motor_controller_1_4" to the microcontroller that is used to control two wheel motors.
+ write "sonar_ir_sensor_module_sonar_only" to the microcontroller that is used to collect 4 sonars reading.

+ For ROS packages: git clone this package into your **catkin** ROS packages' **src** folder.
+ if only want to 
