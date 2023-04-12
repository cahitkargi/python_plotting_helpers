import os
from typing import List, Union
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lscm
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import BoundaryNorm, LogNorm


def colorCycle(n: int, cmap: str = None) -> List:
    r"""
    Creates a color-cycle (i.e. a list of colors) for a color map.

    some colormap names are: plasma, magma, winter, cool, spring, summer, brg, CMRmap, gnuplot.
    For more see, https://matplotlib.org/3.3.1/gallery/color/colormap_reference.html

    Parameters
    ----------
    n : int
        number of colors
    cmap : str
        name of the colormap

    Returns
    -------
    List
        a list of colors (linearly) uniformly sampled from a colormap
    """
    cmap = getattr(cm, 'viridis' if cmap is None else cmap)
    return [cmap(i) for i in np.linspace(0, 1, n)]


def createCMAP(name: str):
    r"""
    Creates matplotlib colormap from the name of the colormap.

    Parameters
    ----------
    name : str
        name of the colormap
    half : bool
        if True, cuts the custom maps into half (not the matplotlib maps). To cut matplotlib maps, see `cutColorMap`.

    Returns
    -------
    colormap
        returns a colormap
    """
    return plt.get_cmap(name)

def cutColorMap(cmapName='viridis', minLim=0.5, maxLim=1):
    """
    Creates and cuts any colormap from matplotlib into two and returns both pieces as colormaps.

    Use `maxLim` when you also want to simulatenously normalise the color map, but it is only useful if you want to
    normalise a colormap with only positive values. So, for most cases, it is better to just cut a colormap from where
    you want using `minLim` value, then normalise later with `normalizeCMAP`.

    Parameters
    ----------
    cmapName : str, optional
        name of the colormap, by default 'viridis'
    minLim : float, optional
        where to cut the colormap, by default 0.5, i.e. by default in the middle
    maxLim : int, optional
        max of the colormap, by default 1.

    Returns
    -------
    colormap
        returns a colormap
    """
    cmap = plt.get_cmap(cmapName)
    newCmap1 = lscm.from_list('trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minLim, b=maxLim),
                               cmap(np.linspace(minLim, maxLim, 254)))
    newCmap2 = lscm.from_list('trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=0, b=minLim),
                               cmap(np.linspace(0, minLim, 254)))
    return newCmap1, newCmap2

def normalizeCMAP(cmap, llim: Union[float, int], ulim: Union[float, int], logScale: bool = False):
    r"""
    Creates BoundaryNorm object, which is used for normalising the colormaps between the given some min (lower) and max
    (upper) limits.

    Parameters
    ----------
    cmap : colormap
        colormap itself (not its string name)
    llim: Union[float, int]
        lower limit of the colormap
    ulim: Union[float, int]
        upper limit of the colormap
    pnorm: bool
        If True, creates a log separated colormap

    Returns
    -------
    BoundaryNorm
        BoundaryNorm object that normalises the colormap
    """
    levels = MaxNLocator(nbins=256).tick_values(llim, ulim)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True) if not logScale else LogNorm(vmax=ulim, vmin=llim)
    return norm
