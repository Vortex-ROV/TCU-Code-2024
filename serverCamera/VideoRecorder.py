import os
import cv2

class VideoRecorder:
    """
    Handles video recording operations.
    
    Args:
        frame_size (tuple): Size of the frames to record (width, height).
        output_filename (str): Name of the output video file (default: 'output.mp4').
    """

    @staticmethod
    def get_num_of_files(directory):
        """Counts the number of files in the given directory."""
        return len(os.listdir(directory))

    def __init__(self, frame_size):
        # Ensure the 'videos' directory exists
        self.video_directory = "videos"
        if not os.path.exists(self.video_directory):
            os.makedirs(self.video_directory)  # Create the directory if it doesn't exist
        
        # Generate the output filename based on the number of files
        num_files = self.get_num_of_files(self.video_directory)
        self.output_filename = os.path.join(self.video_directory, f'output_{num_files}.mp4')
        
        self.frame_size = frame_size
        self.recording = False
        self.out = None

    def start_recording(self):
        """Initializes the video writer and starts recording."""
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = cv2.VideoWriter(self.output_filename, fourcc, 20.0, self.frame_size)
        self.recording = True
        print(f"Recording started... Output file: {self.output_filename}")

    def stop_recording(self):
        """Stops recording and releases the video writer."""
        self.recording = False
        if self.out is not None:
            self.out.release()
            print("Recording stopped.")

    def write_frame(self, frame):
        """Writes a frame to the video file if recording."""
        # flipped = cv2.flip(frame,0)
        if self.recording and self.out is not None:
            self.out.write(flipped)
