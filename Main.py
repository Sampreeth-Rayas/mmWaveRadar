import Preprocessor
import Processor
import Charts
from constants import *

class Manin:
    def main(self):
        preprocessor = Preprocessor()
        preprocessor.set_frame_id(1)
        preprocessor.read_file()
        file_len = preprocessor.get_file_len()
        '''
        
        
        '''
        charts = Charts()
        charts.plot_surface_chart()
