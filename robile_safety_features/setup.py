from setuptools import setup
import os
from glob import glob

package_name = 'robile_safety_features'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kishansawant',
    maintainer_email='kishansawant96@gmail.com',
    description='safety feature implementation using behavior tree and state machine',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'safety_monitoring_BT = robile_safety_features.safety_monitoring_BT:main',
            'safety_monitoring_SMACH = robile_safety_features.safety_monitoring_SMACH:main',
        ],
    },
)
