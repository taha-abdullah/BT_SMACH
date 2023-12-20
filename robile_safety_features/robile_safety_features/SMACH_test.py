import unittest
import rclpy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from safety_monitoring_SMACH import MonitorBatteryAndCollision, RotateBase, StopBase


class TestBatteryAndCollision(unittest.TestCase):
    def setUp(self):
        rclpy.init()

    def tearDown(self):
        rclpy.shutdown()

    def test_low_battery(self):
        node = rclpy.create_node('test')
        state = MonitorBatteryAndCollision(node, battery_threshold=40,
                                           collision_threshold_distance=0.5,
                                           timeout=5)
        # give a low battery condition
        msg = String()
        msg.data = '30'
        state.battery_callback(msg)

        output = state.execute(None)
        self.assertEqual(output, 'low_battery_level')

    def test_collision(self):
        node = rclpy.create_node('test')
        state = MonitorBatteryAndCollision(node, battery_threshold=30,
                                           collision_threshold_distance=0.5, timeout=5)

        # Simulate a collision condition
        msg = LaserScan()
        msg.ranges = [0.1, 0.2, 0.6]
        state.laser_scan_callback(msg)

        output = state.execute(None)
        self.assertEqual(output, 'possible_collision')

    def test_timeout_no_msg(self):
        node = rclpy.create_node('test')
        state = MonitorBatteryAndCollision(node, battery_threshold=30,
                                           collision_threshold_distance=0.5, timeout=2)

        output = state.execute(None)
        self.assertEqual(output, 'timeout')

    def test_timeout_no_collision_no_low_battery(self):
        node = rclpy.create_node('test')
        state = MonitorBatteryAndCollision(node, battery_threshold=30,
                                           collision_threshold_distance=0.5, timeout=2)
        # high batter and no collision condition
        msg = LaserScan()
        msg.ranges = [0.8, 0.9, 0.6]
        state.laser_scan_callback(msg)
        msg = String()
        msg.data = '90'
        state.battery_callback(msg)

        output = state.execute(None)
        self.assertEqual(output, 'timeout')


class TestRotateBase(unittest.TestCase):
    def setUp(self):
        rclpy.init()

    def tearDown(self):
        rclpy.shutdown()

    def test_rotate(self):
        node = rclpy.create_node('test')
        state = RotateBase(node)

        outcome = state.execute(None)
        self.assertEqual(outcome, 'succeeded')


class TestStopBase(unittest.TestCase):
    def setUp(self):
        rclpy.init()

    def tearDown(self):
        rclpy.shutdown()

    def test_stop(self):
        node = rclpy.create_node('test')
        state = StopBase(node)

        outcome = state.execute(None)
        self.assertEqual(outcome, 'succeeded')


if __name__ == '__main__':
    unittest.main()
