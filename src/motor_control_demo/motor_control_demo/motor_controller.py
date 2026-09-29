import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

from .pi_controller import PIController


class MotorController(Node):
    def __init__(self) -> None:
        super().__init__('motor_controller')

        self.declare_parameter('kp', 0.7)
        self.declare_parameter('ki', 1.8)
        self.declare_parameter('max_voltage', 12.0)
        self.declare_parameter('control_rate_hz', 100.0)

        rate_hz = float(self.get_parameter('control_rate_hz').value)
        if rate_hz <= 0.0:
            raise ValueError('control_rate_hz must be positive')
        self.dt = 1.0 / rate_hz

        self.controller = PIController(
            kp=float(self.get_parameter('kp').value),
            ki=float(self.get_parameter('ki').value),
            output_limit=float(self.get_parameter('max_voltage').value),
        )
        self.target_velocity = 0.0
        self.measured_velocity = 0.0

        self.create_subscription(
            Float64, '/motor/target_velocity', self.target_callback, 10
        )
        self.create_subscription(
            Float64, '/motor/measured_velocity', self.feedback_callback, 10
        )
        self.command_publisher = self.create_publisher(
            Float64, '/motor/command_voltage', 10
        )
        self.create_timer(self.dt, self.control_step)
        self.get_logger().info('Motor PI controller started')

    def target_callback(self, msg: Float64) -> None:
        self.target_velocity = msg.data
        self.get_logger().info(f'New target: {msg.data:.2f} rad/s')

    def feedback_callback(self, msg: Float64) -> None:
        self.measured_velocity = msg.data

    def control_step(self) -> None:
        error = self.target_velocity - self.measured_velocity
        voltage = self.controller.update(error, self.dt)
        msg = Float64()
        msg.data = voltage
        self.command_publisher.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MotorController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
