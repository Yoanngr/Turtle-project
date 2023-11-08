#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import actionlib
import ACROBA_Workshop_SIGMA.msg

def main():
    rospy.init_node("test_Follow")

    client = actionlib.SimpleActionClient(
        "Follow_turtle1", ACROBA_Workshop_SIGMA.msg.FollowAction
    )
    client.wait_for_server()
    goal = ACROBA_Workshop_SIGMA.msg.FollowGoal()
    rate = rospy.Rate(60)

    while not rospy.is_shutdown():
        goal.turtlename = "turtle1" 
        client.send_goal(goal)
        client.wait_for_result()
        rate.sleep()

if __name__ == "__main__":
    main()

