#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import actionlib
import ACROBA_Workshop_SIGMA.msg


def main():
    rospy.init_node("test_follo", anonymous=True)

    client = actionlib.SimpleActionClient(
        "follo", ACROBA_Workshop_SIGMA.msg.folloAction
    )
    client.wait_for_server()
    goal = ACROBA_Workshop_SIGMA.msg.folloGoal()
    rate = rospy.Rate(200)

    while not rospy.is_shutdown():
        goal.turtle_name = "turtle1"
        goal.speed_move = 1
        goal.distance = 2
        goal.isForward = True
        goal.speed_rotate = 90
        goal.degrees = 90
        goal.isClockwise = True
        near_velocity=0.5
        lar_velocity=1.0
        client.send_goal(goal)
        client.wait_for_result()
        rate.sleep()


if __name__ == "__main__":
    main()
