from mosaic import image_consolodation
from mosaic import image_tiling
import argparse
import os

def main(args):
    # assign variables and call the appropriate functions

    input_image = args.input_image
    image_table = args.image_table
    output_image = args.output_image
    image_directory = args.image_directory
    for arg in args.__dict__:
        print(arg, args.__dict__[arg])
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
                tile_shape=(20,20), 
                scaling_factor=2)
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
                'Currently, the search algorithm will match only files with '
                'one of the following extensions tif, tiff, png, bmp, jpg, and jpeg. '
                'It will search under the given directory and all subdirectories.'
                )
            )
    args = parser.parse_args()
    main(args)

if __name__ == '__main__':
    parse_arguments() 
