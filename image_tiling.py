from functools import reduce
import numpy as np
import pandas as pd
import cv2

class TiledImage:


    image = None
    tile_shape = None
    partitions = None
    color_matrix = None
    

    def __init__(self, image_path, tile_shape=(100, 100), scaling_factor=None):
        """Does the following:
        0. initialize self.image
        1. extract the height and width of the image;
        2. partition the image;
        3. calculate the average color value for each partition;
        4. store these average color values in a parallel matrix;
        """

        image = cv2.imread(image_path)
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
        if scaling_factor is None:
            pass
        else:
            x, y, c = self.image.shape
            self.image = cv2.resize(self.image, (y*scaling_factor, x*scaling_factor), interpolation=cv2.INTER_CUBIC)
        self.tile_shape = tile_shape
        height, width, _  = self.image.shape
        self.partition_matrix = self.partition(height, width)
        self.color_matrix = self.generate_color_matrix(self.partition_matrix)


    def make(self, image_dataframe, unique_flag=False):
        """Does the following:
        0. queries the image dataframe for CIELab color statistics;
        1. make a matrix of the distance between the average color of
            a tile on self.image and the average color of each
            image in the dataframe;
        2. take the argmin of this matrix to get the "best match" for
            and image tile, then replace that "best match" with np.inf (if duplicate images are not allowed)
            repeating the process until every image tile has a match
        3. load each of the selected images, rescale each image to the size of the tile, then
            concatenate each image together to get the resultant image;
        4. return the image.
        """
        
        distance_matrix = []
        for i, row in enumerate(self.color_matrix):
            for j, color in enumerate(row):
                d_L = np.array(image_dataframe["mean_L"] - color[0])**2
                d_a = np.array(image_dataframe["mean_a"] - color[1])**2
                d_b = np.array(image_dataframe["mean_b"] - color[2])**2
                dist = d_L + d_a + d_b
                distance_matrix.append(dist)
                
        distance_matrix = np.array(distance_matrix)
        if unique_flag:
            mapping_matrix = self.gen_unique_mapping_matrix(distance_matrix)
        else:
            mapping_matrix = self.gen_mapping_matrix(distance_matrix)
        image = self.construct_image(mapping_matrix, image_dataframe)
        return image
    
    
    def gen_mapping_matrix(self, distance_matrix):
        
        mapping_matrix = np.full(self.color_matrix.shape[:2], -1, dtype=int)
        mp_n, mp_m = mapping_matrix.shape
        column_vector = np.apply_along_axis(np.argmin, 1, distance_matrix)
        for i, j in enumerate(column_vector):
            mapping_matrix[i//mp_m, i%mp_m] = j
        return mapping_matrix
        
        
    def gen_unique_mapping_matrix(self, distance_matrix):
        
        mapping_matrix = np.full(self.color_matrix.shape[:2], -1, dtype=int)
        mp_n, mp_m = mapping_matrix.shape
        n, m = distance_matrix.shape
        char_array = ["-", "\\", "|", "/"]
        c = 0
        while np.min(mapping_matrix) <= -1:
            k = np.argmin(distance_matrix)
            i, j = k//m, k%m
            val = distance_matrix[i, j]
            if np.isinf(val):
                break
            distance_matrix[:, j] = np.inf
            distance_matrix[i, :] = np.inf
            mapping_matrix[i//mp_m, i%mp_m] = j
            print(char_array[c], end="\r")
            c += 1
            if c >= 4:
                c = 0
        if np.min(mapping_matrix) <= -1:
            print("Not enough images.")
            return None
        return mapping_matrix
    
    
    def construct_image(self, mapping_matrix, image_dataframe):
        
        image_cache = dict()
        read_n_scale = lambda p: cv2.resize(cv2.imread(p), self.tile_shape, interpolation=cv2.INTER_CUBIC)
        tiles = []
        for row in mapping_matrix:
            im_paths = image_dataframe["path"].iloc[row]
            images = []
            for p in im_paths:
                if p in image_cache.keys():
                    images.append(image_cache[p])
                else:
                    im = read_n_scale(p)
                    image_cache.update({p: im})
                    images.append(im)
            tiles.append(images)
        strips = [np.concatenate(row, axis=1) for row in tiles]
        image = np.concatenate(strips, axis=0)
        return image
    

    def partition(self, h, w):
        """Takes height and width of the image as argumens
        (h and w respectively.)
        Returns an nxmx4 numpy array
        where each cell describes the position of 
        the image tile (relative to others), and the channels describe
        the absolute position of the image tile in pixels (we can 
        derrive the shape of the tile from this information.)
        """
        
        a, b = self.tile_shape
        n = int(h/a)
        m = int(w/b)
        partition_matrix = []
        for i in range(n):
            partition_row = []
            i_0 = a*i
            i_n = i_0 + a
            for j in range(m):
                j_0 = b*j
                j_n = j_0 + b
                tile = (slice(i_0, i_n), slice(j_0, j_n))
                partition_row.append(tile)
            partition_matrix.append(partition_row)
        return np.array(partition_matrix)


    def generate_color_matrix(self, partition_matrix):
        
        color_matrix = []
        for row in partition_matrix:
            color_row = []
            for tile in row:
                row_slice, column_slice = tile
                image = self.image[row_slice, column_slice, :]
                mean_color = self.average_colors(image)
                color_row.append(mean_color)
            color_matrix.append(color_row)
        return np.array(color_matrix)


    def average_colors(self, image):
        
        mean_L = image[:, :, 0].mean()
        mean_a = image[:, :, 1].mean()
        mean_b = image[:, :, 2].mean()
        return np.array([mean_L, mean_a, mean_b])