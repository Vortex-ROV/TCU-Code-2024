import cv2
from vidgear.gears import NetGear
from .ArucoMarkerDetector import ArucoDetector  # Import the ArucoDetector class

class NetgearClient:
    """
    Creates a TCP NetGear Client object to receive frames from the server.
    
    Args:
        address (str): IP address of the server (default: "192.168.33.100")
        port (str): Port number of the server (default: "5454")
    """

    def __init__(self, address="192.168.33.100", port="5454") -> None:
        options = {
            "jpeg_compression": True,
            "jpeg_compression_quality": 80,
            "jpeg_compression_fastdct": True,
            "jpeg_compression_fastupsample": True,
            "bidirectional_mode": True,
        }
        self.client = NetGear(
            receive_mode=True,
            address=address,
            port=port,
            protocol="tcp",
            pattern=1,
            logging=True,
            **options
        )
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.Close()

    def Receive(self):
        """
        Receive a frame from the server
        """
        return self.client.recv()

    def Close(self):
        """
        Close the connection
        """
        self.client.close()

        
def main():
    """
    Main function to receive, display, and optionally record frames from the server.
    """
    with NetgearClient() as client:
        aruco_detector = ArucoDetector()  # Instantiate ArucoDetector
        detection_mode = False  # Start with detection mode off

        while True:
            # Receive frames from the server
            frame = client.client.recv()[1]

            # Break the loop if no frame is received
            if frame is None:
                print("No more frames received. Exiting.")
                break

            # Process frame based on the current mode
            if detection_mode:
                # aruco_detector.update_frame(frame)  # Update for detection
                # display_frame = aruco_detector.processed_frame if aruco_detector.processed_frame is not None else frame
                display_frame = aruco_detector.detect_aruco_markers(frame)  # Detect ArUco markers
            else:
                display_frame = frame  # Show raw frame if detection is off

            # Display the selected frame in the same window
            cv2.imshow("Frame", cv2.flip(display_frame, 0))

            # Key press handling
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Exit on 'q'
                break
            elif key == ord('d'):  # Toggle detection mode on 'd'
                detection_mode = not detection_mode
                print("Detection mode:", "ON" if detection_mode else "OFF")

        # Release resources
        cv2.destroyAllWindows()
        client.Close()

if __name__ == "__main__":
    main()