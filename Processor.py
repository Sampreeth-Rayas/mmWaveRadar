from constants import chirp_size, no_of_rows, no_of_channels, max_no_frames, frame_id
import numpy as np
from numpy.fft import fft, ifft, fft2
import math

class Processor:

    def __init__(self):
        # All the below class variables are two dim array with dim 128 x 256
        self.i_and_q_data = []
        self.one_dim_fft = []
        self.two_dim_fft = []
        self.abs_fft = []
        self.two_dim_fft = []
        self.proccessed_i_and_q = []
        self.resolution_percentage = 100

    # Below function populates all the 4 channel data in 4 rows.
    # First row contains all the data of channel1, Second row - channel 2 etc.
    def populate_chammel_data(self, lvds_data):
        no_of_cols = chirp_size
        no_of_chirps = int(len(lvds_data) / (no_of_channels*chirp_size))     # This is no of chirps per channel
        print('no_of_cols ', no_of_cols, ' no_of_chirps :', no_of_chirps)
        #for i in range(0, no_of_rows):
        i = 0
        #for j in range(no_of_channels) :
        row0 = []
        row1 = []
        row2 = []
        row3 = []
        for i in range (no_of_chirps) :
            for k in range(no_of_channels):
                for j in range(0, chirp_size, 4):
                    #base_index = i * no_of_channels*no_of_cols + j*no_of_channels + k
                    base_index = i*no_of_channels*chirp_size + k*chirp_size + j
                    real_part1 = lvds_data[base_index]
                    real_part2 = lvds_data[base_index + 1]
                    imag_part1 = lvds_data[base_index + 2]
                    imag_part2 = lvds_data[base_index + 3]
                    if k == 0 :
                        row0.append(complex(real_part1, imag_part1))
                        row0.append(complex(real_part2, imag_part2))
                    elif k == 1:
                        row1.append(complex(real_part1, imag_part1))
                        row1.append(complex(real_part2, imag_part2))
                    elif k == 2:
                        row2.append(complex(real_part1, imag_part1))
                        row2.append(complex(real_part2, imag_part2))
                    elif k == 3:
                        row3.append(complex(real_part1, imag_part1))
                        row3.append(complex(real_part2, imag_part2))
        self.i_and_q_data.append(row0)
        self.i_and_q_data.append(row1)
        self.i_and_q_data.append(row2)
        self.i_and_q_data.append(row3)
        print('Row0 ', len(row0), 'Row1 ', len(row1), 'Row2 ', len(row2), 'Row3 ', len(row3))

    def sum_channel_data(self):
        array_size = len(self.i_and_q_data[0])
        for i in range (array_size) :
            c = self.i_and_q_data[0][i] + self.i_and_q_data[1][i] + self.i_and_q_data[2][i] + self.i_and_q_data[3][i]
            self.proccessed_i_and_q.append(c)

    def set_resolution(self, percentage):
        self.resolution_percentage = percentage

    def perform_1D_fft(self):
        array = np.reshape(self.proccessed_i_and_q, (-1, 256))
        self.one_dim_fft = fft(array)

    def perform_2D_fft(self):
        array = np.reshape(self.proccessed_i_and_q, (-1, 256))
        print(' Shape :',  np.shape(array))
        self.two_dim_fft = fft2(array)

    def get_filtered_data(self):
        return 0

    def populate_abs_data(self, frame_id, max_no_frames, isTwoDimFFT):    #Here array can be either one_dim_fft or two_dim_fft
        array = None
        if isTwoDimFFT is False:
            array = self.one_dim_fft
        else :
            array = self.two_dim_fft

        rows = len(array)
        cols = len(array[0])
        print('Rows :', rows, ' Columns :', cols)
        empty_row = [0 for i in range(cols)]

        print('Frame ID :', frame_id)
        no_of_empty_rows = int((frame_id-1) * chirp_size * self.resolution_percentage / (4*no_of_channels*100))
        print('Begin rows ', no_of_empty_rows)
        #no_of_empty_rows = frame_id-1
        for i in range (no_of_empty_rows):
            self.abs_fft.append(empty_row)

        print("Dim 1", np.array(self.abs_fft).shape)
        for i in range(rows):
            row = []
            for j in range(cols) :

                if isTwoDimFFT is True:
                    value = 20*math.log10(abs(array[i][j]))
                else :
                    value = 10 * math.log10(abs(array[i][j]))
                row.append(value)
            self.abs_fft.append(row)

        print("Dim 2", np.array(self.abs_fft).shape)

        no_of_empty_rows = int((max_no_frames - frame_id-1)* chirp_size * self.resolution_percentage / (4*no_of_channels*100))
        print('Max Rows =', max_no_frames, ' Frame Id ', frame_id, ' No of rows ', no_of_empty_rows)

        #no_of_empty_rows = max_no_frames - frame_id -1
        for i in range (no_of_empty_rows):
            self.abs_fft.append(empty_row)

        print("Dim 3", np.array(self.abs_fft).shape)

    def get_abs_data_2D_fft(self):
        return 0

