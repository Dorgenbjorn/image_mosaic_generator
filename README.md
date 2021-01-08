# image_mosaic_generator

This is the help string:
```
usage: __main__.py [-h] [-i INPUT_IMAGE] [-t IMAGE_TABLE] [-o OUTPUT_IMAGE]
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
                        Currently, the search algorithm will match only files
                        with one of the following extensions tif, tiff, png,
                        bmp, jpg, and jpeg. It will search under the given
                        directory and all subdirectories.
```

To generate your source image table, simply run
the program using the `-d` flag specifying the source directory
under which you would like to generate this table from.
After generating the source table, the program will exit.

The image table is required for generating an image mosaic.
Moreover, take care not to move the source images after generating your table.
The paths given in the image table tell the program where to find a particular
image to be used in your new creation and this utility will not know where
you've put it until the table is regenerated.

It is also possible to manually alter the image table to exclude images you
don't want in your mosaic.
Simply delete the row with the unwanted image and it will be as if it never existed.
