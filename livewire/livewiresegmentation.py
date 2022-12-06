import math
from typing import Tuple
from .dijkstra import shortestPath
import numpy as np

class LiveWireSegmentation(object):
    # image: PIL obj, smooth_image: bool, default False, threshold_gradient_image: bool, default False
    def __init__(self, image=None, dl_util = None, smooth_image=False, threshold_gradient_image=False):        
        super(LiveWireSegmentation, self).__init__()

        # init internal containers
        self.image_color = image
        image = image.convert('L')  # PIL image
        image = np.array(image)
        # container for input image
        self._image = None

        # container for the gradient image
        self.edges = None

        # stores the image as an undirected graph for shortest path search
        self.G = None

        # init parameters

        # should smooth the original image using bilateral smoothing filter
        self.smooth_image = smooth_image

        # should use the thresholded gradient image for shortest path computation
        self.threshold_gradient_image = threshold_gradient_image

        # whether use deep learning segmentation for grad compute
        self.dl_util = dl_util

        # init image

        # store image and compute the gradient image
        self.image = image



    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

        if self._image is not None:
            if self.smooth_image:
                self._smooth_image()

            self._compute_gradient_image()

            if self.threshold_gradient_image:
                self._threshold_gradient_image()

            self._compute_graph()

        else:
            self.edges = None
            self.G = None

    def _smooth_image(self):
        from skimage import restoration
        self._image = restoration.denoise_bilateral(self.image)

    def _compute_gradient_image(self):
        from skimage import filters,morphology
        self.edges = filters.scharr(self._image)
        # deep learning utils
        if self.dl_util is not None:
            from skimage import color,transform
            image2 = self.dl_util.seg_main(self.image_color)
            image2 = color.rgb2gray(image2)
            image2 = transform.resize(image2,self._image.shape)
            # print('img shape:',self._image.shape,'color_shape:',image2.shape)
            edges2 = filters.scharr(image2)   
            # self.edges = edges2         
            self.edges = 0.5*self.edges+0.5*edges2
            self.edges.astype(np.uint8)
            
        self.edges = morphology.dilation(self.edges)

    def _threshold_gradient_image(self):
        from skimage.filters import threshold_otsu
        threshold = threshold_otsu(self.edges)
        self.edges = self.edges > threshold
        self.edges = self.edges.astype(float)
    
    def _norm_function(self,a,b,mean)->int:
        a = a/mean
        b = b/mean
        return 1/max(a*b,0.0001)

    def _compute_graph(self, norm_function=math.fabs):
        norm_function = self._norm_function
        self.G = {}
        rows, cols = self.edges.shape
        mean_val = self.edges.mean()
        # MAYBE optimized by matrix calculate
        for col in range(cols):
            for row in range(rows):
                # 8-direction graph
                neighbors = []
                neighbors_diag = []
                if row > 0:
                    neighbors.append((row-1, col))
                    # if col < cols - 1:
                    #     neighbors_diag.append((row-1,col+1))

                if row < rows-1:
                    neighbors.append((row+1, col))
                    if col > 0:
                        neighbors_diag.append((row+1,col-1))

                if col > 0:
                    neighbors.append((row, col-1))
                    if row > 0:
                        neighbors_diag.append((row-1,col-1))

                if col < cols-1:
                    neighbors.append((row, col+1))
                    # if row < rows-1:
                    #     neighbors_diag.append((row+1,col+1))

                dist = {}
                for n in neighbors:
                    # distance function can be replaced with a different norm
                    dist[n] = norm_function(self.edges[row][col],self.edges[n[0], n[1]],mean_val)  

                for m in neighbors_diag:
                    dist[m] = norm_function(self.edges[row][col],0.57*self.edges[m[0], m[1]],mean_val) 
                
                self.G[(row, col)] = dist

    def best_seed(self,loc)->Tuple:
    # input cursor's location (row,col) then find the best possible seed within 5x5 area
        x,y = loc
        rows, cols = self.edges.shape
        x1 = max(0,x-4)
        x2 = min(rows-1,x+4)
        y1 = max(0,y-4)
        y2 = min(cols+1,y+4)
        slice_area = self.edges[x1:(x2+1),y1:(y2+1)]
        index = np.unravel_index(slice_area.argmax(), slice_area.shape)
        index = list(index)
        index[0] = index[0]+x1
        index[1] = index[1]+y1
        index = tuple(index)
        return index
    


    def compute_shortest_path(self, from_, to_, length_penalty=0.0):
        if self.image is None:
            raise AttributeError("Load an image first!")

        path = shortestPath(self.G, from_, to_, length_penalty=length_penalty)

        return path
