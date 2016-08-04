#!/usr/bin/env python
import roslib; roslib.load_manifest('guts')
import rospy
from guts.msg import motor_cmd
import sys, select, termios, tty

reference_speed_fb = 20
reference_speed_lr = 15

msg = """
Control GUTS with Keyboard!
---------------------------
Moving around:

w: forward
s: backward
a: turn left
d: turn right

anything else : stop

CTRL-C to quit
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key




if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('guts_tele_op') 
    pub = rospy.Publisher('motor_cmd_msg', motor_cmd,queue_size=2)    

    motor_cmd_msg = motor_cmd()

    count = 0
    try:
        print msg
        while(1):
            key = getKey()
            if (key == '\x03'):
                print "quit..."
                rospy.sleep(2.0)
                break

            elif key == 'w':
                motor_cmd_msg.left_motor_speed = reference_speed_fb
                motor_cmd_msg.right_motor_speed = reference_speed_fb
                count = 0
                print "forward..."
            elif key == 's':
                motor_cmd_msg.left_motor_speed = -1*reference_speed_fb
                motor_cmd_msg.right_motor_speed = -1*reference_speed_fb
                count = 0
                print "backward..."
            elif key == 'a':
                motor_cmd_msg.left_motor_speed = -1*reference_speed_lr
                motor_cmd_msg.right_motor_speed = reference_speed_lr
                count = 0
                print "turn left..."
            elif key == 'd':
                motor_cmd_msg.left_motor_speed = reference_speed_lr
                motor_cmd_msg.right_motor_speed = -1*reference_speed_lr
                count = 0
                print "turn right..."
            elif key == ' ':
                motor_cmd_msg.left_motor_speed = 0
                motor_cmd_msg.right_motor_speed = 0
                print "stop..."
            else:
                count = count + 1
                if count > 4:
                    motor_cmd_msg.left_motor_speed = 0
                    motor_cmd_msg.right_motor_speed = 0
                    print "stop..."
                
            #rospy.sleep(0.2)
            pub.publish(motor_cmd_msg)

    except:
        print "error during guts_tele_op..."

    finally:
        motor_cmd_msg = motor_cmd()
        motor_cmd_msg.left_motor_speed = 0
        motor_cmd_msg.right_motor_speed = 0

        pub.publish(motor_cmd_msg)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

