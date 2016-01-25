from unittest import TestCase
from livewire import LiveWireSegmentation
from dicom import read_file
from skimage import img_as_int


class MainUnitTest(TestCase):
    def setUp(self):
        df = read_file('lung.dcm')
        self.test_image = img_as_int(df.pixel_array)

    def tearDown(self):
        pass

    def test_compute_shortest_path(self):
        from_ = (0, 0)
        to_ = (1, 1)
        algorithm = LiveWireSegmentation(self.test_image)
        path = algorithm.compute_shortest_path(from_, to_, length_penalty=0.0)
        self.assertListEqual(path, [(0, 0), (0, 1), (1, 1)], "Optimal path is not as expected")
        print path
