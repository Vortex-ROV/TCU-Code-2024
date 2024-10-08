from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
from vidgear.gears import NetGear
import sys
import os
import numpy as np

class CameraThread(QThread):
    frame_updated = pyqtSignal(object)

    def __init__(self, address = "192.168.33.100", port = "5454"):
        super(CameraThread, self).__init__()
        options={
            "max_retries":sys.maxsize
        }
        self.client = NetGear(
            address = address,
            port = port,
            protocol = "tcp",
            pattern = 1,
            receive_mode = True,
            logging = True,
            # request_timeout = sys.maxsize,
            **options
        )

    def run(self):
        i=0
        while True:
            frame = self.client.recv() # A frame is sent every 50 milliseconds, and maybe every 25 milliseconds
            i+=1
            if frame is not None:
                # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)
                # cv2.imshow("Hello",rotated_frame)
                # key = cv2.waitKey(1) 
                # if key == ord(' '):
                    # frame_filename = os.path.join("D:/frames", "frame_{}.jpg".format(len(os.listdir("frames"))))
                    # cv2.imwrite(frame_filename, frame)
                    # cv2.imwrite(f"frame {i}",frame)
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # cv2.imshow("555555",rotated_frame)
                self.frame_updated.emit(rgb_image)


class Camera:
    def __init__(self, ui):
        self.ui = ui
        # self.takephoto = takephoto
        self.camera_thread = CameraThread()
        self.camera_thread.frame_updated.connect(self.update_frame)
        # self.takephoto.clicked.connect(self.save_frame)
        self.camera_thread.start()
        self.camera_thread.setPriority(QThread.HighestPriority)

    def update_frame(self, frame):
        h, w, ch = frame.shape
        Qframe = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(Qframe)
        self.ui.camera.setPixmap(pixmap)
    
    # def save_frame(self):
    #     pixmap = self.ui.camera.pixmap()
    #     if pixmap is not None:
    #         frame = pixmap.toImage().convertToFormat(QImage.Format_RGB888)
    #         frame_data = frame.constBits()
    #         frame_data.setsize(frame.byteCount())
    #         frame_array = np.array(frame_data).reshape(frame.height(), frame.width(), 3)
    #         os.makedirs("frames", exist_ok=True)
    #         frame_filename = os.path.join("frames", "frame_{}.jpg".format(len(os.listdir("frames"))))
    #         cv2.imwrite(frame_filename, cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR))
    #         print("Frame saved:", frame_filename)