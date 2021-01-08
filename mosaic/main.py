from mosaic import image_consolodation
from mosaic import image_tiling
import re
import argparse
import os

def main(args):
    # assign variables and call the appropriate functions

    input_image = args.input_image
    image_table = args.image_table
    output_image = args.output_image
    image_directory = args.image_directory
    tile_dimensions = args.tile_dimensions
    scaling_factor = args.scaling_factor
    for arg in args.__dict__:
        print(arg, args.__dict__[arg])

    match = re.match(r'\d+x\d+', tile_dimensions)
    if match:
        s = match.group()
        h, w = s.split('x')
        tile_dimensions = (int(h), int(w))
    else:
        default = (30, 30)
        print(f"Bad tile dimensions: {tile_dimensions}")
        print(f"Resetting default: {default}")
        tile_dimensions = default
    if scaling_factor > 0:
        pass
    else:
        default = 1
        print(f"Bad scaling factor: {scaling_factor}\n Expected a float greater than zero.")
        print(f"Resetting default: {default}")
        scaling_factor = default

    if image_directory:
        basename = os.path.basename(image_directory)
        computer = image_consolodation.ColorStatisticComputer(
                input_directory=image_directory,
                output_directory=None
                )
        computer.walk()
        computer.export(file_name=f"{basename}.csv")
    else:
        timmy = image_tiling.TiledImage(
                image_path=input_image, 
                tile_shape=tile_dimensions, 
                scaling_factor=scaling_factor)
        image_df = image_tiling.pd.read_csv(image_table)
        out_image_matrix = timmy.make(image_df, unique_flag=False)
        image_tiling.cv2.imwrite(output_image, out_image_matrix)



def parse_arguments():
    # parse arguments for the image tiler


    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-i', 
            '--input_image', 
            type=str, 
            help='The source image.'
            )
    parser.add_argument(
            '-t', 
            '--image_table', 
            type=str, 
            help=('The image source table to use for generating '
                'the output image.')
            )
    parser.add_argument(
            '-o',
            '--output_image',
            type=str,
            help='The path where the output image will be put.'
            )

    parser.add_argument(
            '-d',
            '--image_directory',
            type=str,
            help=('The directory under which images will be searched. '
                'This will generate a .csv file with the same name as the directory on which you\'ve '
                'run the utility.'
                'This resultant csv will be your image_table to be used in generating mosaics.'
                'Currently, the search algorithm will match only files with '
                'one of the following extensions tif, tiff, png, bmp, jpg, and jpeg. '
                'It will search under the given directory and all subdirectories.'
                )
            )
    parser.add_argument(
            '-hxw',
            '--tile_dimensions',
            type=str,
            help=('The width and height (in pixels) of each tile in the mosaic. '
                'This should be represented as "HxW" where W is the width and H is the height '
                '(e.g. 640x480).'
                'Larger dimensions result in larger mosaic tiles while smaller dimensions result in smaller mosaic tiles.'
                ),
            default='30x30'
            )
    parser.add_argument(
            '-S',
            '--scaling_factor',
            type=float,
            help=('The multiple by which the input image will be resized (this is applied to both x and y axies). '
                'So, a scaling_factor of 0.5 will make both the x and y axies of the resultant image half the length of the input '
                'hence the resultant image will be one quarter of the area of the input image. '
                'The same applies for scaling_factors greater than 1 except the resultan image will be larger. '
                'This is especially useful for smaller images. '
                ),
            default=1
            )
    args = parser.parse_args()
    main(args)

if __name__ == '__main__':
    parse_arguments() 
