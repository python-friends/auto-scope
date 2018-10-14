import pandas
import numpy

from pathlib import Path
from skimage import io
from skimage.draw import circle
from matplotlib import pyplot as plt

# Just some test functions for now:

def get_image_stats(img_dir: str) -> pandas.DataFrame:

    """Get image statistics like pixel dimension
    for sanity checks.
    :param img_dir: dir with jpeg files
    :return: image stats dataframe
    """

    images = [io.imread(str(fpath)) for fpath in
              Path(img_dir).glob("*.jpg")]

    return pandas.DataFrame(None)

def read_annotations(fpath) -> pandas.DataFrame:

    """Read annotation file, will be made
    by Leaflet annotation app.
    :param fpath
    :return annotation dataframe
    """

    return pandas.read_csv(fpath)


def draw_marker(image: numpy.array, coordinates: tuple):

    """Draw black circle marker on image
    to test annotation coordinates from
    manually annotated images.
    :param image: image io with skimage
    :param coordinates: parasite location
    :return:
    """

    r,c = circle(*coordinates, 20)

    image[r, c] = 0

    plt.imshow(image)
    plt.show()
