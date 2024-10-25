import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from vidgear.gears import NetGear


class Camera(QThread):
    frame_received = pyqtSignal(np.ndarray)

    def __init__(self, frame_callback=None, parent=None):
        super().__init__(parent)
        self.frame_callback = frame_callback
        self.is_running = True

        # Define NetGear Client
        options = {"flag": 0, "copy": True, "track": False}
        self.client = NetGear(
            address="192.168.33.100",  # replace with your actual IP
            port="5454",
            protocol="tcp",
            pattern=1,
            receive_mode=True,
            logging=True,
            **options
        )

    def run(self):
        # Continuously receive frames from the NetGear server
        while self.is_running:
            frame = self.client.recv()
            if frame is None:
                break  # Stop if there are no more frames

            if self.frame_callback:
                # In standalone mode, process frames via callback
                self.frame_callback(frame)
            else:
                # In GUI mode, emit the frame signal
                self.frame_received.emit(frame)

    def stop(self):
        # Gracefully stop the thread
        self.is_running = False
        self.client.close()
        self.quit()


# Standalone mode implementation
if __name__ == "__main__":

    def process_frame(frame):
        # Show frame in standalone mode
        cv2.imshow("Standalone Camera Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            return False  # Stop the feed if 'q' is pressed
        return True

    # Initialize the camera class with a callback
    camera = Camera(frame_callback=process_frame)
    camera.start()

    while camera.is_running:
        if not process_frame(camera.client.recv()):
            camera.stop()
            break

    cv2.destroyAllWindows()
