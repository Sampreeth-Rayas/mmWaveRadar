import numpy as np
from constants import file_name, frame_id, frame_size
'''
This class reads the binary file with the offset depending on the frame Id and stores the data in the raw_data array.
Also, file length is stored in a class variable.
'''

class Preprocessor :

    # Constructor
    def __init__(self):
        self.raw_data = []
        self.file_size = 0
        self.no_of_frames = 0

    # Reads the binary file and populates the raw data.
    def read_file(self):

        get_file_size()
        max_no_frames = int(self.file_size/frame_size)
        #We need to verify whether frame_id given is within the max no of frames or not.
        if frame_id > max_no_frames:
            print(f"ERROR !! Maximum frame Id is {max_no_frames}. Current frame_id is {frame_id}")
            return None

        offset = (frame_id-1) * frame_size
        with open(file_name, 'rb') as fid:
            self.raw_data = np.fromfile(fid, dtype=np.int16, count=frame_size, offset=offset)

    def get_file_size(self):
        self.file_size = os.path.getsize(file_name)
        return self.file_size


