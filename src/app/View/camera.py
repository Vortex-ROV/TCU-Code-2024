import cv2
import numpy as np
from vidgear.gears import NetGear
import time
from PyQt5.QtCore import QThread, pyqtSignal


class Camera(QThread):
    frame_received = pyqtSignal(np.ndarray)
    

    def __init__(self, frame_callback=None, parent=None):
        super().__init__(parent)
        self.frame_callback = frame_callback  # Callback for standalone mode
        self.is_running = True  # To control thread termination
        self.frame = np.zeros((300, 300, 3), dtype=np.uint8)

        # Setup NetGear client
        options = {"flag": 0, "copy": True, "track": False}
        self.client = NetGear(
            address="192.168.33.100",  # replace with actual IP
            port="5454",
            protocol="tcp",
            pattern=1,
            receive_mode=True,
            logging=True,
            **options
        )

    def run(self):
        """Main loop that handles both standalone and GUI modes."""
        currentFrame = 0
        startTime = time.time()
        while currentFrame < 10000:
            frame = self.client.recv()
            if frame is not None:
                currentFrame+=1
                # Rotate frame by 180 degrees
                frame_rotated = cv2.rotate(frame, cv2.ROTATE_180)

                if self.frame_callback:
                    # Standalone mode: Use the provided callback to display frame
                    if not self.frame_callback(frame_rotated):
                        self.is_running = False  # Stop if callback returns False
                        break
                else:
                    # GUI mode: Emit the rotated frame signal
                    self.frame_received.emit(frame_rotated)
        endTime = int(startTime - time.time())*-1
        print(f"Total frames received: {currentFrame}")
        print(f"Time elapsed: {endTime} seconds")
        print(f'FPS is {currentFrame/endTime}')
        self.stop()
        

        self.client.close()
        cv2.destroyAllWindows()

    def stop(self):
        """Stop the camera thread."""
        self.is_running = False
        self.quit()  # Gracefully quit the QThread


# Standalone mode logic in the `frame_callback`
if __name__ == "__main__":

    def display_frame(frame):
        """Display the frame using OpenCV for standalone mode."""
        frame_resized = cv2.resize(frame, (640, 480))
        cv2.imshow("Standalone Camera Feed", frame_resized)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return False
        return True

    # Instantiate the Camera class and pass the `display_frame` as the callback
    camera = Camera(frame_callback=display_frame)
    camera.start()  # Start the thread

    # Keep the thread running until the user presses 'q'
    camera.wait()  # Wait for the thread to finish execution

    cv2.destroyAllWindows()  # Clean up OpenCV windows
