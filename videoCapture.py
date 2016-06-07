import numpy as np
import cv2


class handCaptrue(object):
    def __init__(self, device_index=0, quit_key='q', lower_hand_mask=None, upper_hand_mask=None):
        self._device_index = device_index  # 设备索引号
        self._quit = quit_key  # 退出摄像头
        self.lower_hand_mask = np.array([0, 60, 90]) if lower_hand_mask is None else lower_hand_mask  # hsv最小值
        self.upper_hand_mask = np.array([30, 180, 220]) if upper_hand_mask is None else upper_hand_mask  # hsv最大值
        self.contours = None  # 轮廓

    # 捕捉视频
    def capture_video(self):
        cap = cv2.VideoCapture(self._device_index)
        while cap.isOpened():
            # 获取帧画面, 如果摄像头开启成功
            ret, frame = cap.read()

            # 对帧画面操作
            if ret:
                self.capture_image(frame)

            # 等待1ms键盘输入，按q退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 停止捕获视频
        cap.release()
        cv2.destroyAllWindows()

    def capture_image(self, frame):
        blur = self.threshold_filter_morphological(frame)
        try:
            cnt = self.find_contours(blur)
        except ValueError as v:
            print(v.args)
        else:
            self.convex_hull(frame, cnt)
            self.draw_contours_display(frame)

    def threshold_filter_morphological(self, frame):
         # 高斯滤波
        blur = cv2.GaussianBlur(frame, (13, 13), 0)

        # 中值过滤
        median = cv2.medianBlur(blur, 5)

        # 转换到HSV
        hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

        # 根据阈值构建掩模
        mask = cv2.inRange(hsv, self.lower_hand_mask, self.upper_hand_mask)

        # 开运算
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 高斯滤波
        blur = cv2.GaussianBlur(opening, (3, 3), 0)
        # 自适应二值化（这里效果不是很好，还需要修改）
        # th2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        # cv2.imshow('test', th2)
        return blur

    def find_contours(self, frame):
        # 查找轮廓
        image, self.contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 选择面积最大的轮廓
        max_contour = -1
        ci = 0
        for index, current_contour in enumerate(self.contours):
            area = cv2.contourArea(current_contour)
            if area > max_contour:
                max_contour = area
                ci = index

        if max_contour == -1:
            raise ValueError('摄像头无法捕捉到轮廓，请调整捕捉画面！')
        else:
            return self.contours[ci]

    @classmethod
    def convex_hull(cls, frame, cnt):
        # 获取凸性缺陷
        hull = cv2.convexHull(cnt, returnPoints=False)

        # 画出凸包
        defects = cv2.convexityDefects(cnt, hull)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            cv2.line(frame, start, end, [0,  255, 0], 2)
            cv2.circle(frame, far, 5, [0, 0, 255], -1)

    def draw_contours_display(self, frame):
        # 绘制轮廓
        gestures = cv2.drawContours(frame, self.contours, -1, (0, 255, 0), 3)

        # 显示处理后效果
        cv2.imshow('Gestures', gestures)

if __name__ == '__main__':
    handCaptrue().capture_video()




