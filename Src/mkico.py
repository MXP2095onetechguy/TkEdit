from pathlib import Path
from PIL import Image


def bake_one_big_png_to_ico(sourcefile, targetfile, sizes=None):
    """Converts one big PNG into one ICO file.

    args:
        sourcefile (str): Pathname of a PNG file.
        targetfile (str): Pathname of the resulting ICO file.
        sizes (list of int): Requested sizes of the resulting
            icon file, defaults to [16, 32, 48].

    Use this function if you have one big, square PNG file
    and don’t care about fine-tuning individual icon sizes.

    Example::

        sourcefile = "Path/to/high_resolution_logo_512x512.png"
        targetfile = "Path/to/logo.ico"
        sizes = [16, 24, 32, 48, 256]
        bake_one_big_png_to_ico(sourcefile, targetfile, sizes)
    """
    if sizes is None:
        sizes = [16, 32, 48]
    icon_sizes = [(x, x) for x in sizes]
    Image.open(sourcefile).save(targetfile, icon_sizes=icon_sizes)


def bake_several_pngs_to_ico(sourcefiles, targetfile):
    """Converts several PNG files into one ICO file.

    args:
        sourcefiles (list of str): A list of pathnames of PNG files.
        targetfile (str): Pathname of the resulting ICO file.

    Use this function if you want to have fine-grained control over
    the resulting icon file, providing each possible icon resolution
    individually.

    Example::

        sourcefiles = [
            "Path/to/logo_16x16.png",
            "Path/to/logo_32x32.png",
            "Path/to/logo_48x48.png"
        ]
        targetfile = "Path/to/logo.ico"
        bake_several_pngs_to_ico(sourcefiles, targetfile)
    """

    # Write the global header
    number_of_sources = len(sourcefiles)
    data = bytes((0, 0, 1, 0, number_of_sources, 0))
    offset = 6 + number_of_sources * 16

    # Write the header entries for each individual image
    for sourcefile in sourcefiles:
        img = Image.open(sourcefile)
        data += bytes((img.width, img.height, 0, 0, 1, 0, 32, 0, ))
        bytesize = Path(sourcefile).stat().st_size
        data += bytesize.to_bytes(4, byteorder="little")
        data += offset.to_bytes(4, byteorder="little")
        offset += bytesize

    # Write the individual image data
    for sourcefile in sourcefiles:
        data += Path(sourcefile).read_bytes()

    # Save the icon file
    Path(targetfile).write_bytes(data)

print("Making ico from png")
bake_one_big_png_to_ico("./asset/TkEdit.png", "./asset/TkEditI.ico")
print("Ico generation is finished")