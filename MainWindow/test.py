import os
import time
from collections import deque
import sys
ROOT_DIR = os.path.abspath("../../../PycharmProjects")
sys.path.append(os.path.join(ROOT_DIR, "/"))  #模型存放路径
import numpy as np

import cv2


if __name__ == '__main__':

    list_region = []
    list_overlapping_region = []
    json = {}
    pts = [deque(maxlen=40) for _ in range(9999)]

    COLORS = np.random.randint(0, 255, size=(200, 3),
                               dtype="uint8")

    font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_postion = (int(960 * 0.01), int(540 * 0.05))

    # 初始化 yolov5
    detector = Detector()

    # 打开视频
    # capture = cv2.VideoCapture('./video/test.mp4')
    capture = cv2.VideoCapture(0)
    dic = [(207, 179), (577, 450)]

    while True:
        # 读取每帧图片
        _, im = capture.read()
        if im is None:
            break

        # 缩小尺寸，1920x1080->960x540
        im = cv2.resize(im, (960, 540))

        list_bboxs = []
        bboxes = detector.detect(im)

        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxs = tracker.update(bboxes, im)
            # 画框
            # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
            output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=None)
            pass
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        pass

        # 输出图片
        # output_image_frame = cv2.add(output_image_frame, color_polygons_image)
        output_image_frame = cv2.rectangle(output_image_frame, dic[0], dic[1], (36, 255, 12), 2)

        if len(list_bboxs) > 0:
            # ----------------------判断撞线----------------------
            for item_bbox in list_bboxs:
                x1, y1, x2, y2, label, track_id = item_bbox

                # # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                # y1_offset = int(y1 + ((y2 - y1) * 0.6))
                color = [int(c) for c in COLORS[track_id % len(COLORS)]]

                # 撞线的点
                y = int((y1 + y2) * 0.5)
                x = int((x1 + x2) * 0.5)
                center = (x, y)
                pts[track_id].append(center)
                for j in range(1, len(pts[track_id])):
                    if pts[track_id][j - 1] is None or pts[track_id][j] is None:
                        continue
                    thickness = int(np.sqrt(64 / float(j + 1)) * 2)
                    cv2.line(output_image_frame, (pts[track_id][j - 1]), (pts[track_id][j]), color, thickness)
                if track_id not in list_region:
                    json['{}_st'.format(track_id)] = time.time()
                    list_region.append(track_id)

                if dic[0][0] < x < dic[1][0] and dic[0][1] < y < dic[1][1]:
                    if track_id not in list_overlapping_region:
                        json['{}_ed'.format(track_id)] = time.time()
                        list_overlapping_region.append(track_id)
                        timestamp = round(json['{}_ed'.format(track_id)] - json['{}_st'.format(track_id)], 2)
                        print("{} 停留时间为{}s".format(track_id, timestamp))
                    pass

        # text_draw = 'DOWN: ' + str(down_count) + \
        #             ' , UP: ' + str(up_count)
        # output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
        #                                  org=draw_text_postion,
        #                                  fontFace=font_draw_number,
        #                                  fontScale=1, color=(255, 255, 255), thickness=2)

        cv2.imshow('demo', output_image_frame)
        cv2.waitKey(1)

        pass
    pass

    capture.release()
    cv2.destroyAllWindows()


