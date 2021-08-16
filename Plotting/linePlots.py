def pltAveg(ax1, datax, datay, ranges=[0, 1], linewidth=1): #pylint:disable=dangerous-default-value
    """
    Plots a line into an axes by creating a y-axes on the right-hand side of the given axes (i.e. uses twinx).
    I use this mainly for plotting the averages of the colorplots on top of them, and the y-ax values for that case are
    the (say time) averages colormap.

    Parameters
    ----------
    ax1 : axes
        axes to plot in
    datax : List | Array
        x axis data
    datay : List | Array
        y axis data
    ranges : list, optional
        limits of the y axes for the average, by default [0, 1].
    linewidth : int, optional
        line width, by default 1

    Returns
    -------
    axes
        returns back the given ax object
    """
    ax = ax1.twinx()
    #ax.scatter(datax, datay, color='k', s=1)
    ax.plot(datax, datay, color='k', linewidth=linewidth, linestyle="-")
    ax.set_ylim([ranges[0], ranges[1]])
    ax.set_yticks([ranges[0], (ranges[0]+ranges[1])/2, ranges[1]])
    ax.set_yticklabels([ranges[0], (ranges[0]+ranges[1])/2, ranges[1]], rotation=0)
    return ax
