from setuptools import find_packages, setup

package_name = 'warehouse_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rosh',
    maintainer_email='roshandwivedi99@gmail.com',
    description='A simulated warehouse robot: driving, obstacle stops, mapping, navigation and pick tasks with ROS2.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'status_publisher = warehouse_bot.status_publisher:main' # Telling ros2 about the subscriber
        ],
    },
)
