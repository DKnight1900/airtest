#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
2014/07/20 jiaqianghuai: 代码注释
'''

__author__ = 'hzjiaqianghuai,hzsunshx'
import time
import math

import numpy as np
import cv2
import os


MIN_MATCH_COUNT = 5
MIN_MATCH = 15
Debug = os.getenv('DEBUG') == 'true'

# Euclidean distance calculation
def distance(p1, p2):
    l2 = (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])
    return math.sqrt(l2)


# remove the duplicate element of the list
def reremove(list):
    """ order preserving """
    checked = []
    for e in list:
        if e not in checked:
            checked.append(e)
    return checked


# color hist based similarity calculation
def hist_similarity(img1, img2):
    # img1 = cv2.imread(origin,1) # queryImage,gray
    #img2 = cv2.imread(query,1) # originImage,gray
    try:
        if img1.ndim == 2 & img2.ndim == 2:
            hist1 = cv2.calcHist([img1], [0], None, [256], [0.0, 255.0])
            hist2 = cv2.calcHist([img2], [0], None, [256], [0.0, 255.0])
            retal = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CORREL)
        elif img1.ndim == 3 & img2.ndim == 3:
            ''' R,G,B split '''
            b1, g1, r1 = cv2.split(img1)
            b2, g2, r2 = cv2.split(img2)
            hist_b1 = cv2.calcHist([b1], [0], None, [256], [0.0, 255.0])
            hist_g1 = cv2.calcHist([g1], [0], None, [256], [0.0, 255.0])
            hist_r1 = cv2.calcHist([r1], [0], None, [256], [0.0, 255.0])
            hist_b2 = cv2.calcHist([b2], [0], None, [256], [0.0, 255.0])
            hist_g2 = cv2.calcHist([g2], [0], None, [256], [0.0, 255.0])
            hist_r2 = cv2.calcHist([r2], [0], None, [256], [0.0, 255.0])
            retal_b = cv2.compareHist(hist_b1, hist_b2, cv2.cv.CV_COMP_CORREL)
            retal_g = cv2.compareHist(hist_g1, hist_g2, cv2.cv.CV_COMP_CORREL)
            retal_r = cv2.compareHist(hist_r1, hist_r2, cv2.cv.CV_COMP_CORREL)
            sum_bgr = retal_b + retal_g + retal_r
            retal = sum_bgr / 3
        else:
            img1 = cv2.cvtColor(img1, cv2.cv.CV_RGB2GRAY)
            img2 = cv2.cvtColor(img2, cv2.cv.CV_RGB2GRAY)
            hist1 = cv2.calcHist([img1], [0], None, [256], [0.0, 255.0])
            hist2 = cv2.calcHist([img2], [0], None, [256], [0.0, 255.0])
            retal = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CORREL)
        return retal
    except:
        return None


# SIFT or SURF based similarity calculation
def feature_similarity(img1, img2):
    # img1 = cv2.imread(query,0) # queryImage,gray
    #img2 = cv2.imread(origin,0) # originImage,gray
    #print "Hello"
    try:
        ''' find the keypoints and descriptors with SIFT '''
        kp1, des1 = siftextract(img1)
        kp2, des2 = siftextract(img2)

    except:
        return []
    kpnum1 = len(kp1)
    kpnum2 = len(kp2)
    #print kpnum1,kpnum2
    if kpnum1 <= kpnum2:
        kpnum = kpnum1
    else:
        kpnum = kpnum2
    #print kpnum
    if kpnum <= 0:
        retal = 0.0
        return retal
    ''' search the match keypoints '''
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        ''' threshold = 0.7 '''
        if m.distance < 0.7 * n.distance:
            good.append(m)
    kpnum_good = float(len(good))
    #print "Good Num: ", kpnum_good
    retal = kpnum_good / kpnum
    return retal


def re_feature_similarity(kp1, des1, kp2, des2):
    # img1 = cv2.imread(query,0) # queryImage,gray
    #img2 = cv2.imread(origin,0) # originImage,gray
    kpnum1 = len(kp1)
    kpnum2 = len(kp2)
    #print kpnum1,kpnum2
    if kpnum1 <= kpnum2:
        kpnum = kpnum1
    else:
        kpnum = kpnum2
    #print kpnum
    if kpnum <= 0:
        retal = 0.0
        return retal
    ''' search the match keypoints '''
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        ''' threshold = 0.7 '''
        if m.distance < 0.7 * n.distance:
            good.append(m)
    kpnum_good = float(len(good))
    #print "Good Num: ", kpnum_good
    retal = kpnum_good / kpnum
    return retal


# 查询图片边缘的像素赋值为0，主要是处理那些背景为透明的图片
def imgprocess(img, ratio):
    h = img.shape[0]
    w = img.shape[1]
    h_t = int(h * ratio)
    w_t = int(w * ratio)
    #print "h_t: %d, w_t: %d" % (h_t,w_t)
    h_b = h - h_t
    w_b = w - w_t
    for i in range(h):
        for j in range(w):
            if (img.ndim == 2) & ((i < h_t) | (j < w_t) | (h_b < i) | (w_b < j)):
                if 200 < img[i, j]:
                    img[i, j] = 0
            elif (img.ndim == 3) & ((i < h_t) | (j < w_t) | (h_b < i) | (w_b < j)):
                graylevel = int((img[i, j, 0] + img[i, j, 1] + img[i, j, 2]) / 3)
                if 200 < graylevel:
                    img[i, j, 0] = 0
                    img[i, j, 1] = 0
                    img[i, j, 2] = 0
    return img


#复制图像
def copyimg(center, w, h, target_img, num):
    center_x = center[0]
    center_y = center[1]
    topleft_x = int(center_x - w)
    topleft_y = int(center_y - h)
    #print "tx, ty: ", topleft_x, topleft_y
    if topleft_x < 0:
        topleft_x = 0
    if topleft_y < 0:
        topleft_y = 0
    #print "ndim: ",target_img.ndim
    if target_img.ndim == 2:
        rect_img = np.zeros((h * num, w * num), target_img.dtype)
        for i in range(h * num):
            ty = topleft_y + i
            if target_img.shape[0] <= ty:
                ty = target_img.shape[0] - 1
            for j in range(w * num):
                tx = topleft_x + j
                if target_img.shape[1] <= tx:
                    tx = target_img.shape[1] - 1
                rect_img[i][j] = target_img[ty][tx]
    elif target_img.ndim == 3:
        rect_img = np.zeros((h, w, 3), target_img.dtype)
        for i in range(h):
            ty = topleft_y + i
            for j in range(w):
                tx = topleft_x + j
                if target_img.shape[0] <= ty:
                    ty = target_img.shape[0] - 1
                if target_img.shape[1] <= tx:
                    tx = target_img.shape[1] - 1
                rect_img[i][j][0] = target_img[ty][tx][0]
                rect_img[i][j][1] = target_img[ty][tx][1]
                rect_img[i][j][2] = target_img[ty][tx][2]
    return rect_img


# template match function，这里加了图像灰度阈值处理
def templatematch(target_img, query_img, value, situ, center):
    h_query = query_img.shape[0]
    w_query = query_img.shape[1]
    #print "w_query:%d, h_query:%d" % (w_query,h_query)
    w_temp = int(w_query / 1)
    h_temp = int(h_query / 1)
    #print "w2:%d, h2:%d" % (w_temp,h_temp)
    size = (w_temp, h_temp)
    temp = cv2.resize(query_img, size, cv2.cv.CV_INTER_LINEAR)
    h_target = target_img.shape[0]
    w_target = target_img.shape[1]
    #print "w_target:%d, h_target:%d" % (w_target,h_target)
    width = w_target - w_temp + 1
    height = h_target - h_temp + 1
    if width < 0 | height < 0:
        return None
    t_ret, t_thresh = cv2.threshold(target_img, 200, 255, cv2.THRESH_TOZERO)
    q_ret, q_thresh = cv2.threshold(query_img, 200, 255, cv2.THRESH_TOZERO)
    #result=np.zeros((width,height),np.uint8)
    #cv.MatchTemplate(image,template, result,cv.CV_TM_SQDIFF_NORMED)
    #result = cv2.matchTemplate(target_img,temp,cv2.cv.CV_TM_SQDIFF_NORMED)
    result = cv2.matchTemplate(t_thresh, q_thresh, cv2.cv.CV_TM_CCORR_NORMED)
    (min_val, max_val, minloc, maxloc) = cv2.minMaxLoc(result)
    #(x,y)=minloc
    (x, y) = maxloc
    if len(center):
        re_x = int(x + center[0] - w_temp / 2)
        re_y = int(y + center[1] - h_temp / 2)
    else:
        re_x = int(x + w_temp / 2)
        re_y = int(y + h_temp / 2)
    maxloc = [re_x, re_y]
    value.append(max_val)
    situ.append(maxloc)


def origin_templatematch(target_img, query_img):
    h_query = query_img.shape[0]
    w_query = query_img.shape[1]
    h_target = target_img.shape[0]
    w_target = target_img.shape[1]
    #print "w_target:%d, h_target:%d" % (w_target,h_target)
    width = w_target - w_query + 1
    height = h_target - h_query + 1
    if width < 0 | height < 0:
        return None
    result = cv2.matchTemplate(target_img, query_img, cv2.cv.CV_TM_CCORR_NORMED)
    (min_val, max_val, minloc, maxloc) = cv2.minMaxLoc(result)
    #(x,y)=minloc
    (x, y) = maxloc
    return max_val


def siftextract(target_img):
    # Initiate SIFT detector
    sift = cv2.SIFT()
    # find the keypoints and descriptors with SIFT
    kp, des = sift.detectAndCompute(target_img, None)
    return kp, des


def _search(des1, des2):
    #search and match the 
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    return matches


# SIFT + Homography
def _homography_match(h, w, kp1, kp2, good, target_img, outfile):
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    #origin_img match keypoints
    r, c, d = dst_pts.shape
    if r < 1:  #不存在匹配点
        return None
    for i in range(r):
        x = dst_pts[i][c - 1][d - 2]
        y = dst_pts[i][c - 1][d - 1]
        cv2.circle(target_img, (int(x), int(y)), 2, (255, 0, 0), -1)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)  #最少需要4个match点
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)  #找到一个变换矩阵，从查询图片映射到检测图片
    row, col, dim = dst.shape
    if row < 1:
        return None
    center = [0, 0]
    count = 0
    for i in range(row):
        if (int(dst[i][col - 1][0]) <= target_img.shape[1]) & (0 <= dst[i][col - 1][0]) & (
                    int(dst[i][col - 1][1]) <= target_img.shape[0]) & (0 <= dst[i][col - 1][1]):
            center += dst[i][col - 1]
            count += 1
            cv2.circle(target_img, (dst[i][col - 1][0], dst[i][col - 1][1]), 2, (255, 0, 255), -1)
    if ((count < 1) | (count <= int(row * 0.5))):  #仿射变换得到的四个坐标，如果至少有两个坐标不在检测图片区域，说明匹配不成功
        return None
    else:
        center_x = int(center[0] / count)
        center_y = int(center[1] / count)
        if outfile:
            cv2.rectangle(target_img, (int(center_x - w / 2), int(center_y - h / 2)),
                          (int(center_x + w / 2), int(center_y + h / 2)), (0, 0, 255), 1, 0)
            cv2.circle(target_img, (center_x, center_y), 2, (0, 255, 0), -1)
            cv2.imwrite(outfile, target_img)
        return [center_x, center_y]


def _re_detectAndmatch(kp_num, kp2_xy, img1, img2, query_img, target_img, outfile):
    h, w = img1.shape
    re_dst_pts = np.float32([kp2_xy[m] for m in range(len(kp2_xy))]).reshape(-1, 1, 2)
    re_r, re_c, re_d = re_dst_pts.shape
    temp = imgprocess(img1, 0.1)
    if re_r:
        value, situ, num = [], [], []
        for i in range(re_r):
            center = re_dst_pts[i][re_c - 1]
            rect_img = copyimg(center, w, h, img2, 2)
            tp = feature_similarity(rect_img, img1)
            num.append(tp)
            templatematch(rect_img, temp, value, situ, center)
        max = value[re_r - 1]
        k = re_r - 1
        for i in range(re_r - 1):
            #print "value: ", value[i]
            if max < value[i]:
                max = value[i]
                k = i
        if Debug:
            print k, max, num[k]
        if (0.18 < num[k]):
            if (max <= 0.6) & (5 < kp_num):
                center, value, situ = [], [], []
                templatematch(img2, temp, value, situ, center)
                if value[0] < 0.7:  #template similarity
                    return None
                else:
                    center_x = situ[0][0]
                    center_y = situ[0][1]
                    rect_img = copyimg((center_x, center_y), w, h, target_img, 1)
                    value = hist_similarity(rect_img, query_img)
                    if (value < 0.03):
                        return None
            else:
                center_x = situ[k][0]
                center_y = situ[k][1]
                if (max < 0.9):
                    rect_img = copyimg((center_x, center_y), w, h, target_img, 1)
                    rect_img2 = copyimg((center_x, center_y), w, h, img2, 2)
                    val = hist_similarity(rect_img, query_img)
                    val2 = feature_similarity(rect_img2, img1)
                    print val, val2
                    if (val < 0.03) | (val2 < 0.15):  #
                        return None
        else:
            if ((0.9 < max) & (0.09 < num[k])):
                center_x = situ[k][0]
                center_y = situ[k][1]
            else:
                return None
    else:
        center, value, situ = [], [], []
        templatematch(img2, temp, value, situ, center)
        #print "value", value
        if value[0] < 0.7:  #template similarity
            return None
        else:
            center_x = situ[0][0]
            center_y = situ[0][1]
    top_x = int(center_x - w / 2)
    top_y = int(center_y - h / 2)
    print top_x, top_y
    if (top_x < 0) | (top_y < 0):
        return None
    if outfile:
        cv2.rectangle(target_img, (int(center_x - w / 2), int(center_y - h / 2)),(int(center_x + w / 2), int(center_y + h / 2)), (0, 0, 255), 1, 0)
        cv2.circle(target_img, (center_x, center_y), 2, (0, 255, 0), -1)
        cv2.imwrite(outfile, target_img)
    return [center_x, center_y]


def _refine_center(list_x, list_y):
    center_sum_x, center_sum_y, count = 0, 0, 0
    #duplicate removal
    rlist_x = reremove(list_x)
    rlist_y = reremove(list_y)
    if len(rlist_x) < 1:
        return None
    rx_len = len(rlist_x)
    ry_len = len(rlist_y)
    if rx_len == ry_len:
        x_list = rlist_x
        y_list = rlist_y
        for i in range(rx_len):
            center_sum_x += x_list[i]
            center_sum_y += y_list[i]
            count += 1
    else:
        x_list = list_x
        y_list = list_y
        for i in range(len(x_list)):
            center_sum_x += x_list[i]
            center_sum_y += y_list[i]
            count += 1
    center_x = int(center_sum_x / count)
    center_y = int(center_sum_y / count)
    temp = [center_x, center_y]
    dist = []
    max, rcount = 0, 0
    rcenter = [0, 0]
    for i in range(count):
        #dis = abs(center_x-rlist_x[i])+abs(center_y-rlist_y[i])
        dis = distance(temp, [x_list[i], y_list[i]])
        if max < dis:
            max = dis
        dist.append(dis)
    for i in range(count):
        if count <= 2:
            rcenter[0] += x_list[i]
            rcenter[1] += y_list[i]
            rcount += 1
        else:
            if dist[i] < max:
                rcenter[0] += x_list[i]
                rcenter[1] += y_list[i]
                rcount += 1
    return rcenter[0], rcenter[1], rcount


def locate_image(orig, quer, outfile='debug.png', threshold=0.3):
    pt = locate_one_image(orig, quer, outfile, threshold)
    if pt:
        return [pt]
    return None


def locate_one_image(origin='origin.png', query='query.png', outfile='match.png', threshold=0.3):
    '''
    Locate one image position

    @param origin: string (target filename)
    @param query: string (image need to search)
    @param threshold: float (range [0, 1), the lower the more ease to match)
    @return None if not found, (x,y) point if found
    '''
    import os

    if not os.path.exists(origin):
        raise IOError('origin_file not exists')
    if not os.path.exists(query):
        raise IOError('query_file not exists')
    threshold = 1 - threshold
    img1 = cv2.imread(query, 0)  # queryImage,gray
    img2 = cv2.imread(origin, 0)  # originImage,gray
    query_img = cv2.imread(query, 1)  # queryImage
    target_img = cv2.imread(origin, 1)  # originImage
    try:
        # find the keypoints and descriptors with SIFT
        kp1, des1 = siftextract(img1)
        kp2, des2 = siftextract(img2)
        num1 = len(kp1)
        num2 = len(kp2)
        if num2 < num1:
            return None
    except:
        return None

    h, w = img1.shape
    '''提前过滤，排除那些肯定不存在查询图片的测试图片'''
    v1 = []
    s1 = []
    templatematch(img2, img1, v1, s1, [])  #全局模板匹配
    c1 = s1[0]
    rect = copyimg((c1[0], c1[1]), w, h, img2, 2)  #复制潜在匹配区域
    kp3, des3 = siftextract(rect)
    num3 = len(kp3)
    if num1 <= num3:
        val2 = re_feature_similarity(kp1, des1, kp3, des3)
        if Debug:
            print "val: ", val2
        if (int(num1*5) <= num3) and (MIN_MATCH < num1):
            if (val2 == 0.0): 
                return None
    ratio_num = int(num1 * 0.1)
    '''store all the good matches as per Lowe's ratio test.'''
    matches = _search(des1, des2)
    good,kp2_xy = [],[]
    for m, n in matches:
        kp2_xy.append(kp2[m.trainIdx].pt)
        if m.distance < threshold * n.distance:  # threshold = 0.7
            good.append(m)
    if len(good) > MIN_MATCH_COUNT:  #good matches的数量超过给定阈值，则进行Homography
        center = _homography_match(h, w, kp1, kp2, good, target_img, outfile)
        if Debug:
            print "center: ",center
        return center
    else:
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        row, col, dim = dst_pts.shape
        if (row < 1) | (row < ratio_num) | ((row == 1) & (ratio_num == 1)):
            center = _re_detectAndmatch(num1, kp2_xy, img1, img2, query_img, target_img, outfile)
            if Debug:
                print "center: ",center
            return center
        else:
            list_x, list_y = [], []
            for i in range(row):
                x = dst_pts[i][col - 1][dim - 2]
                y = dst_pts[i][col - 1][dim - 1]
                list_x.append(int(x))
                list_y.append(int(y))
                cv2.circle(target_img, (int(x), int(y)), 2, (255, 0, 0), -1)
            rcenter_x, rcenter_y, rcount = _refine_center(list_x, list_y)
            if rcount < 1:
                return None
            else:
                center_x = int(rcenter_x / rcount)
                center_y = int(rcenter_y / rcount)
                top_x = int(center_x - w / 2)
                top_y = int(center_y - h / 2)
                if (top_x < 0) & (top_y < 0):
                    return None
                if outfile:
                    cv2.rectangle(target_img, (int(center_x - w / 2), int(center_y - h / 2)),
                              (int(center_x + w / 2), int(center_y + h / 2)), (0, 0, 255), 1, 0)
                    cv2.circle(target_img, (center_x, center_y), 2, (0, 255, 0), -1)
                    cv2.imwrite(outfile, target_img)
                if Debug:
                    print "center: ",[center_x, center_y]
                return [center_x, center_y]


if __name__ == '__main__':
    starttime = time.clock()
    pts = locate_image('testdata/target.png', 'testdata/query.png', 'testdata/debug.png', 0.3)
    endtime = time.clock()
    print "time: ", endtime - starttime
    print "center point: ", pts
    if pts:
        center_x = pts[0][0]
        center_y = pts[0][1]
        point = []
        #read the location information of the object in the origin image
        with open('testdata/data.txt', 'r') as f:
            for line in f:
                point.append(map(float, line.split(',')))
                #print point
        pt = point[0]
        #object top_left coordinate
        topleft_x = int(pt[0])
        topleft_y = int(pt[1])
        #print topleft_x, topleft_y
        #object bottom_right corrdinate
        bottomright_x = int(pt[2])
        bottomright_y = int(pt[3])
        #print bottomright_x, bottomright_y
        if (topleft_x <= center_x & center_x <= bottomright_x) & (topleft_y <= center_y & center_y <= bottomright_y):
            print "Match Successfully !!!"
        else:
            print "Match Failure !!!"
    else:
        print "No object"
