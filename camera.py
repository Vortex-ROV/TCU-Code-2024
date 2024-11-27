import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from serverCamera.client import NetgearClient


class Camera(QThread):
    frame_received = pyqtSignal(np.ndarray)

    def __init__(self, frame_callback=None, parent=None):
        super().__init__(parent)
        self.frame_callback = frame_callback

    def run(self):
        """Main loop that handles both standalone and GUI modes."""
        self.cameraThread = NetgearClient()
        while True:
            frame = self.cameraThread.Receive()
            # frame_size = (frame.shape[1], frame.shape[0])
            frame = frame[1] if frame is not None else None
            if frame is not None:
                frame_rotated = cv2.flip(frame, 0)

                if self.frame_callback:
                    if not self.frame_callback(frame_rotated):
                        self.is_running = False
                        break
                else:
                    self.frame_received.emit(frame)
        self.stop()

        cv2.destroyAllWindows()

    def stop(self):
        """Stop the camera thread."""
        self.is_running = False
        self.quit()


if __name__ == "__main__":

    def display_frame(frame):
        """Display the frame using OpenCV for standalone mode."""
        frame_resized = cv2.resize(frame, (640, 480))
        cv2.imshow("Standalone Camera Feed", frame_resized)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return False
        return True

    camera = Camera(frame_callback=display_frame)
    camera.start()
    camera.wait()
    cv2.destroyAllWindows()