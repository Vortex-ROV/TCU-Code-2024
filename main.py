import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from camera import Camera
from design import Ui_MainWindow
from joystick.joystick import JoyStick
from communication.link import MavproxyLink, CompanionLink
from communication.messages import Message
from serverCamera.VideoRecorder import VideoRecorder
from serverCamera.ArucoMarkerDetector import ArucoDetector

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super().__init__()
        self.setupUi(self)

        self.cameraThread = Camera()
        self.cameraThread.frame_received.connect(self.update_camera_stream)
        self.cameraThread.start()

        self.joystick_thread = JoyStick()
        self.joystick_thread.link = MavproxyLink(port=14550)
        self.joystick_thread.start()
        self.aruco_marker_detection = ArucoDetector(self.joystick_thread.link)

        self.arucoDetectionEnabled = False
        self.videoRecorder = None
        self.recordStat = False
        self.record.clicked.connect(self.startRecording)
        self.saveFrame.clicked.connect(self.toggle_aruco_detection_state)

    def update_camera_stream(self, frame):
        if self.videoRecorder is None:
            frame_size = (frame.shape[1], frame.shape[0])
            self.videoRecorder = VideoRecorder(frame_size)

        if self.arucoDetectionEnabled:
            # self.aruco_marker_detection.update_frame(frame)
            processed_frame = self.aruco_marker_detection.detect_aruco_markers(frame)
            # processed_frame = self.aruco_marker_detection.processed_frame
            processed_frame = frame
            if processed_frame is None:
                processed_frame = frame  # Fallback to original frame if detection isn't ready
        else:
            processed_frame = frame  # No processing if detection is disabled

        # Convert frame for display in the GUI
        processed_frame = cv2.flip(processed_frame, 0)
        processed_frame = cv2.flip(processed_frame, 1)
        frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
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

    def toggle_aruco_detection_state(self):
        """
        Toggles the state of ArUco marker detection.
        """
        self.arucoDetectionEnabled = not self.arucoDetectionEnabled
        state = "enabled" if self.arucoDetectionEnabled else "disabled"
        print(f"ArUco marker detection {state}")

        if not self.arucoDetectionEnabled:
            msg = Message()
            msg.set_value("armed", False)
            self.joystick_thread.link.control_pixhawk(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())