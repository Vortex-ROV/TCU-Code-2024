import time
import cv2
import numpy as np
import sys
from vidgear.gears import NetGear

class NetgearClient:
    """
    Create a tcp Netgear Client object
    
    Args:
        address (str): IP address of the server
        port (str): Port number of the server
        options (dict): Options for the Netgear object
    """

    def __init__(self,Address="192.168.33.100",Port="5454") -> None:
        options = {
            "jpeg_compression": True,
            "jpeg_compression_quality": 90,
            "jpeg_compression_fastdct": True,
            "jpeg_compression_fastupsample": True,
            "max_retries": sys.maxsize,
            "bidirectional_mode": True  # Enable two-way communication
        }
        self.client = NetGear(
            receive_mode=True,
            address=Address,
            port=Port,
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
    with NetgearClient() as client:
        start_time = time.time()  # Start time for FPS calculation

        # while True:
        for _ in range(5000):
            frame = client.Receive()
            frame = frame[1] if frame is not None else None
            if frame is not None:
                # print(f"Frame shape: {frame}, Frame type: {type(frame)}")
                cv2.imshow("Client", frame)
                key = cv2.waitKey(1) 
                if key == ord('q'):
                    break

                # Calculate and display FPS
        end_time = time.time()  # End time for FPS calculation
        elapsed_time = end_time - start_time
        fps = 5000 / elapsed_time if elapsed_time > 0 else 0
        print(f"Processed 5000 frames in {elapsed_time:.2f} seconds. FPS: {fps:.2f}")
 
        cv2.destroyAllWindows()
        client.Close() # close the connection


if __name__ == "__main__":
    main()