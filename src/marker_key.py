#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import sys, select, os

from rospy import rostime
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

def getKey():
    if os.name == 'nt':
      if sys.version_info[0] >= 3:
        return msvcrt.getch().decode()
      else:
        return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__ == "__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('maker_key')
    pub = rospy.Publisher('marker_pos', Odometry, queue_size=10)

    markers = rospy.get_param('/markers')
    index = 0
    odometry = Odometry()

    while(index < len(markers)):
        key = getKey()
        if key == 'm' :
            odometry.pose.pose.position.x = markers[index][0]
            odometry.pose.pose.position.y = markers[index][1]
            odometry.pose.pose.orientation.z = markers[index][2]
            odometry.header.seq = index
            odometry.header.stamp = rospy.Time.now()
            pub.publish(odometry)
            print(odometry)
            index = index + 1
        elif key == '\x03' :
            break

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
