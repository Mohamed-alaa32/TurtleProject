#!/usr/bin/env python3


from math import atan2, pow, sqrt
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist



#Variables: Distance, Velocity, Angular, dX , dY, Xi ,X, Yi, Y, B, Phi

class TurtleBot:
    def __init__(self):
        rospy.init_node ('turtle_controller', anonymous=True)
    
        self.velocity_publisher = rospy.Publisher ('/turtle1/cmd_vel', Twist, queue_size=10)
    
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        self.pose = Pose()

        self.rate = rospy.Rate(5)
    
    def update_pose(self, data):

        self.pose = data         
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    
    def distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
    
    
    def linear_vel(self, goal_pose):
        
        constant=rospy.get_param("/gains/linear")
        return constant * self.distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose):
        constant2=rospy.get_param("/gains/angular")
        return constant2 * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        goal_pose = Pose()

        goal_pose.x = rospy.get_param("/goals/x")
        
        goal_pose.y = rospy.get_param("/goals/y")
        

        tolerance = 0.1
        

        vel_msg = Twist()

        while self.distance(goal_pose) >= tolerance:

            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)
            
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            

            self.velocity_publisher.publish(vel_msg)

            self.rate.sleep()
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass       