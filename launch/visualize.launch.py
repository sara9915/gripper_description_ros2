import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch_ros.actions import Node



def generate_launch_description():

    xacro_file_default = os.path.join(get_package_share_directory('gripper_description'), 'grippers',
                                     'yaskawa_pushing.xacro')

    model_launch_arg = DeclareLaunchArgument(
        name='model',
        default_value= xacro_file_default,
        description='Absolute xacro path'
    )


    robot_description = Command(
        [FindExecutable(name='xacro'), ' ', LaunchConfiguration('model')])

    rviz_file = os.path.join(get_package_share_directory('gripper_description'), 'rviz',
                             'visualize.rviz')

    return LaunchDescription([   
        model_launch_arg,
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(package='rviz2',
             executable='rviz2',
             name='rviz2',
             arguments=['--display-config', rviz_file]
             )
    ])