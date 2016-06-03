#!/usr/bin/env python
import roslib; roslib.load_manifest('guts')
import rospy

from guts.msg import gp_prediction
from guts.msg import motor_cmd
import math

kp_trans = 20
kp_rot = 10

mean_y_offset = 1.2


def gp_tracking_callback(gp_prediction_msg):
    rospy.loginfo(rospy.get_name() + ": I heard %f %f %f %f" % (gp_prediction_msg.mean_x, gp_prediction_msg.mean_y, gp_prediction_msg.cov_x, gp_prediction_msg.cov_x,))

    motor_cmd_msg = motor_cmd()

    if (math.sqrt(math.pow(gp_prediction_msg.mean_x,2)+math.pow(gp_prediction_msg.mean_y,2))>mean_y_offset) and (math.sqrt(max(gp_prediction_msg.cov_x,gp_prediction_msg.cov_y))<0.4):    
        motor_cmd_msg.left_motor_speed = kp_trans*gp_prediction_msg.mean_y + kp_rot*gp_prediction_msg.mean_x
        motor_cmd_msg.right_motor_speed = kp_trans*gp_prediction_msg.mean_y - kp_rot*gp_prediction_msg.mean_x
    else:
        motor_cmd_msg.left_motor_speed = 0
        motor_cmd_msg.right_motor_speed = 0  
    

    pub = rospy.Publisher('motor_cmd_msg', motor_cmd)
    pub.publish(motor_cmd_msg)    


def gp_tracking():
    rospy.Subscriber("gp_prediction_msg",gp_prediction, gp_tracking_callback)
    rospy.init_node('guts_tracking_node', anonymous=True)
    
    rospy.spin()


if __name__ == '__main__':
    gp_tracking()
