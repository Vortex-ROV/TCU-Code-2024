import time
import cv2
import numpy as np
import sys
from queue import Queue
from vidgear.gears import NetGear
import threading

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
            "jpeg_compression_fastupsample": True
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

def main():
    """
    Main function to run the client
    """
    # Create the client object
    Client = NetgearClient()
    t = time.time()
    # Loop to receive frames
    for i in range(5000):
        # Receive frames from the server
        frame = Client.client.recv()
        # If NoneType
        if frame is None:
            break
        # Display the frame
        cv2.imshow("frame",frame)
        cv2.waitKey(1)
    # Calculate the frame rate
    print(5000/(time.time()-t))
    # Close the stream
    Client.client.close()

if __name__ == "__main__":
    main()

