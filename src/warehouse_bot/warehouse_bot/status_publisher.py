import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String


class StatusPublisher(Node):

    def __init__(self):
        super().__init__('status_publisher')
        self.publisher = self.create_publisher(String, 'robot_status', 10)
        self.battery = 100
        self.timer = self.create_timer(1.0, self.publish_status)

    def publish_status(self):
        msg = String()
        if (self.battery <= 20):
            msg.data  = f'Battery: {self.battery}% - LOW BATTERY, return to charger'
            self.get_logger().warning(msg.data)
            
        else:
            msg.data  = f'Battery: {self.battery}%'
            self.get_logger().info(msg.data)

        self.publisher.publish(msg)

        self.battery -= 1
        if (self.battery <= 0):
            self.battery = 100
            msg.data  = f'Charging Complete, Battery % -> {self.battery}'
            self.get_logger().info(msg.data)



def main():
    rclpy.init()
    node = StatusPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()