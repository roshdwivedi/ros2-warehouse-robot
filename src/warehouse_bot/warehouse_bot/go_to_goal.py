import math


import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from warehouse_bot.geometry import (
    clamp,
    distance_and_angle_to_goal,
    normalize_angle,
    yaw_from_quaternion,
)


K_ANGULAR = 1.5
MAX_ANGULAR = 1.0
ANGLE_TOLERANCE = math.radians(3.0)


class GoToGoal(Node):

    def __init__(self):
        super().__init__('go_to_goal')
        self.goal_x = 0.0
        self.goal_y = 2.0
        # Robot pose: None until the first odom message arrives
        self.x = None
        self.y = None
        self.yaw = None
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.on_odom, 10)
        self.timer = self.create_timer(0.1, self.control_loop)

    def on_odom(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.yaw = yaw_from_quaternion(q.x, q.y, q.z, q.w)

    def control_loop(self):
        if self.x is None:
            return  # no odometry yet, nothing to do
        distance, angle_to_goal = distance_and_angle_to_goal(
            self.x, self.y, self.goal_x, self.goal_y)
        heading_error = normalize_angle(angle_to_goal - self.yaw)
        self.get_logger().info(
            f'distance {distance:.2f} m, heading error {math.degrees(heading_error):.1f} deg'
        )
        
        cmd = Twist()
        if abs(heading_error) > ANGLE_TOLERANCE:
            cmd.angular.z = clamp(K_ANGULAR * heading_error, MAX_ANGULAR)
        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = GoToGoal()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
