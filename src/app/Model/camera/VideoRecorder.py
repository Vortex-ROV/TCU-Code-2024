import datetime
import cv2
import os

class VideoRecorder:
    """
    Handles video recording operations.
    
    Args:
        frame_size (tuple): Size of the frames to record (width, height).
        output_filename (str): Name of the output video file (default: 'output.mp4').
    """

    def get_num_of_files(directory):
        list = os.listdir(directory)
        number_files = len(list)
        return number_files
        
    def __init__(self, frame_size, output_filename=f'D:/Vortex25/FramesUW/output_{get_num_of_files("D:/Vortex25/FramesUW/")}.mp4'):
        self.frame_size = frame_size
        self.output_filename = output_filename
        self.recording = False
        self.out = None

    def start_recording(self):
        """Initializes the video writer and starts recording."""
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.output_filename, fourcc, 20.0, self.frame_size)
        self.recording = True
        print("Recording started...")

    def stop_recording(self):
        """Stops recording and releases the video writer."""
        self.recording = False
        if self.out is not None:
            self.out.release()
            print("Recording stopped.")

    def write_frame(self, frame):
        """Writes a frame to the video file if recording."""
        if self.recording and self.out is not None:
            self.out.write(frame)