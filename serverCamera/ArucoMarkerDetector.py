import cv2
import numpy as np
import threading
from communication.message import Message
from communication.companion_link import CompanionLink

class ArucoDetector:
    def __init__(self):

        self.companion_link = CompanionLink(address="192.168.33.1", port=4096)
        self.companion_link.client.connect()
        # Set the dictionary and parameters for detecting ArUco markers
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_100)
        self.parameters = cv2.aruco.DetectorParameters()
        
        # Variable to store the original and processed frames
        self.frame = None
        self.processed_frame = None

        # Thread for detection
        self.detection_thread = threading.Thread(target=self.detect_markers_in_thread)
        self.detection_thread.daemon = True
        self.detection_thread.start()

    def update_frame(self, frame):
        """
        Updates the frame for detection.
        
        Args:
            frame: The frame to process for ArUco marker detection.
        """
        self.frame = frame

    def detect_markers_in_thread(self):
        """
        Thread function to detect ArUco markers in the current frame.
        Continuously processes new frames and applies detection.
        """
        while True:
            if self.frame is not None:
                # Process the frame to detect ArUco markers
                self.processed_frame = self.detect_aruco_markers(self.frame.copy())

    def detect_aruco_markers(self, frame):
        """
        Detects ArUco markers and draws them on the frame.

        Args:
            frame: The frame to detect markers in.

        Returns:
            The frame with detected markers and additional information.
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers in the frame
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

        # Get the center of the camera frame
        frame_center_x, frame_center_y = frame.shape[1] // 2, frame.shape[0] // 2
        center_radius = 30  # Define the radius of the central circle

        # Draw a circle and a point at the center of the frame
        cv2.circle(frame, (frame_center_x, frame_center_y), center_radius, (255, 0, 0), 2)  # Circle
        cv2.circle(frame, (frame_center_x, frame_center_y), 5, (0, 255, 255), -1)  # Center point

        # If markers are detected
        if np.all(ids is not None):
            # Draw detected markers
            frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Calculate the center of the first detected marker
            for corner in corners:
                # Get the marker's corner points
                top_left, bottom_right = corner[0][0], corner[0][2]

                # Calculate the center of the marker
                marker_center_x = int((top_left[0] + bottom_right[0]) / 2)
                marker_center_y = int((top_left[1] + bottom_right[1]) / 2)

                # Draw the center point of the marker
                cv2.circle(frame, (marker_center_x, marker_center_y), 5, (0, 255, 0), -1)

                # Calculate the distance between the marker center and the frame center
                x_diff = frame_center_x - marker_center_x
                y_diff = frame_center_y - marker_center_y
                distance_to_center = np.sqrt(x_diff**2 + y_diff**2)

                # Move the camera only if the marker center is outside the central circle
                if distance_to_center > center_radius:
                    self.move_camera(x_diff, y_diff)
                else:
                    self.companion_link.send_control_commands(Message().bytes())
                    print("Marker is within the center circle. No movement needed.")

                break  # Process only the first marker for simplicity

        else:
            self.companion_link.send_control_commands(Message().bytes())

        return frame

    def move_camera(self, x_diff, y_diff):
        """
        Controls camera movement based on marker position.

        Args:
            x_diff: Difference between the center of the frame and the marker on the x-axis.
            y_diff: Difference between the center of the frame and the marker on the y-axis.
        """
        message = Message()
        if abs(x_diff) > 10:
            message.set_value("armed", True)
            if x_diff > 0:
                message.set_value("lateral", 1600)
            else:
                message.set_value("lateral",1400)
            # print("Move Right" if x_diff > 0 else "Move Left")
        if abs(y_diff) > 10:
            message.set_value("armed", True)
            if y_diff > 0:
                message.set_value("forward", 1600)
            else:
                message.set_value("forward", 1400)
            # print("Move Down" if y_diff > 0 else "Move Up")

        self.companion_link.send_control_commands(message.bytes())

    
