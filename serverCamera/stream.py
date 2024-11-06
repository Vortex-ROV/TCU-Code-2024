from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal
import cv2

class CameraThread(QThread):
    frame_updated = pyqtSignal(object)

    def __init__(self):
        super(CameraThread, self).__init__()
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_updated.emit(rgb_image)
            self.msleep(25)
        self.cap.release()

class Stream:
    def __init__(self, ui):
        self.ui = ui
        self.camera_thread = CameraThread()
        self.camera_thread.frame_updated.connect(self.update_frame)
        self.camera_thread.start()
        self.camera_thread.setPriority(QThread.HighestPriority)

    def update_frame(self, frame):
        h, w, ch = frame.shape
        Qframe = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(Qframe)
        self.ui.camera.setPixmap(pixmap)