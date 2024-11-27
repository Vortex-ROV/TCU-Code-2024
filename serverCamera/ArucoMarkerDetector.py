import cv2
import numpy as np
import threading
from communication.messages import Message
from communication.link import MavproxyLink

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error_x = 0
        self.integral_x = 0

        self.prev_error_y = 0
        self.integral_y = 0

    def update(self, error_x, error_y):
        self.integral_x += error_x
        self.integral_y += error_y

        derivative_x = error_x - self.prev_error_x
        derivative_y = error_y - self.prev_error_y

        output_x = self.kp * error_x + self.ki * self.integral_x + self.kd * derivative_x
        output_y = self.kp * error_y + self.ki * self.integral_y + self.kd * derivative_y

        self.prev_error_x = error_x
        self.prev_error_y = error_y
        
        return output_x, output_y

class ArucoDetector:
    def __init__(self, companion_link=None):
        if companion_link is None:
            self.companion_link = MavproxyLink()
        else:
            self.companion_link = companion_link
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_100)
        self.parameters = cv2.aruco.DetectorParameters()

        self.pid = PIDController(kp=0.1, ki=0.01, kd=0.01)

        # Initialize frame variables
        self.frame = None
        self.processed_frame = None

        # Detection thread
        # self.detection_thread = threading.Thread(target=self.detect_markers_in_thread)
        # self.detection_thread.daemon = True
        # self.detection_thread.start()

    def update_frame(self, frame):
        """
        Updates the frame for detection.
        
        Args:
            frame: The frame to process for ArUco marker detection.
        """
        self.frame = frame

    def detect_markers_in_thread(self):
        """
        Detects ArUco markers in the frame in a separate thread.
        """
        while True:
            if self.frame is not None:
                self.processed_frame = self.detect_aruco_markers(self.frame)

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

        print(f"Detected markers: {ids}")

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
                    self.pid.update(x_diff, y_diff)
                    self.companion_link.control_pixhawk(Message())
                    print("Marker is within the center circle. No movement needed.")

                break  # Process only the first marker for simplicity
        else:
            self.companion_link.control_pixhawk(Message())

        return frame

    def move_camera(self, x_diff, y_diff):
        """
        Controls camera movement based on marker position.

        Args:
            x_diff: Difference between the center of the frame and the marker on the x-axis.
            y_diff: Difference between the center of the frame and the marker on the y-axis.
        """
        message = Message()

        # Update the camera position based on the PID controller
        x_output, y_output = self.pid.update(x_diff, y_diff)

        if abs(x_diff) > 10:
            value = 1500 + int(x_output)
            if value > 1800:
                value = 1800
            elif value < 1200:
                value = 1200
            
            message.set_value("armed", True)
            message.set_value("lateral", value)
        if abs(y_diff) > 10:
            value = 1500 + int(y_output)
            if value > 1800:
                value = 1800
            elif value < 1200:
                value = 1200

            message.set_value("armed", True)
            message.set_value("forward", value)

        self.companion_link.control_pixhawk(message)

    
