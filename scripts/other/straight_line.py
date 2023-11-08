#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def move_turtle(speed, distance, is_forward):
    # Initialize the ROS node
    rospy.init_node('straight_line', anonymous=True)

    # Create a publisher for the /turtle1/cmd_vel topic
    cmd_vel_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    # Create a Twist message to control the TurtleBot's movement
    cmd = Twist()

    # Set the linear velocity (forward or backward based on is_forward)
    cmd.linear.x = speed if is_forward else -speed

    # Set the initial time for measuring the duration
    start_time = rospy.get_time()

    # Move the TurtleBot for the specified distance
    while (rospy.get_time() - start_time) < (distance / speed):
        cmd_vel_publisher.publish(cmd)
        rospy.sleep(0.1)

    # Stop the TurtleBot by publishing a Twist with zero velocity
    cmd.linear.x = 0
    cmd_vel_publisher.publish(cmd)

if __name__ == '__main__':
    try:
        speed = 1.0  # Adjust the desired speed
        distance = 1.0  # Adjust the desired distance
        is_forward = True  # Set to True for forward, False for backward

        move_turtle(speed, distance, is_forward)

    except rospy.ROSInterruptException:
        pass

