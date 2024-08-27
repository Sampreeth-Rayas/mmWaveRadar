from Preprocessor import *
from Processor import *
from Charts import *
from constants import *
import numpy as np

if __name__ == '__main__':
    frame_id = 1000
    print('Start execution !!')
    #for i in range(1, 4000, 4000):
    chart = Charts()
    chart.prepare('100')
    #for i in range (1, 2300, 500):
    preprocessor = Preprocessor()

    preprocessor.set_frame_id(frame_id)
    if preprocessor.read_file() is False:
        print('Reading error. Exiting')
        exit(-1)
    max_no_frames = preprocessor.get_max_frames()
    print('LVDS :', np.array(preprocessor.lvds_data))
    processor = Processor()
    processor.populate_chammel_data(preprocessor.lvds_data)
    processor.sum_channel_data()
    processor.perform_1D_fft()
    processor.set_resolution(10)
    processor.populate_abs_data(frame_id, max_no_frames, False)
    print('One dim FFT ABS FFT data', np.array(processor.abs_fft))

    #chart.set_title_labels('One Dim FFT (Not scaled)', 'Time', 'Distance', '1D FFT Value')
    #chart.plot_surface_chart(processor.abs_fft)
    #chart.show()

    #print('I and Q data :', np.array(processor.i_and_q_data))
    #print('Processed I and Q data :', np.array(processor.proccessed_i_and_q))
    processor.one_dim_fft = None
    processor.perform_2D_fft()
    processor.abs_fft = []
    processor.populate_abs_data(frame_id, max_no_frames, True)
    print(' Max Frames :', max_no_frames)
    print('ABS FFT data', np.array(processor.abs_fft) )

    print('Dimesnion :', np.array(processor.abs_fft).shape)
    #chart.clear_charts()
    chart.set_title_labels('Two Dim FFT (Not scaled)', 'Time', 'Distance', 'Relative Speed (Unprocessed)')
    chart.plot_surface_chart(processor.abs_fft)
    chart.show()

