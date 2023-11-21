#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import actionlib
import ACROBA_Workshop_SIGMA.msg

def main():
    rospy.init_node("test_Rotate")

    client = actionlib.SimpleActionClient(
        "Rotate", ACROBA_Workshop_SIGMA.msg.RotateAction
    )
    client.wait_for_server()
    goal = ACROBA_Workshop_SIGMA.msg.RotateGoal()
    rate = rospy.Rate(60)

    while not rospy.is_shutdown():
        goal.turtle_name = "turtle1"
        goal.speed = 0.1
        goal.angle = 90  # Rotate 90 degrees
        goal.isClockwise = False  # Rotate counterclockwise
        client.send_goal(goal)
        client.wait_for_result()
        rate.sleep()

if __name__ == "__main__":
    main()

