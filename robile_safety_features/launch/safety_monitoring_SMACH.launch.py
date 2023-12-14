#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    safety_monitoring_SMACH_node = Node(
        package='robile_safety_features',
        executable='safety_monitoring_SMACH',
        output='screen',
        emulate_tty=True
    )

    return LaunchDescription([
        safety_monitoring_SMACH_node
    ])
