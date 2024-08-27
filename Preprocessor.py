import os
import numpy as np
from constants import file_name, frame_id, frame_size, max_no_frames

'''
This class reads the binary file with the offset depending on the frame Id and stores the data in the raw_data array.
Also, file length is stored in a class variable.
'''

class Preprocessor:

    # Constructor
    def __init__(self):
        self.lvds_data = []
        self.file_size = 0
        self.frame_id = frame_id
        self.file_name = file_name
        self.max_no_frames = max_no_frames

    def get_file_size(self):
        self.file_size = os.path.getsize(self.file_name)
        print(f'File Size : {self.file_size}')
        return self.file_size

    # Reads the binary file and populates the raw data.
    def read_file(self):
        self.get_file_size()
        self.max_no_frames = int(self.file_size / frame_size)
        # We need to verify whether frame_id given is within the max no of frames or not.
        if self.frame_id > self.max_no_frames:
            print(f'ERROR !! Maximum frame Id is {self.max_no_frames}. Current frame_id is {self.frame_id}')
            return False

        offset = (self.frame_id - 1) * frame_size
        print('Offset :', offset, ' Frame Size :', frame_size )
        with open(file_name, 'rb') as fid:
            self.lvds_data = np.fromfile(fid, dtype=np.int16, count=frame_size, offset=offset)
            #self.lvds_data = np.fromfile(fid, dtype=np.int16, offset=offset)

        return True
    '''

    We can have two overriding functions to set the file name and frame id. This we may utilize later in the main function.
    '''
    def set_file_name(self, file_name):
        self.file_name = file_name

    def get_frame_id(self):
        return self.frame_id

    def set_frame_id(self, id):
        self.frame_id = id

    def get_max_frames(self):
        return self.max_no_frames