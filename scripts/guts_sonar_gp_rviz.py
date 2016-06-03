#!/usr/bin/env python
import roslib; roslib.load_manifest('guts')
import rospy
import math

from guts.msg import gp_prediction
from visualization_msgs.msg import Marker

def gp_prediction_rviz_callback(gp_prediction_msg):
    rospy.loginfo(rospy.get_name() + ": I heard %f %f %f %f" % (gp_prediction_msg.mean_x, gp_prediction_msg.mean_y, gp_prediction_msg.cov_x, gp_prediction_msg.cov_y,))

    point = Marker()
    point.header.frame_id = "/my_frame"
    #point.header.stamp = rospy.get_time()
    point.type = Marker.CUBE
    point.action = Marker.ADD
    point.id = 0
    point.ns = "basic_shapes"

    point_cov = Marker()
    point_cov.header.frame_id = "/my_frame"
    #point.header.stamp = rospy.get_time()
    point_cov.type = Marker.CYLINDER
    point_cov.action = Marker.ADD
    point_cov.id = 1
    point_cov.ns = "basic_shapes"

    guts_body = Marker()
    guts_body.header.frame_id = "/my_frame"
    #point.header.stamp = rospy.get_time()
    guts_body.type = Marker.CUBE
    guts_body.action = Marker.ADD
    guts_body.id = 2
    guts_body.ns = "basic_shapes"

    point.scale.x = 0.2
    point.scale.y = 0.2
    point.scale.z = 0.2

    point_cov.scale.x = math.sqrt(gp_prediction_msg.cov_x)
    point_cov.scale.y = math.sqrt(gp_prediction_msg.cov_y)
    point_cov.scale.z = 0.0

    guts_body.scale.x = 0.65
    guts_body.scale.y = 0.8
    guts_body.scale.z = 0.2

    point.color.a = 1.0
    point.color.r = 0.0
    point.color.g = 1.0
    point.color.b = 0.0
    point.pose.orientation.w = 1.0
    point.pose.orientation.x = 0.0
    point.pose.orientation.y = 0.0
    point.pose.orientation.z = 0.0

    point_cov.color.a = 1.0
    point_cov.color.r = 1.0
    point_cov.color.g = 0.0
    point_cov.color.b = 0.0
    point_cov.pose.orientation.w = 1.0
    point_cov.pose.orientation.x = 0.0
    point_cov.pose.orientation.y = 0.0
    point_cov.pose.orientation.z = 0.0

    guts_body.color.a = 1.0
    guts_body.color.r = 0.0
    guts_body.color.g = 0.0
    guts_body.color.b = 1.0
    guts_body.pose.orientation.w = 1.0
    guts_body.pose.orientation.x = 0.0
    guts_body.pose.orientation.y = 0.0
    guts_body.pose.orientation.z = 0.0

    point.pose.position.x = gp_prediction_msg.mean_x
    point.pose.position.y = gp_prediction_msg.mean_y
    point.pose.position.z = 0

    point_cov.pose.position.x = gp_prediction_msg.mean_x
    point_cov.pose.position.y = gp_prediction_msg.mean_y
    point_cov.pose.position.z = 0

    guts_body.pose.position.x = 0
    guts_body.pose.position.y = -0.4
    guts_body.pose.position.z = 0
    
    
    

    pub = rospy.Publisher('gp_prediction_rviz_msg', Marker)
    pub.publish(point)  
    pub.publish(point_cov)  
    pub.publish(guts_body)    


def gp_prediction_rviz():
    rospy.Subscriber("gp_prediction_msg",gp_prediction, gp_prediction_rviz_callback)
    rospy.init_node('guts_gp_prediction_rviz_node', anonymous=True)
    
    rospy.spin()


if __name__ == '__main__':
    gp_prediction_rviz()
