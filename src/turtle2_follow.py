#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# Initialize current_pose for turtles with default values
current_pose_turtle2 = Pose()
current_pose_turtle1 = Pose()

def pose_callback_turtle2(data):
    # Callback function to get the current pose of turtle2
    global current_pose_turtle2
    current_pose_turtle2 = data

def pose_callback_turtle1(data):
    # Callback function to get the current pose of turtle1
    global current_pose_turtle1
    current_pose_turtle1 = data

def calculate_distance():
    # Calculate the Euclidean distance between turtle1 and turtle2
    delta_x = current_pose_turtle1.x - current_pose_turtle2.x
    delta_y = current_pose_turtle1.y - current_pose_turtle2.y
    distance = math.sqrt(delta_x**2 + delta_y**2)
    return distance

def calculate_angle():
    # Calculate the angle difference (orientation) between turtle1 and turtle2
    angle_difference = math.atan2(current_pose_turtle1.y - current_pose_turtle2.y,
                                   current_pose_turtle1.x - current_pose_turtle2.x) - current_pose_turtle2.theta
    return angle_difference

def move_turtle2_track():
    # Set up a publisher for the Twist messages for turtle2
    cmd_vel_pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)

    # Set up a subscriber to get the current pose of turtle2
    rospy.Subscriber('/turtle2/pose', Pose, pose_callback_turtle2)

    # Set up a subscriber to get the current pose of turtle1
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback_turtle1)

    # Set the rate at which to publish Twist messages
    rate = rospy.Rate(5)  # 5 Hz

    while not rospy.is_shutdown():
        # Create a Twist message
        twist_msg = Twist()

        # Calculate linear and angular velocities for turtle2 to track turtle1
        distance_to_turtle1 = calculate_distance()
        angle_to_turtle1 = calculate_angle()

        # Proportional control for linear velocity (adjust as needed)
        linear_velocity = 0.8 * distance_to_turtle1

        # Proportional control for angular velocity (adjust as needed)
        angular_velocity = 2.0 * angle_to_turtle1

        # Set the linear and angular velocities
        twist_msg.linear.x = linear_velocity
        twist_msg.angular.z = angular_velocity

        # Publish the Twist message
        cmd_vel_pub.publish(twist_msg)

        # Log the current pose of turtle2 and turtle1
        rospy.loginfo("Turtle2 Pose: x=%.2f, y=%.2f, theta=%.2f",
                      current_pose_turtle2.x, current_pose_turtle2.y, current_pose_turtle2.theta)
        rospy.loginfo("Turtle1 Pose: x=%.2f, y=%.2f, theta=%.2f",
                      current_pose_turtle1.x, current_pose_turtle1.y, current_pose_turtle1.theta)

        # Sleep to maintain the desired rate
        rate.sleep()

def main():
    # Initialize the ROS node
    rospy.init_node('turtle2_follow', anonymous=True)

    # Move turtle2 to track turtle1
    move_turtle2_track()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

