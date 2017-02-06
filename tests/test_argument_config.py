import unittest
from ratioexemplaris import ArgumentConfig

class TestArgumentConfig(unittest.TestCase):

	def setUp(self):
		self.instance = ArgumentConfig()

	def test_assign_values(self):
		self.instance.test = 'TEST';
		self.assertEqual(self.instance.test, 'TEST')

	def test_register_config(self):
		pass


if __name__ == '__main__':
    unittest.main()