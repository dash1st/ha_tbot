import time
import os
import datetime
from threading import Thread
from queue import Queue

import cv2

print(url)
    #거실2
    #url = 'rtsp://admin:YLWMWP@192.168.0.6:554/h264_stream'
    #안방 
    #url = 'rtsp://admin:UVSOFQ@192.168.0.2:554/h264_stream'

class Camera:
    def __init__(self, mirror=False):
        self.data = None
        #self.cam = cv2.VideoCapture(0) #로컬 카메라 연결
        self.cam = cv2.VideoCapture(url)

        self.WIDTH = 640
        self.HEIGHT = 480

        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False

        self.scale = 1
        self.__setup()

        self.recording = False

        self.mirror = mirror

    def __setup(self):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        time.sleep(2)

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()


    def save_picture(self):
    # 이미지 저장하는 함수
        ret, img = self.cam.read()
        if ret:
            now = datetime.datetime.now()
            date = now.strftime('%Y%m%d')
            hour = now.strftime('%H%M%S')
            user_id = '00001'
            #filename = './images/cvui_{}_{}_{}.png'.format(date, hour, user_id)
            filename = './images/temp.png'
            cv2.imwrite(filename, img)
            #self.image_queue.put_nowait(filename)

if __name__ == '__main__':

    cam = Camera(mirror=True)
    cam.save_picture()








