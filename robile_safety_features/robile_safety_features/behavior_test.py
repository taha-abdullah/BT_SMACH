from behaviors import rotate, stop_motion, battery_status2bb, laser_scan_2bb
import unittest
import rclpy
import py_trees


class TestRotate(unittest.TestCase):
    def setUp(self):
        rclpy.init()
        self.name = "rotate_test"
        self.topic_name = "/cmd_vel"
        self.ang_vel = 1.0

    def tearDown(self):
        rclpy.shutdown()

    def test_rotate_behavior_values(self):
        node = rclpy.create_node('rotate_test')
        rotate_behavior = rotate(name=self.name, topic_name=self.topic_name, ang_vel=self.ang_vel)
        rotate_behavior.setup(node=node)

        # Ensure the behavior is initialized correctly
        self.assertEqual(rotate_behavior.name, self.name)
        self.assertEqual(rotate_behavior.topic_name, self.topic_name)
        self.assertEqual(rotate_behavior.ang_vel, self.ang_vel)
        self.assertFalse(rotate_behavior.sent_goal)

    def test_rotate_behavior_update(self):
        node = rclpy.create_node('rotate_test')
        rotate_behavior = rotate(name=self.name, topic_name=self.topic_name, ang_vel=self.ang_vel)
        rotate_behavior.setup(node=node)

        # Test the update method
        status = rotate_behavior.update()
        self.assertEqual(status, py_trees.common.Status.RUNNING)


class TestStop(unittest.TestCase):

    def setUp(self):
        rclpy.init()
        self.name = "stop_test"
        self.topic_name = "/cmd_vel"

    def tearDown(self):
        rclpy.shutdown()

    def test_stop_behavior_values(self):
        node = rclpy.create_node('stop_test')
        stop_behavior = stop_motion(name=self.name, topic_name=self.topic_name)
        stop_behavior.setup(node=node)

        # Ensure the behavior is initialized correctly
        self.assertEqual(stop_behavior.name, self.name)
        self.assertEqual(stop_behavior.cmd_vel_topic, self.topic_name)

    def test_stop_behavior_update(self):
        node = rclpy.create_node('stop_test')
        stop_behavior = stop_motion(name=self.name, topic_name=self.topic_name)
        stop_behavior.setup(node=node)

        # Test the update method
        status = stop_behavior.update()
        self.assertEqual(status, py_trees.common.Status.SUCCESS)


class TestBattery(unittest.TestCase):
    def setUp(self):
        rclpy.init()
        self.name = "Battery2BB"
        self.topic_name = "/battery_voltage"
        self.threshold = 30.0

    def tearDown(self):
        rclpy.shutdown()

    def test_battery_low(self):
        battery_status = battery_status2bb(name=self.name, topic_name=self.topic_name,
                                           threshold=self.threshold)
        battery_status.blackboard.battery = 20
        battery_status.update()
        self.assertEqual(battery_status.feedback_message, "Battery level is low")

    def test_battery_ok(self):
        battery_status = battery_status2bb(name=self.name, topic_name=self.topic_name,
                                           threshold=self.threshold)
        battery_status.blackboard.battery = 90
        battery_status.update()
        self.assertEqual(battery_status.feedback_message, "Battery level is ok")


class TestCollision(unittest.TestCase):
    def setUp(self):
        rclpy.init()
        self.name = "Scan2BB"
        self.topic_name = "/scan"
        self.safe_range = 0.25

    def tearDown(self):
        rclpy.shutdown()

    def test_collision(self):
        collision_status = laser_scan_2bb(name=self.name, topic_name=self.topic_name,
                                          safe_range=self.safe_range)
        collision_status.blackboard.laser_scan = [0.1, 0.7, 0.3]
        collision_status.update()
        self.assertEqual(collision_status.blackboard.collison_warning, True)

    def test_no_collision(self):
        collision_status = laser_scan_2bb(name=self.name, topic_name=self.topic_name,
                                          safe_range=self.safe_range)
        collision_status.blackboard.laser_scan = [0.3, 0.5, 0.4]
        collision_status.update()
        self.assertEqual(collision_status.blackboard.collison_warning, False)


if __name__ == '__main__':
    unittest.main()
