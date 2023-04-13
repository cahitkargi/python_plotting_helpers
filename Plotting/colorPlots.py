import numpy as np
from .colorFuncs import normalizeCMAP

def ColorPlot(xValues, yValues, data, ax, cbarMax=1, cbarMin=0, cmap='YlGn', logColorScale=False): #pylint:disable=too-many-arguments
    """
    plots a `pcolormesh` from the given x,y, and data values but also uses some of the functions from `colorFuncs` to
    create custom colormaps and normalise.

    For every x values, the number of y values should be the same. Color plot of irregular data, i.e. number of y values
    are different for each x, is done by the `irregColorPlot`.

    Parameters
    ----------
    xValues : List | Array
        X values for the plot (no need to create meshgrid, just a single list)
    yValues : List | Array
        Y values for the plot (no need to create meshgrid, just a single list)
    data : List | Array
        Z vales for the plot (should have the proper shape for the given x and y)
    ax : axes
        axes object to plot in
    cbarMax : int, optional
        upper limit of the colormap, by default 1
    cbarMin : int, optional
        lower limit of the colormap, by default 0
    cmap : str, optional
        name of the colormap, by default 'YlGn'
    logScale : bool, optional
        If True, the colormap is log separated, by default False

    Returns
    -------
    pcolormesh
        returns the same return as the pcolormesh
    """
    Y, X = np.meshgrid(yValues, xValues)
    cm = createMAP(cmap)
    surf1 = ax.pcolormesh(X, Y, data, cmap=cm, norm=normalizeCMAP(cm, cbarMin, cbarMax, logColorScale), rasterized=True)
    return surf1

def irregColorPlot(xValues, yValue, data, ax, cbarMax=1, cbarMin=0, cmap='YlGn', logColorScale=False, zFullRange=True): #pylint:disable=too-many-arguments, too-many-locals
    """
    plots a `pcolormesh` for an irregular data, which means the number of y values is different for x values.
    Currently, I use it only for step size sweeps, so it works with a yValue rather than a list of yValues.
    The yValue, in my case, is the total simulation time, so the number of steps for each step size different.
    In this implementation, the yValue option also allows me to plot for any time t that is smaller than the full data.
    It can be modified to make it more general, provided it still works fast enough and keeps the existing features.

    TODO update docstrings

    For regular data, it is better to use `ColorPlot`.

    Parameters
    ----------
    xValues : List | Array
        X values for the plot (no need to create meshgrid, just a single list)
    yValue : float | int
        a single y value, i.e. the limit for the y-axes
    data : List | Array
        Z vales for the plot (should have the proper shape for the given x and y)
    ax : axes
        axes object to plot in
    cbarMax : int, optional
        upper limit of the colormap, by default 1
    cbarMin : int, optional
        lower limit of the colormap, by default 0
    cmap : str, optional
        name of the colormap, by default 'GrYl'
    logScale : bool, optional
        If True, the colormap is log separated, by default False

    Returns
    -------
    pcolormesh
        returns the same return as the pcolormesh
    """
    yNum = isinstance(yValue, (int, float))

    for ind in range(len(xValues)-1):
        X0 = [xValues[ind], xValues[ind+1]]
        Y0 = [x*X0[0] for x in range(int(yValue//X0[0])+1)] if yNum else yValue[ind]
        Z0 = [] if zFullRange else [[val] for val in data[ind]]
        if len(Z0) == 0:
            for bkg in range(len(Y0)-1):
                z0 = []
                z0.append(data[ind][bkg])
                Z0.append(z0)
        cm = createMAP(cmap)
        surf1 = ax.pcolormesh(X0, Y0, Z0, cmap=cm, norm=normalizeCMAP(cm, cbarMin, cbarMax, logColorScale), rasterized=True)
    return surf1
