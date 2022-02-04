import numpy as np
from quanguru import EigenVectorDist, WignerSurmise

#from ..rmtDistributions import EigenVectorDist, WignerDyson, WignerSurmise, Poissonian
from .colorFuncs import colorCycle

def plotEigStat(data, dimension, ax, bins, stepPlot=True, legend=False, theoryLines=True, density=True, htype='bar',#pylint:disable=too-many-arguments, bad-option-value, dangerous-default-value, too-many-locals
                color=None, labels=[r'COE', r'CUE', r'CSE '], linewidth=1, alpha=1):
    """
    Function to plot a histogram for the eigenvector statistics and also plots the theory lines on top.

    Parameters
    ----------
    data : List | Array
        Data for the histogram
    dimension : int
        dimension for the theory lines
    ax : axes
        axes object to plot in
    bins : List | Array | int
        bins for the histogram, it can be an array of the bin positions or number of bins. same as plt.hist(bins)
    stepPlot : bool, optional
        If True, plots the theory lines in steps at bin positions, by default True
    legend : bool, optional
        If True, creates a legend for the theory lines, by default False
    theoryLines : bool, optional
        If True, plots the theory lines, by default True
    density : bool, optional
        If True, normalises the histogram, by default True
    htype : str, optional
        type/style of the histogram, by default 'bar'. See plt.hist for more.
    color : str, optional
        color of the histogram, by default None
    labels : list, optional
        labels for the x and y axes, by default [r'COE ($\beta = 1$)', r'CUE ($\beta = 2$)', r'CSE ($\beta = 4$)']

    Returns
    -------
    axes
        returns the given axes object back
    """
    hist = ax.hist(data, bins=bins, density=density, histtype=htype, color=color, alpha=alpha)
    if not isinstance(bins, str):
        bins = hist[1]
    else:
        bins = np.linspace(0, 1, 2000)
    binMeans = [(bins[i+1] + bins[i])/2 for i in range(len(bins)-1)]
    colors = colorCycle(3, 'viridis_r')

    if theoryLines:
        COE = [EigenVectorDist(X, int(dimension), 1) for X in binMeans]
        CUE = [EigenVectorDist(X, int(dimension), 2) for X in binMeans]
        CSE = [EigenVectorDist(X, int(dimension), 4) for X in binMeans]

        if stepPlot:
            # ax.step(binMeans, COE, linestyle='--', color='lime', label=labels[0], linewidth=1)
            # ax.step(binMeans, CUE, linestyle='-.', color=colors[1], label=labels[1], linewidth=1)
            # ax.step(binMeans, CSE, linestyle=(0, (1, 1)), color=colors[2], label=labels[2], linewidth=1)
            ax.step(binMeans, COE, linestyle='--', color='k', label=labels[0], linewidth=linewidth)
            ax.step(binMeans, CUE, linestyle=(0, (3, 1, 1, 1)), color='k', label=labels[1], linewidth=linewidth)
            ax.step(binMeans, CSE, linestyle=(0, (1, 1)), color='k', label=labels[2], linewidth=linewidth)
        else:
            # ax.plot(binMeans, COE, linestyle='--', color='lime', label=labels[0], linewidth=1)
            # ax.plot(binMeans, CUE, linestyle='-.', color=colors[1], label=labels[1], linewidth=1)
            # ax.plot(binMeans, CSE, linestyle=(0, (1, 1)), color=colors[2], label=labels[2], linewidth=1)
            ax.plot(binMeans, COE, linestyle='--', color='k', label=labels[0], linewidth=linewidth)
            ax.plot(binMeans, CUE, linestyle=(0, (3, 1, 1, 1)), color='k', label=labels[1], linewidth=linewidth)
            ax.plot(binMeans, CSE, linestyle=(0, (1, 1)), color='k', label=labels[2], linewidth=linewidth)

    if legend:
        ax.legend(loc='upper right', prop={'size': 8})

    return ax


def plotEigValStat(data, ax, bins, legend=False, theoryLines=True, density=True, htype='bar',#pylint:disable=too-many-arguments, dangerous-default-value
                   labels=[r'COE', r'CUE', r'CSE'], color=None, linewidth=1):
    """
    Function to plot a histogram for the eigenvalue statistics and also plots the theory lines on top.

    Parameters
    ----------
    data : List | Array
        Data for the histogram
    ax : axes
        axes object to plot in
    bins : List | Array | int
        bins for the histogram, it can be an array of the bin positions or number of bins. same as plt.hist(bins)
    legend : bool, optional
        If True, creates a legend for the theory lines, by default False
    theoryLines : bool, optional
        If True, plots the theory lines, by default True
    density : bool, optional
        If True, normalises the histogram, by default True
    htype : str, optional
        type/style of the histogram, by default 'bar'. See plt.hist for more.
    color : str, optional
        color of the histogram, by default None

    Returns
    -------
    axes
        returns the given axes object back
    """
    xvals = np.arange(0, 5, 0.01)
    ax.hist(data, bins=bins, density=density, histtype=htype, color=color)
    colors = colorCycle(3, 'viridis_r')
    if theoryLines:
        ax.plot(xvals, [WignerSurmise(x, 0) for x in xvals], linestyle='-', color='k', linewidth=linewidth, label=r'$e^{-s}$')
        ax.plot(xvals, [WignerSurmise(x, 1) for x in xvals], linestyle='--', color='k', linewidth=linewidth, label=labels[0])
        ax.plot(xvals, [WignerSurmise(x, 2) for x in xvals], linestyle=(0, (3, 1, 1, 1)), color='k', linewidth=linewidth,
                label=labels[1])
        ax.plot(xvals, [WignerSurmise(x, 4) for x in xvals], linestyle=(0, (1, 1)), color='k', linewidth=linewidth,
                label=labels[2])

    if legend:
        ax.legend(loc='upper right', fontsize='x-large')

    return ax
