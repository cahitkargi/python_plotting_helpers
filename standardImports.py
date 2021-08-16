#from helpers.readCSV import readCSV
from quanguru import readCSV, saveCSV

from Plotting.linePlots import pltAveg
from Plotting.plotSettings import axTickSettings, createLegend
from Plotting.colorPlots import irregColorPlot, ColorPlot
from Plotting.colorFuncs import rainbowCycle, createMAP, normalizeCMAP
from helpers.Plotting.figCreate import createFigAndAx, grid, cm2inch
from helpers.Plotting.EigVecStatPlot import plotEigStat, plotEigValStat

from helpers import onLOL as lol

#from helpers.rmtDistributions import EigenVectorDist, WignerDyson, WignerSurmise, Poissonian
from quanguru import EigenVectorDist, WignerDyson, WignerSurmise, Poissonian

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset, inset_axes
import matplotlib.colors as mpc
#mpl.font_manager._rebuild()
mpl.rcParams["font.family"] = "serif"
plt.rcParams["axes.axisbelow"] = False
mpl.rcParams["font.serif"] = "STIX"
mpl.rcParams["mathtext.fontset"] = "stix"
plt.rcParams.update({'font.size': 10,'legend.frameon': False,'legend.title_fontsize':8})
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

# root where the simulation data is stored
root = '/Volumes/mkquantum/Users/PhD_Students/KargiCahit/'
