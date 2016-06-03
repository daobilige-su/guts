#!/usr/bin/env python
import roslib; roslib.load_manifest('guts')
import rospy
from guts.msg import motor_cmd

import serial
ser = serial.Serial('/dev/ttyACM1', 19200, timeout=60)
# turn of velocity change smoothing function.
ser.flushInput()
ser.flushOutput()
rospy.sleep(1.0)
ser.write("bso0000e")
rospy.sleep(1.0)


# motor_cmd.left_motor_speed and motor_cmd.right_motor_speed has to be -63-63
def callback(motor_cmd_msg):
    rospy.loginfo(rospy.get_name() + ": I heard %d %d" % (motor_cmd_msg.left_motor_speed, motor_cmd_msg.right_motor_speed))
    serial_msg = 'b%03d%03de' % ((motor_cmd_msg.left_motor_speed+64),(motor_cmd_msg.right_motor_speed+64))
    rospy.loginfo("so, I am sending serial %s" % serial_msg)
    ser.flushInput()
    ser.flushOutput()
    ser.write(serial_msg)
    


def receive_motor_cmd_smg():
    rospy.Subscriber("motor_cmd_msg", motor_cmd, callback)
    rospy.init_node('guts_motor_controller', anonymous=True)
    
    rospy.spin()


if __name__ == '__main__':
    receive_motor_cmd_smg()
