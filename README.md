# image_mosaic_generator

This is the help string:
```
usage: __main__.py [-h] [-i INPUT_IMAGE] [-t IMAGE_TABLE] [-o OUTPUT_IMAGE]
                   [-d IMAGE_DIRECTORY] [-hxw TILE_DIMENSIONS]
                   [-S SCALING_FACTOR]

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
                        This will generate a .csv file with the same name as
                        the directory on which you've run the utility.This
                        resultant csv will be your image_table to be used in
                        generating mosaics.Currently, the search algorithm
                        will match only files with one of the following
                        extensions tif, tiff, png, bmp, jpg, and jpeg. It will
                        search under the given directory and all
                        subdirectories.
  -hxw TILE_DIMENSIONS, --tile_dimensions TILE_DIMENSIONS
                        The width and height (in pixels) of each tile in the
                        mosaic. This should be represented as "HxW" where W is
                        the width and H is the height (e.g. 640x480).Larger
                        dimensions result in larger mosaic tiles while smaller
                        dimensions result in smaller mosaic tiles.
  -S SCALING_FACTOR, --scaling_factor SCALING_FACTOR
                        The multiple by which the input image will be resized
                        (this is applied to both x and y axies). So, a
                        scaling_factor of 0.5 will make both the x and y axies
                        of the resultant image half the length of the input
                        hence the resultant image will be one quarter of the
                        area of the input image. The same applies for
                        scaling_factors greater than 1 except the resultan
                        image will be larger. This is especially useful for
                        smaller images.
```

To generate your source image table, simply run
the program using the `-d` flag specifying the source directory
where the images from under which will be used to generate this table.
After generating the source table, the program will exit.

The image table is required for generating an image mosaic.
Moreover, take care not to move the source images after generating your table.
The paths given in the image table tell the program where to find a particular
image to be used in your new creation and this utility will not know where
you've put it until the table is regenerated.

It is also possible to manually alter the image table to exclude images you
don't want in your mosaic.
Simply delete the row with the unwanted image and it will be as if it never existed.
