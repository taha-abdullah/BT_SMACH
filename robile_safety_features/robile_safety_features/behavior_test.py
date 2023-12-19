from behaviors import rotate, stop_motion, battery_status2bb, laser_scan_2bb
import unittest
import rclpy
import py_trees
class TestRotate(unittest.TestCase):
    def __init__(self, name="rotate_test", topic_name="/cmd_vel", ang_vel=1.0, node = None):
        self.name = name
        self.topic_name = topic_name
        self.ang_vel = ang_vel
        self.node = node


    def test_rotate_behavior(self):
        rotate_behavior = rotate(self.name)
        rotate_behavior.setup(node=self.node, topic_name=self.topic_name, ang_vel=self.ang_vel)

        # Ensure the behavior is initialized correctly
        self.assertEqual(rotate_behavior.name, self.name)
        self.assertEqual(rotate_behavior.topic_name, self.topic_name)
        self.assertEqual(rotate_behavior.ang_vel, self.ang_vel)
        self.assertFalse(rotate_behavior.sent_goal)

        # Test the update method
        status = rotate_behavior.update()
        self.assertEqual(status, py_trees.common.Status.RUNNING)

        # Test the terminate method
        new_status = py_trees.common.Status.SUCCESS
        terminate_status = rotate_behavior.terminate(new_status)
        self.assertEqual(terminate_status, py_trees.common.Status.SUCCESS)

def main():
    rclpy.init()
    node = rclpy.create_node('safety_features_node')
    rotation_behaviour = TestRotate(name = 'test_rotation', node = node)


if __name__ == '__main__':
    main()
 
