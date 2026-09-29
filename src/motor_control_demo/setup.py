from glob import glob
from setuptools import find_packages, setup


package_name = 'motor_control_demo'


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    tests_require=['pytest'],
    zip_safe=True,
    maintainer='ROS 2 Student',
    maintainer_email='student@example.com',
    description='A small ROS 2 closed-loop motor control learning project.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'motor_controller = motor_control_demo.motor_controller:main',
            'motor_simulator = motor_control_demo.motor_simulator:main',
        ],
    },
)
