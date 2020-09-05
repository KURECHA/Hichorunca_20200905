import cv2
from cap_box import cap_box

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0+cv2.CAP_DSHOW)


    def __del__(self):
        self.video.release()

    def get_frame(self, size):
        success, image = self.video.read()
        image, ecobag_used, s_bag_num, l_bag_num, egg_flag = cap_box(size)
        result = [ecobag_used, s_bag_num, l_bag_num]
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(), result, egg_flag
