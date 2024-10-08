from .client import NetgearClient  # Import your client class
import cv2
def main():
    """
    Entry point function for the package.
    This will be executed when the package is run.
    """
    with NetgearClient() as client:
        while True:
            frame = client.Receive()
            if frame is not None:
                cv2.imshow("Client", frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
        cv2.destroyAllWindows()
        client.Close()  # Close the connection

if __name__ == "__main__":
    main()
