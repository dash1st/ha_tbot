import time
import os
import datetime
from threading import Thread
from queue import Queue
import cv2
    #거실2
    #url = 'rtsp://admin:YLWMWP@192.168.0.6:554/h264_stream'
    #안방 
    #url = 'rtsp://admin:UVSOFQ@192.168.0.2:554/h264_stream'

class Camera:
    def __init__(self, mirror=False):
        #거실1
        url = 'rtsp://admin:YLWMWP@192.168.0.6:554/h264_stream'
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

    def stream(self):
        # streaming thread function
        def streaming():
            # The actual threaded function
            self.ret = True
            while self.ret:
                self.ret, np_image = self.cam.read()
                if np_image is None:
                    continue
                if self.mirror:
                    # Inverted left and right in mirror mode
                    np_image = cv2.flip(np_image, 1)
                self.data = np_image
                k = cv2.waitKey(1)
                if k == ord('q'):
                    self.release()
                    break

        Thread(target=streaming).start()

    def show(self):
        while True:
            frame = self.data
            if frame is not None:
                cv2.imshow('Davinci AI', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                # q : close
                self.release()
                cv2.destroyAllWindows()
                break

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


#    def record_video(self):
#        # 동영상 녹화 함수
#        fc = 20.0
#        record_start_time = time.time()
#        now = datetime.datetime.now()
#        date = now.strftime('%Y%m%d')
#        t = now.strftime('%H')
#        num = 1
#        filename = 'videos/cvui_{}_{}_{}.avi'.format(date, t, num)
#        while os.path.exists(filename):
#            num += 1
#            filename = 'videos/cvui_{}_{}_{}.avi'.format(date, t, num)
#        codec = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
#        out = cv2.VideoWriter(filename, codec, fc, (int(self.cam.get(3)), int(self.cam.get(4))))
#        while self.recording:
#            if time.time() - record_start_time >= 600:
#                self.record_video()
#                break
#            ret, frame = self.cam.read()
#            if ret:
#                if len(os.listdir('./videos')) >= 100:
#                    name = self.video_queue.get()
#                    if os.path.exists(name):
#                        os.remove(name)
#                out.write(frame)
#                self.video_queue.put_nowait(filename)
#            k = cv2.waitKey(1)gf
#            if k == ord('q'):
#                break

if __name__ == '__main__':

    cam = Camera(mirror=True)
#    cam.stream()
#    cam.show()
    cam.save_picture()








