import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.animation import FuncAnimation

num_chirps = 128  # Number of chirps per frame
num_rx_antennas = 4  # Number of receiving antennas
num_samples = 256  # Number of samples per chirp
range_doppler_array = []
Fs = 5000e3  # Sampling rate in Hz
S = 8e12  # Chirp slope in Hz/s
T_chirp = 56e-3  # Chirp duration in seconds
frame_iterator = 0
window_width = 5

#fig, ax = plt.subplots()
time_distance = []
total_doppler_array = []
#empty_row = [0 for i in range(num_samples)]
empty_row = [0 for i in range(num_samples)]
total_doppler_array = [empty_row for i in range(num_chirps)]
total_doppler_array = np.array(total_doppler_array)

#time_distance = [[0.0]*num_samples]*1000
empty_float_zeros = np.zeros(num_samples, dtype='float32' )
time_distance = [empty_float_zeros for i in range(1000)]
time_distance = np.array(time_distance)

def load_lvds_data(file_path, num_chirps, num_rx_antennas, num_samples):
    # Load LVDS data and reshape according to the radar setup
    # This assumes binary format. Adapt as needed for your LVDS data format.
    raw_data = np.fromfile(file_path, dtype=np.int16)
    print('Data len : ', len(raw_data))
    size = int(len(raw_data))
    data = []
    for i in range(0, size, 2):
        data.append(complex(raw_data[i], raw_data[i+1]))
    return np.array(data).reshape(-1, num_chirps, num_rx_antennas, num_samples)

def range_doppler_processing(data, num_samples, num_chirps, doppler_padding_factor, threshold_dB):
    # Perform Range FFT (along the fast-time axis, samples)
    range_fft = np.fft.fft(data, axis=-1, n=num_samples)
    range_fft = range_fft[:, :, :, :num_samples // 2]  # Use one side of FFT (positive frequencies)
    doppler_fft = np.fft.fft(range_fft, axis=1, n=num_chirps*doppler_padding_factor)
    doppler_map = np.fft.fftshift(doppler_fft, axes=1)  # Shift zero frequency to center
    # Compute power for Range-Doppler map
    range_doppler_map = np.abs(doppler_map)
    range_doppler_map = 20 * np.log10(range_doppler_map / np.max(range_doppler_map))  # Normalize and convert to dB
    #range_doppler_map[range_doppler_map < threshold_dB] = threshold_dB
    return range_doppler_map

def plot_range_doppler_map_with_sampling_freq(range_doppler_map, num_samples, num_chirps, Fs, S, T_chirp):
    # Calculate range and Doppler bins
    range_resolution = Fs / (2 * S)
    max_range = range_resolution * (num_samples / 2 )
    range_bins = np.linspace(0, 100, num_samples // 2)
    range_bins = np.flip(range_bins)
    doppler_resolution = 1 / (num_chirps * T_chirp )
    max_velocity = doppler_resolution * (num_chirps / 2)
    doppler_bins = np.linspace(-max_velocity, max_velocity, num_chirps)
    range_doppler_map[range_doppler_map < -150 ] = 0
    i_max, j_max = range_doppler_map.shape
    for i in range(i_max):
        for j in range(j_max):
            min = range_doppler_map[i][j]
            if min != 0:
                total_doppler_array[i][j] = min

    if frame_iterator == rows - window_width:
        plt.title('Range-Doppler Map ' + str(frame_iterator))
        i_max, j_max = total_doppler_array.shape
        for i in range(i_max):
            #print('')
            for j in range(j_max) :
                if j > 127 and j < 129:
                    total_doppler_array[i][j] = -130
                elif total_doppler_array[i][j] != 0:
                    #if i > 70 and total_doppler_array[i][j] < -80:
                    if abs(total_doppler_array[i][j]) - abs(j - 128) > 80:
                        total_doppler_array[i][j] = 0
                    elif total_doppler_array[i][j] > -120 :
                        if j > 128:
                            total_doppler_array[i][j] = -120
                        else:
                            total_doppler_array[i][j] = 120
                    elif total_doppler_array[i][j] > -110 :
                        if j > 128:
                            total_doppler_array[i][j] = -110
                        else:
                            total_doppler_array[i][j] = 110
                    elif total_doppler_array[i][j] > -100 :
                        if j > 128:
                            total_doppler_array[i][j] = -100
                        else:
                            total_doppler_array[i][j] = 100
                    elif total_doppler_array[i][j] > -90 :
                        if j > 128:
                            total_doppler_array[i][j] = -90
                        else:
                            total_doppler_array[i][j] = 90
                    elif total_doppler_array[i][j] > -80 :
                        if j > 128:
                            total_doppler_array[i][j] = -80
                        else:
                            total_doppler_array[i][j] = 80
                    else :
                        if j > 128:
                            total_doppler_array[i][j] = -50
                        else:
                            total_doppler_array[i][j] = 50

                if total_doppler_array[i][j] != 0 and abs(total_doppler_array[i][j]) != 50 and total_doppler_array[i][j] != -130:
                    speed = -max_velocity + ((j+1)*2*max_velocity/(j_max))
                    distance = (100*(i+1)/(i_max))
                    if speed != 0 and distance != 0:
                        time = int(abs(speed/distance * 1000))
                        if time < 1000 and time_distance[time][0] < 255:
                            #print('[', time, ', ', time_distance[time][0], '] =', speed)
                            time_distance[time][0] = int(time_distance[time][0]) + 1
                            #print('Verify ', time_distance[time][0], ' j=', j, ' : ', total_doppler_array[i][j])
                            jIndex = int(time_distance[time][0])
                            time_distance[time][jIndex] = distance
                            print('Verify :', jIndex, ' Time:', time, ' speed :', speed, ' distance :', distance, end=' ')
                            print(time_distance[time][int(jIndex)])

        np.set_printoptions(threshold=sys.maxsize)
        print('Time distance array')
        x_max, y_max = np.array(time_distance).shape
        print('Shape :::',x_max, '  ', y_max )
        x_axis = []
        y_axis = []
        prev_val = 0
        for i in range(x_max) :
            x_axis.append(i/10)
            if time_distance[i][0] == 0:
                y_axis.append(prev_val)
                continue
            j = int(time_distance[i][0])
            print(' ', i, end=' :')
            #x_axis.append(i)
            if abs(prev_val - time_distance[i][1]) < 15:
                prev_val = time_distance[i][1]
            y_axis.append(prev_val)
            for k in range(j+1) :
                print(time_distance[i][k], end =' ')
            print('')

        x_axis = np.array(x_axis)
        y_axis = np.array(y_axis)

        plt.imshow(total_doppler_array, aspect='auto', extent=[doppler_bins[0], doppler_bins[-1], range_bins[-1], range_bins[0]], cmap='jet')
        plt.colorbar(label='')
        plt.xlabel('Speed (m/s)')
        plt.ylabel('Range (m)')
        plt.title('Cumulative Speed-Range Map')
        plt.show()

def update_plot(frame) :
    plot_range_doppler_map_with_sampling_freq(np.transpose(range_doppler_array), num_samples, num_chirps, Fs, S,
                                              T_chirp)

def plot_range_doppler_map(range_doppler_map, max_range, max_velocity):
    plt.title('Range-Doppler Map ' + frame_iterator)
    plt.figure(figsize=(10, 6))
    plt.imshow(range_doppler_map, aspect='auto', extent=[-max_velocity, max_velocity, 0, max_range], cmap='jet')
    plt.show()

# Radar parameters (change these according to your setup)
file_path = 'D:\\Radar\\From LRDE\\Moving1i1o.bin'  # Path to your LVDS data
#file_path = 'D:\\Radar\\From LRDE\\Moving1o.bin'
#file_path = 'D:\\Radar\\Data\\AWR1843_data\\CarOutScooterIn_03Mar.bin'
#file_path = 'D:\\Radar\\Data\\AWR1843_data\\FanData_16_04_2023.bin'

#file_path = 'D:\\Radar\\Testdata\\20240917\\Round1\\adc_data_Raw_0.bin'
# Physical parameters (adjust according to radar system)
max_range = 100  # in meters
max_velocity = 30  # in m/sra

doppler_padding_factor = 2  # Zero-padding factor for Doppler FFT
threshold_dB = -40  # Threshold in dB to remove weak/aliased signals

#Load and process data
data = load_lvds_data(file_path, num_chirps, num_rx_antennas, num_samples)
range_doppler_map = range_doppler_processing(data, num_samples, num_chirps, doppler_padding_factor, threshold_dB)
print('Range Doppler matrix ', np.array(range_doppler_map).shape)
# Plot the Range-Doppler map
rows, cols, channels, frames = range_doppler_map.shape
print('Dimensions :', rows, cols, channels, frames)
range_doppler = []
zFrames = []
yFrames = []
frames_data = []
range_doppler_map = np.array(range_doppler_map)
plt.xlabel('Velocity (m/s)')
plt.ylabel('Range (m)')
plt.figure(figsize=(10, 6))

update_interval = 100


for i in range(0, rows, window_width):
    yFrames = []
    for j in range (cols):
        #for k in range(channels) :
        zframes = []
        for l in range(frames):
            sum_channel_data = range_doppler_map[i][j][0][l]  + range_doppler_map[i][j][1][l] + range_doppler_map[i][j][2][l] + range_doppler_map[i][j][3][l]
            zframes.append(sum_channel_data)
        yFrames.append(zframes)
    range_doppler_array = np.array(yFrames)
    frame_iterator = i
    plot_range_doppler_map_with_sampling_freq(np.transpose(range_doppler_array), num_samples, num_chirps, Fs, S, T_chirp)