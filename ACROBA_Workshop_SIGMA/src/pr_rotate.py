#!/usr/bin/env python3
import rospy
import actionlib
import ACROBA_Workshop_SIGMA.msg
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class RotateAction:
    feedback = ACROBA_Workshop_SIGMA.msg.RotateFeedback()
    result = ACROBA_Workshop_SIGMA.msg.RotateResult()

    def __init__(self, name):
        self.vel_msg = Twist()
        self._action_name = name
        self._as = actionlib.SimpleActionServer(
            self._action_name,
            ACROBA_Workshop_SIGMA.msg.RotateAction,
            execute_cb=self.execute_cb,
            auto_start=False,
        )
        self._as.start()
        rospy.loginfo("Rotate Server Ready...")

    def pose_feedback_callback(self, data):
        self.feedback.pose = data
        self._as.publish_feedback(self.feedback)

    def execute_cb(self, goal):
        velocity_publisher = rospy.Publisher("/"+goal.turtle_name+"/cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("/"+goal.turtle_name+"/pose", Pose, self.pose_feedback_callback)

        if (goal.speed <= 0 or goal.angle == 0 or type(goal.isClockwise) != bool):
            self._as.set_aborted()
            if goal.speed <= 0:
                rospy.loginfo("Aborted: speed value should be > 0")
            if goal.angle == 0:
                rospy.loginfo("Aborted: angle value should not be 0")
            if type(goal.isClockwise) != bool:
                rospy.loginfo("Aborted: isClockwise value should be True or False")
        else:
            success = True
            rospy.loginfo("Let's rotate your robot")

            # Checking if the rotation is clockwise or counterclockwise
            if goal.isClockwise:
                self.vel_msg.angular.z = -abs(goal.speed)
            else:
                self.vel_msg.angular.z = abs(goal.speed)

            current_angle = 0
            t0 = rospy.Time.now().to_sec()

            while current_angle < goal.angle:
                velocity_publisher.publish(self.vel_msg)
                t1 = rospy.Time.now().to_sec()
                current_angle = goal.speed * (t1 - t0)

            self.vel_msg.angular.z = 0
            velocity_publisher.publish(self.vel_msg)

            rospy.sleep(0.5)

            if success:
                rospy.loginfo("%s: Succeeded" % self._action_name)
                self._as.set_succeeded(self.result)

if __name__ == "__main__":
    rospy.init_node("Rotate")
    server = RotateAction(rospy.get_name())
    rospy.spin()

