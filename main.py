import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from camera import Camera
from design import Ui_MainWindow
from joystick.joystick import JoyStick
from communication.link import MavproxyLink, CompanionLink
from serverCamera.VideoRecorder import VideoRecorder

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cameraThread = Camera()
        self.cameraThread.frame_received.connect(self.update_camera_stream)
        self.cameraThread.start()

        self.joystick_thread = JoyStick()
        self.joystick_thread.link = MavproxyLink()
        self.joystick_thread.start()

        self.videoRecorder = None
        self.recordStat = False
        self.record.clicked.connect(self.startRecording)

    def update_camera_stream(self, frame):
        if self.videoRecorder is None:
            frame_size = (frame.shape[1], frame.shape[0])
            self.videoRecorder = VideoRecorder(frame_size)

        # Convert frame for display in the GUI
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qImg = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], frame_rgb.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.camera.setPixmap(pixmap)

        # If recording, write the frame to the video file
        if self.recordStat and self.videoRecorder is not None:
            self.videoRecorder.write_frame(frame)

    def startRecording(self):
        if not self.recordStat and self.videoRecorder is not None:
            self.videoRecorder.start_recording()
            self.recordStat = True
        elif self.recordStat and self.videoRecorder is not None:
            self.videoRecorder.stop_recording()
            self.recordStat = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())