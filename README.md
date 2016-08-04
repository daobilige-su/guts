# guts
repository for the ROS package used in our GUTS project

This is a ROS package for our project GUTS plus the arduino codes for microcontroller used in the system hardware.

# how to use 
**microcontrollers**
+ For microcontrollers: use Arduino SDK to write codes into related microcontrollers. Arduino codes are in the "arduino_code" folder. Specifically,
+ write "guts_vod" code into the POD attached to the user.
+ write "motor_controller_1_4" to the microcontroller that is used to control two wheel motors.
+ write "sonar_ir_sensor_module_sonar_only" to the microcontroller that is used to collect 4 sonars reading.

**ROS package**
+ For ROS packages: git clone this package into your **catkin** ROS packages' **src** folder.
+ (1) **roscd && cd ..** to go to catkin workspace's folder.
+ (2) **catkin_make** to build the package. 
+ (3) **roscd guts** to go to the folder of this package.
+ (4) **cd GPy-0.4.6** to go Gpy folder.
+ (5) **sudo python install** to install Gpy. make sure internet is on, as the intallation process needs internet.
+ (6) **roscd guts** to go to the folder of this package.
+ (7) **roslaunch guts guts_sonar_gp_tracking_motor_rviz.launch** to run Gaussian Process based sonar array user tracking (with real motors) and rviz visualization.
+ (8) **roslaunch guts guts_sonar_gp_tracking_rviz.launch** to run Gaussian Process based sonar array user tracking (but without moters running) and rviz visualization.
+ (9) **roslaunch guts guts_sonar_gp_rviz.launch** to run run Gaussian Process based sonar array user location prediction (without tracking and motors running) and rviz visualization.
+ (10) **roslaunch guts guts_tele_op.launch** to run teleoperation with keyboard.
