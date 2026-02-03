from setuptools import setup
import os
from glob import glob

package_name = 'trajectory_relay'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launchファイルをインストール
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='autoware',
    maintainer_email='autoware@example.com',
    description='Relay node for Autoware trajectories',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # コマンド名 = パッケージ名.ファイル名:関数名
            'trajectory_relay_node = trajectory_relay.trajectory_relay_node:main'
        ],
    },
)
