import matplotlib.pyplot as plt

def grid(n,m, fig=None):
    """
    Create an n-by-m axis grid (into a given figure)

    Parameters
    ----------
    n : int
        number of rows
    m : int
        number of columns
    fig : figure, optional
        figure object, by default None

    Returns
    -------
    List
        a list contaning the axes.
    """
    #axList = [*[plt.subplot2grid((n, m), (i, j), colspan=1 ,fig=fig) for j in range(m)] for i in range(n)]
    axList = []
    for i in range(n):
        for j in range(m):
            ax = plt.subplot2grid((n, m), (i, j), colspan=1, fig=fig)
            axList.append(ax)
    return axList

def cm2inch(*tupl):#pylint:disable=invalid-name
    """
    cm to inch convertion, used in figure creation to set the sizes in cm.

    Returns
    -------
    tuple
        returns the tuple containing the converted values.
    """
    inch = 2.54
    return tuple(i/inch for i in tupl[0]) if isinstance(tupl[0], tuple) else tuple(i/inch for i in tupl)

def createFigAndAx(width, height, rows=1, columns=1, inCm = True, labels=[], fontsize=12):#pylint:disable=too-many-arguments, dangerous-default-value
    """
    Creates a `rows`-by-`columns` figure with the given `width` and `height` (`inCm` if `True`).

    Parameters
    ----------
    width : float | int
        width of the figure (in cm)
    height : float | int
        height of the figure (in cm)
    rows : int, optional
        number of rows (of axes), by default 1
    columns : int, optional
        number of columns (of axes), by default 1
    inCm : bool, optional
        If True creates the figure with cm dimension, by default True. else uses inch
    labels : list, optional
        x and y axes labels, by default []. these are actually texts placed at relative positions, not actual ax labels.
        This is an older option, and I do not suggest using these.
    fontsize : int, optional
        font size for the labels, by default 12

    Returns
    -------
    tuple
        returns the created figure and the list of axes in the grid.
    """
    size = cm2inch(width, height) if inCm else (width, height)
    fig = plt.figure(figsize=size)
    if len(labels) > 0:
        fig.text(0.004, 0.5, labels[0], va='center', rotation='vertical', fontsize=fontsize)
        fig.text(0.5, 0.0075, labels[1], ha='center', fontsize=fontsize)
    axGrids = grid(rows, columns, fig=fig)
    return fig, axGrids
