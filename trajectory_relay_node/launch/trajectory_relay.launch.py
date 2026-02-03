from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('input_selector', default_value='0'),
        Node(
            package='trajectory_relay',
            executable='trajectory_relay_node',
            name='trajectory_relay_node',
            output='screen',
            parameters=[
                {'input_selector': LaunchConfiguration('input_selector')},
                {'out_topic': '/planning/trajectory'},
                {'in_topic_1': '/planning/trajectory/planning_validator'},
                {'in_topic_2': '/planning/trajectory/diffusion_planner'}
            ]
        )
    ])
