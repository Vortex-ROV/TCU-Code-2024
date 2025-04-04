import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from app.Model.camera.camera import Camera
from app.View.design import Ui_MainWindow

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cameraThread = Camera()
        self.cameraThread.frame_received.connect(self.update_camera_stream)
        self.cameraThread.start()

    def update_camera_stream(self, frame):
        frame_resized = cv2.resize(frame, (self.camera.width(), self.camera.height()))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        qImg = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], frame_rgb.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.camera.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()