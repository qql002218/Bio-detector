'''
opencv 划线
'''
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import  os
import test
import time
from collections import deque
import math

import tracker
from detector import Detector



def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

class torch:
    def __init__(self,flag,dic,detector,pxconvert):
        self.list_region = []
        self.list_overlapping_region = []
        self.json = {}
        self.pts = [deque(maxlen=40) for _ in range(9999)]
        self.flag = flag
        self.dic = dic
        self.distRes = {} ##距离结果
        self.precenter = {} ##上下文联系，算每帧的运动距离
        self.detector = detector  #初始化检测器
        self.COLORS = np.random.randint(0, 255, size=(200, 3),
                                    dtype="uint8")
        self.pxconvert = pxconvert

        self.num =0
        self.data =[[] for i in range(30)] #为30个老鼠建立数据list

    def distance(self,num1,num2): #计算两个像素点间距离的方法
        return  round(math.sqrt((num1[0]-num2[0])**2+((num1[1]-num2[1])**2))*self.pxconvert,2)

    def torchdetect(self, img):
        self.num +=1 ##每次调用一次该方法，帧数加一

        font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
        if self.flag is 'rect':
            # img = cv2.resize(img, (960, 540))

            list_bboxs = []
            bboxes = self.detector.detect(img) #应用检测器对每帧图片进行检测

            # 如果画面中 有bbox
            if len(bboxes) > 0:
                list_bboxs = tracker.update(bboxes, img)
                # 画框
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                output_image_frame = tracker.draw_bboxes(img, list_bboxs, line_thickness=None)
                pass
            else:
                # 如果画面中 没有bbox
                output_image_frame = img
            pass

            # 输出图片
            # output_image_frame = cv2.add(output_image_frame, color_polygons_image)
            output_image_frame = cv2.rectangle(output_image_frame, self.dic[0], self.dic[1], (36, 255, 12), 2)
            if len(list_bboxs) > 0:
                # ----------------------判断撞线----------------------
                for item_bbox in list_bboxs:
                    x1, y1, x2, y2, label, track_id = item_bbox

                    # # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                    # y1_offset = int(y1 + ((y2 - y1) * 0.6))

                    color = [int(c) for c in self.COLORS[track_id % len(self.COLORS)]]


                    # 撞线的点
                    y = int((y1 + y2) * 0.5)
                    x = int((x1 + x2) * 0.5)
                    center = (x, y)

                    for j in range(1, len(self.pts[track_id])):
                        if self.pts[track_id][j - 1] is None or self.pts[track_id][j] is None:
                            continue
                        thickness = int(np.sqrt(64 / float(j + 1)) * 2)
                        cv2.line(output_image_frame, (self.pts[track_id][j - 1]), (self.pts[track_id][j]), color, thickness)
                    if track_id not in self.list_region: #检测老鼠是不是在上下帧中第一次出现
                        self.json['{}_st'.format(track_id)] = time.time() #记录第一次出现的时间
                        self.list_region.append(track_id)
                        self.precenter['{}'.format(track_id)] = center
                        self.distRes['{}'.format(track_id)]=0
                        self.data[track_id] = []  #为响应的tracker_id初始化data list

                    if self.dic[0][0] < x < self.dic[1][0] and self.dic[0][1] < y < self.dic[1][1]:
                        if track_id not in self.list_overlapping_region:
                            self.json['{}_ed'.format(track_id)] = time.time()
                            self.list_overlapping_region.append(track_id)
                            timestamp = round(self.json['{}_ed'.format(track_id)] - self.json['{}_st'.format(track_id)], 2)
                            print("{} 停留时间为{}s".format(track_id, timestamp))
                        pass

                    self.pts[track_id].append(center)
                    disttemp = self.distance(center, self.precenter[
                        '{}'.format(track_id)]) if track_id in self.list_region else 0
                    # print(disttemp)
                    # disttemp = self.distRes[''.format(track_id)] + disttemp
                    # if disttemp <= 1:
                    #     disttemp = round(0.5 * random.random(),2) #bounding box 在检测的时候有抖动情况发生，消除抖动
                    self.distRes['{}'.format(track_id)] = disttemp +self.distRes['{}'.format(track_id)]
                    self.precenter['{}'.format(track_id)] = center
                    self.data[track_id].append((self.num, round(self.distRes['{}'.format(track_id)],2))) #检测完一帧，加入一帧的距离数据
            return output_image_frame

        if self.flag is 'line':
            # img = cv2.resize(img, (960, 540))

            list_bboxs = []
            bboxes = self.detector.detect(img)
            # 如果画面中 有bbox
            if len(bboxes) > 0:
                list_bboxs = tracker.update(bboxes, img)
                # 画框
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                output_image_frame = tracker.draw_bboxes(img, list_bboxs, line_thickness=None)
                pass
            else:
                # 如果画面中 没有bbox
                output_image_frame = img
            pass

            # 输出图片
            # output_image_frame = cv2.add(output_image_frame, color_polygons_image)
            output_image_frame = cv2.line(output_image_frame, self.dic[0], self.dic[1], (36, 255, 12), 2)
            if len(list_bboxs) > 0:
                # ----------------------判断撞线----------------------
                for item_bbox in list_bboxs:
                    x1, y1, x2, y2, label, track_id = item_bbox

                    # # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                    # y1_offset = int(y1 + ((y2 - y1) * 0.6))
                    color = [int(c) for c in self.COLORS[track_id % len(self.COLORS)]]

                    # 撞线的点
                    y = int((y1 + y2) * 0.5)
                    x = int((x1 + x2) * 0.5)
                    center = (x, y)


                    if track_id not in self.list_region:
                        self.json['{}_st'.format(track_id)] = time.time()
                        self.list_region.append(track_id)

                    if  y > (self.dic[0][1]+self.dic[1][1])*0.5:
                        # print(f'y={y}')
                        # print(f'y1+y2/2={(self.dic[0][1]+self.dic[1][1])*0.5}')
                        if track_id not in self.list_overlapping_region:
                            self.list_overlapping_region.append(track_id)
                            self.json['{}_ed'.format(track_id)] = time.time()
                            timestamp = round(self.json['{}_ed'.format(track_id)] - self.json['{}_st'.format(track_id)], 2)
                            print("{} 停留时间为{}s".format(track_id, timestamp))
                        pass
            return output_image_frame


class DrawLineWidget(object):
    def __init__(self, frame, key):
        self.original_image = frame
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # List to store start/end points
        self.image_coordinates = []
        self.json = {}
        self.key = key

    # def getframe(self):
    #     cap = cv2.VideoCapture(0)  # 调整参数实现读取视频或调用摄像头
    #     while 1:
    #         ret, frame = cap.read()
    #         cv2.imshow("cap", frame)
    #         # width = cap.get(3)
    #         # height = cap.get(4)
    #         # print('width：{}，height:{}'.format(width,height))
    #         if cv2.waitKey(100) & 0xff == ord('q'):
    #             self.pic = frame
    #             break
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     return frame

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x, y)]

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x, y))
            # print('Starting: {}, Ending: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))

            # Draw line
            if self.key == 'draw_line':
                cv2.line(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36, 255, 12), 2)
                cv2.imshow("image", self.clone)
                self.json['line'] = self.image_coordinates  # 把坐标扔进去
            if self.key == 'draw_rect':
                cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36, 255, 12), 2)
                self.json['rect'] = self.image_coordinates  # 把坐标扔进去

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        return self.clone

    def getData(self):
        return self.json


if __name__ == '__main__':
    det = Detector()
    dic = [(207, 179), (577, 450)]
    tor = torch('rect',dic,det)
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        frame = tor.torchdetect(frame)
        cv2.imshow('image',frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)


    # while True:
    #     cv2.imshow('image', draw_line_widget.show_image())
    #     key = cv2.waitKey(1)
    #
    #     # Close program with keyboard 'q'
    #     if key == ord('q'):
    #         cv2.destroyAllWindows()
    #         exit(1)
