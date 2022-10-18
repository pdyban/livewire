import torch
import torch.nn as nn
import numpy as np
from torchvision import models
import torchvision.transforms as T 
from PIL import Image

class Dlseg(object):
    def __init__(self,model,pth_file = None) -> None:
        super(Dlseg, self).__init__()
        self.model = model
        self.model = nn.DataParallel(self.model)
        self.model = self.model.cuda()

    def seg_main(self,img)->np.ndarray: # PIL image
        # Apply the transformations needed 
        trf = T.Compose([
        T.Resize(224), 
        # T.CenterCrop(224), 
        T.ToTensor(), 
        T.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])]) 
        img = img.convert("RGB")
        img = trf(img).unsqueeze(0)
        self.model.eval()
        with torch.no_grad():
            out = self.model(img.cuda())['out']
        om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
        om = self.decode_img(om)
        return om

    def decode_img(self,image, nc=21):
    # Define the helper function
        label_colors = np.array([(0, 0, 0),  # 0=background
                    # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                    (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                    # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                    (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
                    # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                    (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
                    # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                    (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])
        r = np.zeros_like(image).astype(np.uint8)
        g = np.zeros_like(image).astype(np.uint8)
        b = np.zeros_like(image).astype(np.uint8)
        for l in range(0, nc):
            idx = image == l
            r[idx] = label_colors[l, 0]
            g[idx] = label_colors[l, 1]
            b[idx] = label_colors[l, 2]
        rgb = np.stack([r, g, b], axis=2)
        return rgb



