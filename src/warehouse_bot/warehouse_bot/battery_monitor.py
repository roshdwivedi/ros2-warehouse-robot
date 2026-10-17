import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class BatteryMonitor(Node):
    def __init__(self):
        super().__init__('battery_monitor')
        self.subscription = self.create_subscription(
            String, 'robot_status', self.on_status, 10
        )
        self.battery_low = False

    def on_status(self, msg):
        is_low = 'LOW' in msg.data

        if is_low and not self.battery_low:
            self.get_logger().warning(f'Robot needs charging: {msg.data}')
        elif not is_low and self.battery_low:
            self.get_logger().info(f'Battery OK again: {msg.data}')
        self.battery_low = is_low


def main():
    rclpy.init()
    node = BatteryMonitor()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
