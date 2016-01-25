__author__ = 'missoni'


class LiveWireSegmentation(object):
    def __init__(self, image=None):
        super(LiveWireSegmentation, self).__init__()
        self.image = image
        self.edges = None
        self.thresholded_edges = None
        self.G = None

    # def _smooth_image(self):
    #     from skimage import restoration
    #     self.image = restoration.denoise_bilateral(self.image)

    def _compute_gradient_image(self):
        from skimage import filters
        self.edges = filters.scharr(self.image)

    def _threshold_gradient_image(self):
        from skimage.filters import threshold_otsu
        threshold = threshold_otsu(self.edges)
        self.edges = self.edges > threshold

    def _compute_graph(self):
        from math import fabs

        self.G = {}
        rows, cols = self.edges.shape
        for col in range(cols):
            for row in range(rows):

                neighbors = []
                if row > 0:
                    neighbors.append( (row-1, col) )

                if row < rows-1:
                    neighbors.append( (row+1, col) )

                if col > 0:
                    neighbors.append( (row, col-1) )

                if col < cols-1:
                    neighbors.append( (row, col+1) )

                dist = {}
                for n in neighbors:
                    # distance function can be replaced with a different norm
                    dist[n] = fabs(self.edges[row][col] - self.edges[n[0], n[1]])

                self.G[(row, col)] = dist

    def compute_shortest_path(self, from_, to_, length_penalty=0.0):
        if self.image is None:
            raise AttributeError("Load an image first!")

        # not implemented yet!
        #self.smooth_image()

        if self.edges is None:
            self._compute_gradient_image()

        if self.thresholded_edges is None:
            self._threshold_gradient_image()

        if self.G is None:
            self._compute_graph()

        from dijkstra import shortestPath
        path = shortestPath(self.G, from_, to_, length_penalty=length_penalty)

        return path