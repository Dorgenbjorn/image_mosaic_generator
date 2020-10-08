# image_mosaic_generator

This is the help string:
```
usage: main.py [-h] [-i INPUT_IMAGE] [-t IMAGE_TABLE] [-o OUTPUT_IMAGE]
               [-d IMAGE_DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_IMAGE, --input_image INPUT_IMAGE
                        The source image.
  -t IMAGE_TABLE, --image_table IMAGE_TABLE
                        The image source table to use for generating the
                        output image.
  -o OUTPUT_IMAGE, --output_image OUTPUT_IMAGE
                        The path where the output image will be put.
  -d IMAGE_DIRECTORY, --image_directory IMAGE_DIRECTORY
                        The directory under which images will be searched.
                        Currently, the search algorythm will match only files
                        with one of the following extensions tif, tiff, png,
                        bmp, jpg, and jpeg. It will search under the given
                        directory and all subdirectories.
```
