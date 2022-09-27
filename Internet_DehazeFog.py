import math
import time
import cv2
import itertools
import numpy as np


def Dark_img(image):    # 此处返回的是灰度图
    """
    求暗通道图像
    :param image: 读取到的原图
    :return: 经过三通道最小值处理以及最小值滤波的暗通道灰度图
    """
    '''rgb三通道中取最小值'''
    min_img = np.copy(image)
    for h in range(min_img.shape[0]):
        for w in range(min_img.shape[1]):
            for c in range(min_img.shape[2]):
                min_img[h, w, c] = np.min(min_img[h, w, c:c + 3])
    '''再进行一个最小值滤波 方盒大小为15'''
    dark_img = np.copy(min_img)
    dark_img = cv2.cvtColor(dark_img, cv2.COLOR_BGR2GRAY)
    r = 15
    for h in range(dark_img.shape[0]):
        for w in range(dark_img.shape[1]):
            if (h+r) >= dark_img.shape[0]:
                dark_img[h, w] = np.min(dark_img[h:dark_img.shape[0], w:w + r])
            if (w+r) >= dark_img.shape[1]:
                dark_img[h, w] = np.min(dark_img[h:h+r, w:dark_img.shape[1]])
            if (h+r) < dark_img.shape[0] and (w+r) < dark_img.shape[1]:
                dark_img[h, w] = np.min(dark_img[h:h + r, w:w + r])
    # cv2.imshow('dark_img', dark_img)
    return dark_img


def Guided_img(I, p, winSize, eps):
    """
    导向滤波
    :param I: 原图的灰度图/255.0，以此为导向
    :param p: 最小值处理后的按通道图/255.0
    :param winSize: 做均值滤波box的大小
    :param eps: 0.001
    :return: 一个灰度图，对暗通道做导向滤波
    """
    mean_I = cv2.blur(I, winSize)       # I的均值平滑
    mean_p = cv2.blur(p, winSize)       # p的均值平滑

    mean_II = cv2.blur(I * I, winSize)  # I*I的均值平滑
    mean_Ip = cv2.blur(I * p, winSize)  # I*p的均值平滑

    var_I = mean_II - mean_I * mean_I   # 方差
    cov_Ip = mean_Ip - mean_I * mean_p  # 协方差

    a = cov_Ip / (var_I + eps)          # 相关因子a
    b = mean_p - a * mean_I             # 相关因子b

    mean_a = cv2.blur(a, winSize)       # 对a进行均值平滑
    mean_b = cv2.blur(b, winSize)       # 对b进行均值平滑

    q = mean_a * I + mean_b
    # cv2.imshow('guided_img', guided_img)
    return np.uint8(np.clip(255 * q, 0, 255))


def A(image, dark_img):
    """
    求对应三通道大气光A的值 取值最小0.1%的像素点计算平均值
    :param image: 原图
    :param dark_img: 暗通道(rgb)
    :return: 大气光的rgb值
    """
    height = image.shape[0]
    width = image.shape[1]
    size = width * height    # 计算图像的总像素点数
    min_part_size = int(max(math.floor(size/1000), 1))      # 取总个数的0.1%
    arr = []
    for row in dark_img:    # 变为一维数组
        arr.extend(row)
    indexes = np.argsort(arr)[::-1]       # 寻找最大像素的下标
    a_sum = np.zeros(3)
    for i, j in itertools.product(range(3), range(min_part_size)):
        # 根据一维数组下标计算对应二维数组下标
        a_sum[i] += image[indexes[j]//width][indexes[j]-width*(indexes[j]//width)][i]
    # 计算平均值
    A = a_sum / min_part_size
    for i in range(3):
        A[i] = int(A[i])
    return A


def tx(guided_img):
    """
    求tx
    :param guided_img: 暗通道导向图(rgb)/255.0
    :return: tx
    """
    return np.clip(1.0 - guided_img*0.95, 0.30, 1.00)


"""
图像去雾——暗通道算法
:param path: 图像路径
:return: none
"""


def Dehaze(image):
    '''读取图像'''
    initial_img = np.copy(image)
    dark_img = Dark_img(image)      # 得到暗通道图像
    guided_img = Guided_img(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)/255.0,
                            dark_img/255.0, (81, 81), 0.001)   # 进行引导滤波
    guided_img = cv2.cvtColor(guided_img, cv2.COLOR_GRAY2BGR)

    A_ = A(guided_img, dark_img)      # 求大气光照A
    tx_ = tx(guided_img/255.0)   # 求tx
    dehaze_img = (initial_img - A_)/tx_ + A_

    cv2.imwrite('dehaze_img.png', dehaze_img)
    time.sleep(1.0)
    return initial_img, cv2.imread('dehaze_img.png', 1)


path = r"D:\26059\Desktop\DehazeFog\test_images\download.jpg"
image = cv2.imread(path, 1)
height = 500
width = int(height * image.shape[0] / image.shape[1])
image = cv2.resize(image, (height, width))
initial, dehaze = Dehaze(image)     # 去雾
cv2.imshow('Dehaze', np.hstack((initial, dehaze)))
cv2.waitKey(0)