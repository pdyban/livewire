from .livewiresegmentation import LiveWireSegmentation
import numpy as np

class Trackmanager(object):
    def __init__(self,image,step = 20,smooth_image=False,threshold_gradient_image=False,dl_util=None,length_penalty = 10.0) -> None:
        super(Trackmanager,self).__init__()
        self.algorithm = LiveWireSegmentation(image,dl_util=dl_util,smooth_image=smooth_image, threshold_gradient_image=threshold_gradient_image)
        self.length_penalty  = length_penalty

        self.step = step
        self.ini_point = None
        self.start_point = None
        self.end_point = None
        self.seed_points_list = []
        self.all_points_list = []
        self.tmp_path = []

    def clear(self):
        self.ini_point = None
        self.start_point = None
        self.end_point = None
        self.seed_points_list = []
        self.all_points_list = []
        self.tmp_path = []

    def get_path(self):
        # flatten the path
        return [item for sublist in self.all_points_list for item in sublist]
    
    def get_seeds(self):
        return self.seed_points_list
    
    def set_start(self,start_point):
        self.start_point = start_point
        self.ini_point = start_point

    def add_path(self,start_point,end_point):
        path = self.algorithm.compute_shortest_path(start_point, end_point, length_penalty=self.length_penalty)
        return path

    def add_tmp_path(self,end_point):
        path = self.algorithm.compute_shortest_path(self.start_point, end_point, length_penalty=self.length_penalty)
        call_refresh = False
        if len(path)>self.step:
            call_refresh = True
            self.end_point = self.algorithm.best_seed(end_point)
            self.update_points(self.end_point)
        return path,call_refresh

    def update_points(self,end_point):
        path = self.algorithm.compute_shortest_path(self.start_point, end_point, length_penalty=self.length_penalty)
        self.end_point = end_point
        self.start_point = self.end_point
        self.all_points_list.append(path)
        self.seed_points_list.append(self.start_point)

    def back_step(self):
        if len(self.seed_points_list)!=0:
            self.seed_points_list.pop()
        if len(self.all_points_list)!=0:
            self.all_points_list.pop()
        if self.seed_points_list == []:
            self.start_point = None
        else:
            self.start_point = self.seed_points_list[-1]
        # remember to refresh frame!
         
    def close_poly(self):
        self.update_points(self.ini_point)