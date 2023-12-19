import unittest
 
def list_sum(my_list):
    # Sums the elements of the list
    return sum(my_list)
 
class MyTestClass(unittest.TestCase):
    def test_list(self):
        # Checks if the sum of the below list is as expected
        my_list = [1, 2, 3, 4, 5]
        self.assertEqual(list_sum(my_list), 15, "Should be 15")
 
    def test_string(self):
        # Checks if the string is 'Hello from AskPython'
        my_str = 'Hi'
        self.assertEqual(my_str, 'Hello from AskPython', "Should be 'Hello from AskPython'")
 
 
if __name__ == '__main__':
    # Main module
    unittest.main()