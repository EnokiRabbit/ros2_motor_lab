from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    parameters = PathJoinSubstitution([
        FindPackageShare('motor_control_demo'),
        'config',
        'motor_lab.yaml',
    ])

    return LaunchDescription([
        Node(
            package='motor_control_demo',
            executable='motor_controller',
            name='motor_controller',
            parameters=[parameters],
            output='screen',
        ),
        Node(
            package='motor_control_demo',
            executable='motor_simulator',
            name='motor_simulator',
            parameters=[parameters],
            output='screen',
        ),
    ])

