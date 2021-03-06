import os
import shutil
import subprocess
import re
import pprint
import pandas as pd
import numpy as np
import cv2
from functools import reduce


class Consolodator:


    input_directory = None
    output_directory = None
    extensions = None


    def __init__(self, input_directory, output_directory):
        
        self.input_directory = input_directory
        self.output_directory = output_directory
        if output_directory:
            mkdir(output_directory)
        # TODO: Make a configuration file for extensions.
        self.extensions = ["tif", "tiff", "png", "bmp", "jpg", "jpeg"]


    def walk(self):

        for root, dirs, files in os.walk(self.input_directory):
            pprint.pprint(root)
            pprint.pprint(files)
            matched_file_names = [
                    self.validate_file(f) for f in files]
            matched_file_names = list(
                    filter(lambda f: not not f, matched_file_names)
                    )
            for f in matched_file_names:
                path = os.path.join(root, f)
                self.process_file(path)
            print("-"*42)
        return None


    def process_file(self, path):

        shutil.copy(path, self.output_directory)
        print("COPIED {} TO {}".format(path, self.output_directory))


    def validate_file(self, filename):
        
        regex_list = [
                self.make_extension_regex(e) for e in self.extensions]
        for regex in regex_list:
            if self.has_extension(filename, regex):
                return filename
            else:
                pass
        return ''


    def has_extension(self, filename, regex):
        
        return not (re.match(regex, filename.lower()) is None)


    def make_extension_regex(self, extension):
        
        regex = r".+\.{0}$".format(extension)
        return regex



class ColorStatisticComputer(Consolodator):


    color_stats_df = None


    def __init__(self, input_directory, output_directory):

        Consolodator.__init__(self, input_directory, output_directory)
        self.color_stats_df = pd.DataFrame()


    def process_file(self, path):

        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
        mean_L = image[:,:,0].mean()
        mean_a = image[:,:,1].mean()
        mean_b = image[:,:,2].mean()
        df = pd.DataFrame()
        df["path"] = [path]
        df["mean_L"] = [mean_L]
        df["mean_a"] = [mean_a]
        df["mean_b"] = [mean_b]
        self.color_stats_df = self.color_stats_df.append(
                df.set_index("path")
                )


    def export(self, file_name="image_statistics.csv"):

        self.color_stats_df.to_csv(file_name)



###########################################################
#    
#    Helper functions:
#    1. mkdir
#
###########################################################

def mkdir(path):


    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
