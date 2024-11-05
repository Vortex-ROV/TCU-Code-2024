from .client import NetgearClient  # Import your client class
import cv2
import time

def main():
    """
    Entry point function for the package.
    This will be executed when the package is run.
    """
    total_frames = 5000  # Number of frames to process
    frame_count = 0      # Initialize frame counter
    start_time = time.time()  # Start the timer

    with NetgearClient() as client:
        while frame_count < total_frames:
            frame = client.Receive()
            if frame is not None:
                frame_count += 1  # Increment frame counter
                cv2.imshow("Client", frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

        end_time = time.time()  # End the timer
        total_time = end_time - start_time  # Total time taken
        fps = frame_count / total_time  # Calculate FPS
        print(f"Processed {frame_count} frames in {total_time:.2f} seconds")
        print(f"FPS: {fps:.2f}")

        cv2.destroyAllWindows()
        client.Close()  # Close the connection

if __name__ == "__main__":
    main()
