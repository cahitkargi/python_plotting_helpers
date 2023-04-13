import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import matplotlib as mpl
from .figCreate import cm2inch

def setLimits(axGrids, xlims = None, ylims = None):
    """
    Sets x and y limits for a list/array of axes.
    Nothing special, just uses set_xlim/set_ylim in a loop.

    Parameters
    ----------
    axGrids : List | Array
        a list/array of axes objects
    xlims : float | int, optional
        x axes limit, by default None
    ylims : float | int, optional
        y axes limit, by default None
    """
    if isinstance(xlims, (list, tuple)):
        for ax in axGrids:
            ax.set_xlim([xlims[0], xlims[1]])

    if isinstance(ylims, (list, tuple)):
        for ax in axGrids:
            ax.set_ylim([ylims[0], ylims[1]])

def setTicks(axGrids, xTicks=None, yTicks=None):
    """
    Sets x and y ticks for a list/array of axes.
    Nothing special, just uses set_xticks/set_yticks in a loop.

    Parameters
    ----------
    axGrids : List | Array
        a list/array of axes objects
    xTicks : List, optional
        a list of x ticks, by default None
    yTicks : List, optional
        a list of y ticks, by default None
    """
    if isinstance(xTicks, (list, tuple)):
        for ax in axGrids:
            ax.set_xticks(xTicks)

    if isinstance(yTicks, (list, tuple)):
        for ax in axGrids:
            ax.set_yticks(yTicks)

def omitTicklabels(axList, rows, columns, xt=True, yt=True, ticks=True): # pylint:disable=too-many-arguments
    """
    Omits the ticks and/or tick-labels of shared axes in a grid.

    Parameters
    ----------
    axGrids : List | Array
        a list/array of axes objects
    rows : int
        number of rows in the grid
    columns : int
        number of columns in the grid
    xt : bool, optional
        If False, does nothing to x ticks or tick-labels, by default True
    yt : bool, optional
        If False, does nothing to y ticks or tick-labels, by default True
    ticklabels : bool, optional
        If True, omits only the tick-labels and keeps the ticks, by default False
    """
    for ind, ax in enumerate(axList):
        if xt:
            if ind < (columns*(rows-1)):
                if ticks:
                    ax.set_xticklabels([])
                else:
                    ax.set_xticks([])

        if yt:
            if ind%columns != 0:
                if ticks:
                    ax.set_yticklabels([])
                else:
                    ax.set_yticks([])

def axTickSettings(ax, yonly=False, left=True, right=False, bottom=True, top=False, labelbottom=True,labeltop=False, # pylint:disable=too-many-arguments
                   labelleft=True, labelright=False, minorCount=None, fontsize=10, lineWidth=1.2, lineLength=4):
    """
    Apply certain settings to a given axes object.

    Parameters
    ----------
    ax : axes
        axes object to apply the settings
    yonly : bool, optional
        If True does not apply the settings to x-axes, by default False
    left : bool, optional
        If True, shows the y-ticks on the left, by default True
    right : bool, optional
        If True, shows the y-ticks on the right, by default False
    bottom : bool, optional
        If True, shows the x-ticks on the bottom, by default True
    top : bool, optional
        If True, shows the x-ticks on the top, by default False
    labelbottom : bool, optional
        If True, shows the x-tick-labels on the bottom, by default True
    labeltop : bool, optional
        If True, shows the x-ticks on the top, by default False
    labelright : bool, optional
        If True, shows the y-tick-labels on the right, by default False
    minorCount : int, optional
        number of minor ticks, by default None
    """
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator(minorCount))
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator(minorCount))

    ax.tick_params(axis='both', direction='in', bottom=bottom, top=top, left=left, right=right, labelleft=labelleft,
                   labelbottom=labelbottom, labelright=labelright, labeltop=labeltop, which='both', labelsize=fontsize)

    ax.tick_params(length=lineLength, width=lineWidth)
    ax.tick_params(length=int(lineLength/2), width=lineWidth, which='minor')

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(lineWidth)

    if not yonly:
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

def createLegend(ax, *args, **kwargs):
    """
    Creates a legend for the given axes and pplies certain settings to the legend.
    You can use any kwargs for legend settings to overwrite the default values or modify futher.

    Parameters
    ----------
    ax : axes
        axes object
    """
    defaultKwargs = {
        'title':'',
        'loc':'upper left',
        'handlelength':1,
        'handletextpad':0.25,
        'columnspacing':0.5,
        'labelcolor':'linecolor',
        'ncol':3,
        'handleheight':1,
        'labelspacing':0.2,
        'prop':dict(size=8)
    }
    leg = ax.legend(*args, **kwargs, **{k:v for k, v in defaultKwargs.items() if k not in kwargs})
    for line in leg.get_lines():
        line.set_linewidth(1)
    return leg

def rcSettings():
    """
    Upon calling, this function changes some of the default matplotlib configurations.
    """
    mpl.rcParams["font.family"] = "serif"
    plt.rcParams["axes.axisbelow"] = False
    mpl.rcParams["font.serif"] = "STIX"
    mpl.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams.update({'font.size': 10,'legend.frameon': False,'legend.title_fontsize':10})
    mpl.rcParams['text.usetex'] = True
    mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
    plt.rcParams["figure.figsize"] = cm2inch(8.5, 8)
    plt.rcParams['figure.dpi'] = 200

def _setLogSub(ax, axFunc, axStr):
    getattr(ax, axFunc)('log')
    locmaj = mpl.ticker.LogLocator(base=10,numticks=12) 
    getattr(ax, axStr).set_major_locator(locmaj)
    locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),numticks=12)
    getattr(ax, axStr).set_minor_locator(locmin)
    getattr(ax, axStr).set_minor_formatter(mpl.ticker.NullFormatter())

def setLogScale(ax, xLog=False, yLog=False):
    if xLog:
        _setLogSub(ax, 'set_xscale', 'xaxis')

    if yLog:
        _setLogSub(ax, 'set_yscale', 'yaxis')
