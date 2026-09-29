import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class MotorSimulator(Node):
    """A first-order DC motor model: tau * dw/dt + w = gain * voltage."""

    def __init__(self) -> None:
        super().__init__('motor_simulator')

        self.declare_parameter('motor_gain', 3.0)
        self.declare_parameter('time_constant', 0.25)
        self.declare_parameter('simulation_rate_hz', 200.0)

        self.motor_gain = float(self.get_parameter('motor_gain').value)
        self.time_constant = float(self.get_parameter('time_constant').value)
        rate_hz = float(self.get_parameter('simulation_rate_hz').value)
        if self.time_constant <= 0.0 or rate_hz <= 0.0:
            raise ValueError('time_constant and simulation_rate_hz must be positive')

        self.dt = 1.0 / rate_hz
        self.command_voltage = 0.0
        self.velocity = 0.0

        self.create_subscription(
            Float64, '/motor/command_voltage', self.command_callback, 10
        )
        self.velocity_publisher = self.create_publisher(
            Float64, '/motor/measured_velocity', 10
        )
        self.create_timer(self.dt, self.simulation_step)
        self.get_logger().info('Motor simulator started')

    def command_callback(self, msg: Float64) -> None:
        self.command_voltage = msg.data

    def simulation_step(self) -> None:
        steady_state_velocity = self.motor_gain * self.command_voltage
        acceleration = (
            steady_state_velocity - self.velocity
        ) / self.time_constant
        self.velocity += acceleration * self.dt

        msg = Float64()
        msg.data = self.velocity
        self.velocity_publisher.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MotorSimulator()
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
