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
            "max_retries": sys.maxsize
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
        while True:
            frame = client.Receive()
            if frame is not None:
                cv2.imshow("Client", frame)
                key = cv2.waitKey(1) 
                if key == ord('q'):
                    break
        cv2.destroyAllWindows()
        client.Close() # close the connection


if __name__ == "__main__":
    main()