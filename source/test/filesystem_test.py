# import copy
import unittest
# from dataset_manager.manage_dataset.scan import Property, rewrite_pathnames


class FilesystemTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    # def test_rewrite_1(self):
    #     properties1 = [
    #         Property("/data/property/NOx.lue", "/blah/nox"),
    #         Property("/data/property/NO2.lue", "/blah/no2")
    #     ]

    #     rewrite_path = None
    #     properties2 = rewrite_pathnames(copy.deepcopy(properties1),
    #         rewrite_path)

    #     self.assertEqual(len(properties2), len(properties1))
    #     self.assertEqual(properties2[0], properties1[0])
    #     self.assertEqual(properties2[1], properties1[1])


    # def test_rewrite_2(self):
    #     properties1 = [
    #         Property("/data/property/NOx.lue", "/blah/nox"),
    #         Property("/data/property/NO2.lue", "/blah/no2")
    #     ]

    #     rewrite_path = []
    #     properties2 = rewrite_pathnames(copy.deepcopy(properties1),
    #         rewrite_path)

    #     self.assertEqual(len(properties2), len(properties1))
    #     self.assertEqual(properties2[0], properties1[0])
    #     self.assertEqual(properties2[1], properties1[1])


    # def test_rewrite_3(self):
    #     properties1 = [
    #         Property("/data/property/NOx.lue", "/blah/nox"),
    #         Property("/data/property/NO2.lue", "/blah/no2")
    #     ]

    #     rewrite_path = [
    #         "/data/property",
    #         "/data/property"
    #     ]
    #     properties2 = rewrite_pathnames(copy.deepcopy(properties1),
    #         rewrite_path)

    #     self.assertEqual(len(properties2), len(properties1))
    #     self.assertEqual(properties2[0], properties1[0])
    #     self.assertEqual(properties2[1], properties1[1])


    # def test_rewrite_4(self):
    #     properties1 = [
    #         Property("/data/property/NOx.lue", "/blah/nox"),
    #         Property("/data/property/NO2.lue", "/blah/no2")
    #     ]

    #     rewrite_path = [
    #         "/data/property",
    #         "/some_other_path"
    #     ]
    #     properties2 = rewrite_pathnames(copy.deepcopy(properties1),
    #         rewrite_path)

    #     self.assertEqual(len(properties2), len(properties1))
    #     self.assertEqual(properties2[0].dataset_pathname,
    #         rewrite_path[1] + "/NOx.lue")
    #     self.assertEqual(properties2[1].dataset_pathname,
    #         rewrite_path[1] + "/NO2.lue")


if __name__ == "__main__":
    unittest.main()
