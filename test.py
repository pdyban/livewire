from unittest import TestCase, main
from livewire import LiveWireSegmentation, compute_shortest_path
from dicom import read_file
from skimage import img_as_int
import numpy as np


class LiveWireSegmentationTest(TestCase):
    def setUp(self):
        df = read_file('images/lung.dcm')
        self.test_image = img_as_int(df.pixel_array)

    def tearDown(self):
        pass

    def test_compute_shortest_path(self):
        from_ = (0, 0)
        to_ = (1, 1)
        algorithm = LiveWireSegmentation(self.test_image)
        path = algorithm.compute_shortest_path(from_, to_, length_penalty=0.0)
        self.assertListEqual(path, [(0, 0), (0, 1), (1, 1)], "Optimal path is not as expected")

    def test_computes_graph_only_once(self):
        from_ = (0, 0)
        to_ = (1, 1)
        algorithm = LiveWireSegmentation(self.test_image)
        first_id = id(algorithm.G)
        path = algorithm.compute_shortest_path(from_, to_)
        prev_id = id(algorithm.G)

        from_ = (10, 10)
        to_ = (11, 11)
        path = algorithm.compute_shortest_path(from_, to_)
        cur_id = id(algorithm.G)
        self.assertEqual(cur_id, prev_id, 'Graph was recomputed even though not requested')
        self.assertEqual(first_id, prev_id, 'Graph was recomputed even though not requested')

    def test_length_penalty_changes_result(self):
        shape = self.test_image.shape
        from_ = (shape[0]/4, shape[1]/4)
        to_ = (shape[0]/2, shape[1]/2)

        algorithm = LiveWireSegmentation(self.test_image)

        path1 = algorithm.compute_shortest_path(from_, to_)
        path2 = algorithm.compute_shortest_path(from_, to_, length_penalty=100.0)
        self.assertNotEqual(len(path1), len(path2), 'Length penalty has had no effect on optimal path')

    def test_can_init_image_later(self):
        algorithm = LiveWireSegmentation(self.test_image)

        algorithm_post = LiveWireSegmentation()
        algorithm_post.image = self.test_image

        self.assertDictEqual(algorithm.G, algorithm_post.G, 'Post-initialization failed')

    def test_can_read_threshold_parameter(self):
        algorithm_with_thresholding = LiveWireSegmentation(self.test_image, threshold_gradient_image=True)
        algorithm_without_thresholding = LiveWireSegmentation(self.test_image, threshold_gradient_image=False)

        self.assertNotEqual(np.linalg.norm(algorithm_with_thresholding.edges),
                            np.linalg.norm(algorithm_without_thresholding.edges),
                            'Gradient image with and without thresholding are the same')


class StandaloneTest(TestCase):
    """
    Tests standalone function compute_shortest_path.
    """
    def setUp(self):
        df = read_file('images/lung.dcm')
        self.test_image = img_as_int(df.pixel_array)

    def tearDown(self):
        pass

    def test_compute_shortest_path(self):
        from_ = (0, 0)
        to_ = (1, 1)
        path_standalone = compute_shortest_path(self.test_image, from_, to_)

        algorithm = LiveWireSegmentation(self.test_image)
        path_class = algorithm.compute_shortest_path(from_, to_, length_penalty=0.0)
        self.assertListEqual(path_standalone, path_class, "Optimal path is not as expected")

if __name__ == '__main__':
    main()
