#!/usr/bin/env python
import roslib; roslib.load_manifest('guts')
import rospy
import math
import tf

from guts.msg import motor_cmd
from visualization_msgs.msg import Marker

def gp_tracking_rviz_callback(motor_cmd_msg):
    rospy.loginfo(rospy.get_name() + ": I heard %d %d" % (motor_cmd_msg.left_motor_speed, motor_cmd_msg.right_motor_speed))

    arrow = Marker()
    arrow.header.frame_id = "/my_frame"
    #point.header.stamp = rospy.get_time()
    arrow.type = Marker.ARROW
    arrow.action = Marker.ADD
    arrow.id = 4
    arrow.ns = "basic_shapes"

    arrow.scale.x = 1.0
    arrow.scale.y = 1.0
    arrow.scale.z = 0.1 * ((motor_cmd_msg.left_motor_speed + motor_cmd_msg.right_motor_speed)/2)

    arrow.color.a = 1.0
    arrow.color.r = 1.0
    arrow.color.g = 1.0
    arrow.color.b = 0.0

    if (motor_cmd_msg.left_motor_speed + motor_cmd_msg.right_motor_speed != 0):
        yaw = math.pi/2 - math.atan(((motor_cmd_msg.left_motor_speed - motor_cmd_msg.right_motor_speed)/2.0)/((motor_cmd_msg.left_motor_speed + motor_cmd_msg.right_motor_speed)/2.0))
        
    else:
        yaw = math.pi/2

    

    quaternion = tf.transformations.quaternion_from_euler(0, 0, yaw)

    arrow.pose.orientation.w = quaternion[3]
    arrow.pose.orientation.x = quaternion[0]
    arrow.pose.orientation.y = quaternion[1]
    arrow.pose.orientation.z = quaternion[2]


    arrow.pose.position.x = 0
    arrow.pose.position.y = 0
    arrow.pose.position.z = 0

    pub = rospy.Publisher('gp_prediction_rviz_msg', Marker)
    pub.publish(arrow)     


def gp_tracking_rviz():
    rospy.Subscriber("motor_cmd_msg",motor_cmd, gp_tracking_rviz_callback)
    rospy.init_node('guts_gp_tracking_rviz_node', anonymous=True)
    
    rospy.spin()


if __name__ == '__main__':
    gp_tracking_rviz()
