#!/usr/bin/env python
import roslib; roslib.load_manifest('guts')
import rospy
from guts.msg import sonar_data

import serial
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=60)

def guts_sonar_ir_pub():
    pub = rospy.Publisher('guts_sonar_ir_data', sonar_data)
    rospy.init_node('guts_sonar_ir_node') 
    while not rospy.is_shutdown():
        current_time = rospy.get_rostime()
        s = ser.readline()
        arduino_serial_data = []
        arduino_serial_data.append([int(x) for x in s.split()])
        print arduino_serial_data
        sonar_data_msg = sonar_data()

        sonar_data_msg.sec = current_time.secs
        sonar_data_msg.nsec = current_time.nsecs

        if len(arduino_serial_data[0]) == 6:
            for x in range(6):
                sonar_data_msg.sonar_data[x] = arduino_serial_data[0][x]
        else:
            continue
        pub.publish(sonar_data_msg)

        #rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        guts_sonar_ir_pub()
    except rospy.ROSInterruptException:
        pass
