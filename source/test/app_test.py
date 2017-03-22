import unittest
from emis_monitor import create_app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True


    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
