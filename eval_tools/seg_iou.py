#计算IOU 注意两个输入图片尺寸必须一样
from PIL import Image
import numpy as np
import glob

def get_array(path):
    img = Image.open(path).convert('L')
    img = img.getdata()
    img = np.array(img)
    return img

def get_IOU(maskpath,resultpath):
    mask = get_array(maskpath)
    result = get_array(resultpath)
    #计算iou
    S1 = 0 #交集
    S2 = 0 #并集
    S3 = 0
    S4 = 0
    for i in range(len(mask)):
        #print(result[i])
        thresold_gray = 30
        if mask[i]>thresold_gray and result[i]>thresold_gray:##0~255为由黑到白，根据图片情况自行调整
            S1 = S1 + 1
        if mask[i]>thresold_gray or result[i]>thresold_gray:
            S2 = S2 + 1
        if mask[i] < thresold_gray and result[i] < thresold_gray:
            S3=S3+1
        if mask[i] < thresold_gray or result[i] < thresold_gray:
            S4=S4+1
    iou = S1/S2
    iouf=S3/S4
    miou=(iou+iouf)/2
    return iou,miou

def main():
    n = 0
    mask_path = "test//mask"
    result_path = "test//results"
    iou_sum  = 0
    miou_sum = 0
    for file in glob.glob(mask_path+"//*.png"): ##计算出有多少张图片
        n = n + 1
    ious = []
    mious = []
    for i in range(n): ##计算单张图片的IOU
        iou, miou = get_IOU(mask_path+"//"+str(i)+".png",result_path+"//"+str(i)+".png")
        ious.append(iou)
        mious.append(miou)
    for i in range(n):
        iou_sum = ious[i]+iou_sum
        miou_sum = mious[i] + miou_sum
    AverageIOU = iou_sum/(n)
    AverageMIOU = miou_sum / (n)
    print('===')
    print(AverageIOU)
    print(AverageMIOU)

def single():
    loc=input("Drag your picture here(special UTF-8 in path is not availiable)->")
    loc=loc.replace("\\","/")
    loc=loc.replace("\"","")

    loc1=input("Drag your picture here(special UTF-8 in path is not availiable)->")
    loc1=loc1.replace("\\","/")
    loc1=loc1.replace("\"","")

    AverageIOU, AverageMIOU = get_IOU(loc,loc1)
    print('===')
    print('AverageIOU:',AverageIOU)
    # print(AverageMIOU)

if __name__ == '__main__':
    single()

