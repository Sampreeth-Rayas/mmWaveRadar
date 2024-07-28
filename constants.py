
no_of_channels = 4
#We will use one of the files. We can uncomment the file we are going to use for testing and comment rest of them.
file_name = 'D:\\Radar\\Data\\AWR1843_data\\CarOutScooterIn_03Mar.bin'
#file_name = 'D:\\Radar\\Data\\AWR1843_data\\Moving1o.bin'
#file_name = 'D:\\Radar\\Data\\AWR1843_data\\StaticObject1.bin'
#file_name = 'D:\\Radar\\Data\\AWR1843_data\\StaticRotatingBehindCoverObj1.bin'
#file_name = 'D:\\Radar\\Data\\AWR1843_data\\StaticRotatingObj1.bin'

frame_id = 1
int_size = 16
chirp_size = 256    #256 complex numbers not bytes
no_of_rows = 128
frame_size = 2 * int_size * chirp_size * no_of_rows     #2 for 2 integer values in a complex number = 1048576
