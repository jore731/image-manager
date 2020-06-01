#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
import seaborn as sns
import sys
import pathlib
import re
import os


def metricEvolutionGraph(data, graphTitle, save=True, **kwargs):
    r"""Represents a metric evolution graph to show the progress of 
    multiple elements colored by a label value. 
    Elements don't need to have the same number of points.
    Can represent one line (design reference line) 
    and a horizontal line (clearance line).
    
    Parameters
    ----------
    data : list of list, 
        list of lists, each list containing 3 elements, 
        list with the x, y, and label. For example 
        [[[x1, x2, x3], [y1, y2, y3], label1], 
        [[x1, x2, x3], [y1, y2, y3], label2], ...] 
        Label values will be used to choose a color for the lines.
    
    graphTitle : string
        Title of the graph, will be used as filename 
        if fileName kwarg is not provided
    
    save : boolean, optional
        If True, the figure is saved into a file.
    
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    fontScale : float, optional, default 1.
        Global scalation factor for every text of the figure.
        
    legendLoc : string, optional, default "best".
        Legend location, accepts standart legend locations 
        for matplotlib, plus "out top right", "out center right", 
        "out lower right" for placing the legend out of 
        the plotting area and "none" for hidding the legend.
        
    xSize : float, optional, default 12
        Horizontal size of the figure, in inches.
        
    ySize : float, optional, default 8
        Vertical size of the figure, in inches.
        
    gridMinor : boolean, optional, default True.
        If True, minor grid is displayed.
        
    xLabel : string, optional.
        Label for the x axis.
        
    yLabel : string, optional.
        Label for the y axis.
        
    xLim : float, optional.
        Right limit of the x axis in x data units.
        
    yLim : float, optional
        Top limit of the y axis in y data units.
        
    designLine : boolean, default False.
        If True, the design reference line is represented.
        
    designSlope : float, optional, default 1
        Slope for the design line.
        
    designIntercept : float, optional,default 0.
        Intercept for the design line.
        
    designColor : string, optional, default black.
        Named color or hex code for the design reference line.
        
    designLabel : string, optional
        Label of the design reference line, it will 
        be displayed in the legend.
        
    clearanceLine : boolean, optional, default False
        If True, the clearance line is represented.
        
    clearancey : float, optional, default 0
        Location in y units for the horizontal line
        
    clearanceColor : string, optional, default r
        Named color or hex code for the clearance horizontal line.
        
    clearanceLabel : string, optional
        Label of the clearance line, it will 
        be displayed in the legend.
        
    palette : seaborn compatible palette, optional
         Can be the name of a seaborn palette, 
         a seaborn palette or a list interpretable 
         as a palette by seaborn.
         
    colorDict : dictionaries label: color, optional
         Dict with label:color to use to color the progression lines,
         if not provided, the palette will be used.
         
    fileName : string, optional.
        If not provided graphTitle will be used. 
        Non alphanumeric values will be deleted.
        
    markerShape : string, optional, default "o"
        Shape of the marker. Check matplotlib.markers for the possible values.
        
    markerFill : string, optional, default "w"
        Color to fill the marker, named color or hex code, 
        use "none" for empty circles and
        None to fill the circles with the color of the edges.
        
    markerSize : float, optional, default 5
        Size of the markers.
        
    markerEdgeWidth : float, optional,  default 2
        Linewidth ot the edges of the markers.
        
    Examples
    --------
    >>> dataIn = [[[750, 1100, 1200, 1300], [1100, 1250, 1350, 1650], "type 1"],
    ...           [[500, 1100, 1200], [750, 1150, 1250], "type 1"],
    ...           [[750, 1100, 1200, 1300], [250, 1050, 1150, 1250], "type 1"],
    ...           [[1100, 1200, 1300], [950, 1050, 1150], "type 2"],
    ...           [[1100, 1200], [850, 950], "type 1"]]
    >>> metricEvolutionGraph(dataIn, "metric Evolution Graph Example",
    ...                      gridMinor=True, legendLoc="out top right",
    ...                      xSize=12, ySize=7,
    ...                      xLabel="x label", yLabel="y label",
    ...                      xLim=2000, yLim=2000,
    ...                      designLine=True, designSlope=1,
    ...                      designIntercept=0, designColor="k",
    ...                      designLabel="Design", clearanceLine=True,
    ...                      clearancey=1800,  clearanceColor="r",
    ...                      clearanceLabel="Clearance",
    ...                      markerSize=5, markerFill="w",
    ...                      markerShape="o",
    ...                      colorDict={"type 1": "green", "type 2": "blue"},
    ...                      palette="deep")
        
    """
    
    """Version 1.0"""
    
    class functionError(Exception):
        """Custom error class defined to differentiate our errors
        from the standard errors"""
        
        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None
    
        def __str__(self):
            print('calling str')
            if self.message:
                return 'functionError, {0} '.format(self.message)
            else:
                return 'functionError, undefined function error'
    
    
    ################################Kwargs#############################
    fontScale = kwargs.get("fontScale", 1.3)
    legendLoc = kwargs.get("legendLoc", "best")
    xSize = kwargs.get("xSize", 12)
    ySize = kwargs.get("ySize", 8)
    gridMinor = kwargs.get("gridMinor", True)
    xLabel = kwargs.get("xLabel", False)
    yLabel = kwargs.get("yLabel", False)
    xLim = kwargs.get("xLim", False)
    yLim = kwargs.get("yLim", False)
    
    markerShape = kwargs.get("markerShape", 'o')
    markerFill = kwargs.get("markerFill", 'w')
    markerSize = kwargs.get("markerSize", 5)
    markerEdgeWidth = kwargs.get("markerEdgeWidth", 2)
    
    designLine = kwargs.get("designLine", False)
    if designLine:
        designSlope = kwargs.get("designSlope", 1)
        designIntercept = kwargs.get("designIntercept", 0)
        designColor = kwargs.get("designColor", "k")
        designLabel = kwargs.get("designLabel", None)
    
    clearanceLine = kwargs.get("clearanceLine", False)
    if clearanceLine:
        clearancey = kwargs.get("clearancey", 0)
        clearanceColor = kwargs.get("clearanceColor", "r")
        clearanceLabel = kwargs.get("clearanceLabel", None)
    
    palette = kwargs.get("palette", "deep")
    colorDict = kwargs.get("colorDict", False)
    filename = kwargs.get("fileName", graphTitle)
    

    ################### input validation ##############################
    if not isinstance(data, list):
        raise functionError("Data is not a list")
        
    if not isinstance(graphTitle, str):
        try:
            graphTitle = str(graphTitle)
        except:
            raise functionError("graphTitle is not a string.")
            
    if not isinstance(fontScale, (int, float)):
        raise functionError("fontScale is not a number")
    elif fontScale < 0:
        raise functionError("fontScale is negative. "
                         "Only positive values are allowed")
        

    #possible legendLoc values.
    posLeyeLocValues=['best', 0, 'upper right', 1, 'upper left', 2, 
                      'lower left', 3, 'lower right', 4,'right', 5,
                      'center left', 6, 'center right', 7, 'lower center', 8,
                      'upper center', 9, 'center', 10, "none", "out top right",
                      "out center right", "out lower right"] 
    if legendLoc:        
        if not legendLoc in posLeyeLocValues:
            raise functionError("legendLoc is not a valid value.")
    
    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")
    
    if not isinstance(gridMinor,bool):
        raise functionError("gridMinor is not a boolean")
    
    if xLabel:
        if not isinstance(xLabel, str):
            try:
                xLabel = str(xLabel)
            except:
                raise functionError("xLabel is not a string.")
    
    if yLabel:
        if not isinstance(yLabel, str):
            try:
                yLabel = str(yLabel)
            except:
                raise functionError("yLabel is not a string.")
    
    if xLim:
        if not isinstance(xLim, (int, float)):
            raise functionError("xLim is not an integer or a float")

    if yLim:
        if not isinstance(yLim, (int, float)):
            raise functionError("yLim is not an integer or a float")
            
    if isinstance(designLine,bool):
        if designLine is True:
            if not isinstance(designSlope, (int, float)):
                raise functionError("designSlope is "
                                 "not an integer or a float")
            if not isinstance(designIntercept, (int, float)):
                raise functionError("designIntercept is "
                                 "not an integer or a float")            
    else:
        raise functionError("designLine is not a boolean")
        
    if isinstance(clearanceLine,bool):
        if clearanceLine is True:
            if not isinstance(clearancey, (int, float)):
                raise functionError("clearancey is "
                                 "not an integer or a float")        
    else:
        raise functionError("clearanceLine is not a boolean")
    
    if xLabel:
        if not isinstance(xLabel, str):
            try:
                xLabel = str(xLabel)
            except:
                raise functionError("xLabel is not a string.")
    
    if yLabel:
        if not isinstance(yLabel, str):
            try:
                yLabel = str(yLabel)
            except:
                raise functionError("yLabel is not a string.")
    
    if not isinstance(markerSize, (int, float)):
        raise functionError("markerSize is not an integer or a float")
    
    if not isinstance(markerEdgeWidth, (int, float)):
        raise functionError("markerEdgeWidth is not an integer or a float")
    
    ####################initial settings and calculations##############
    sns.set(font_scale=fontScale)
    sns.set_style("whitegrid", 
                  {'xtick.bottom': True, 
                   'xtick.top': True, 
                   'xtick.direction': 'in',
                   'ytick.left': True,
                   'ytick.right': True,
                   'ytick.direction': 'in',
                   'axes.edgecolor': '.15',
                   'grid.linestyle': '-'}
                  )
    
    #set palette and then get palette as a hex list
    #we need to do this to assign colors to our palette.
    sns.set_palette(palette)
    palette = list(sns.color_palette().as_hex())
    
    #Create dict with the diferent labels and the color associated.
    if colorDict is False:
        colorDict = {}
        dataInLabel = []
        for AC in data:
            if not AC[2] in dataInLabel:
                dataInLabel.append(AC[2])
                colorDict.update({AC[2]: palette[len(colorDict)]})
    
    ### Figure creation ###############################################
    fig, ax = plt.subplots(figsize=(xSize, ySize))
    
    ax.set_title(graphTitle, fontsize="large")
    
    markerStyle = dict(marker=markerShape, 
                       mfc=markerFill, 
                       markersize=markerSize, 
                       markeredgewidth=markerEdgeWidth)
    
    for AC in data:
        ax.plot(AC[0], AC[1], color=colorDict[AC[2]], 
                linestyle='dashed', **markerStyle)
    
    #Clearance line
    if clearanceLine:
        ax.axhline(y=clearancey, color=clearanceColor, 
                   linewidth= 2, label=clearanceLabel, linestyle='dashed')
    
    if xLim:
        ax.set_xlim(left=0, right=xLim)
    else:
        ax.set_xlim(left=0)
        
    if yLim:
        ax.set_ylim(bottom=0, top=yLim)
    else:
        ax.set_ylim(bottom=0)
        
    if xLabel:
        ax.set_xlabel(xLabel)
    if yLabel:
        ax.set_ylabel(yLabel)
    
    #Design line
    if designLine:
        xRange = ax.get_xlim()
        ax.plot(xRange,[x*designSlope + designIntercept for x in xRange],
                scalex=False, scaley=False, color=designColor,
                linestyle='dashed', label=designLabel)
    
    #Grid minor addition
    if gridMinor:
        ax.get_xaxis().set_minor_locator(ticker.AutoMinorLocator())
        ax.get_yaxis().set_minor_locator(ticker.AutoMinorLocator())
        ax.grid(b=True, which='minor', color='.8', linewidth=1, 
                linestyle='--', alpha=0.5)
    
    #######Legend creation#############################################
    
    #extend the legend to include the colors of the lines
    handles = ax.get_legend_handles_labels()[0]
    extraLegElement=[]
    for label, color in colorDict.items():
        extraLegElement.append(Patch(color=color, label=label))
    handles = handles + extraLegElement
    
    #list with the standart valid matplotlib legend values
    stdLeyeLocList = ['best', 0, 'upper right', 1, 'upper left', 2, 
                      'lower left', 3, 'lower right', 4, 'right', 5, 
                      'center left', 6, 'center right', 7, 'lower center', 8,
                      'upper center', 9, 'center', 10]
    
    # put legend as usual if is a standart name, 
    # nothing if "none", custom if others 
    if legendLoc in stdLeyeLocList:
        ax.legend(handles=handles, loc=legendLoc)
    
    elif legendLoc == "out top right":
        ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))
    
    elif legendLoc == "out center right":
        ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
        
    elif legendLoc == "out lower right":
        ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(1, 0))
    
    elif legendLoc == "none":
        pass
    
    ##########################Figure Saving############################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path = os.path.split(fullpath)[0] #caller file path and name
        
        # To create the file name, remove non alphanumeric chars
        name = re.sub(r'\W+', '', filename.title())
        
        plt.savefig(pathlib.Path(path,name).with_suffix(".png"),
                    bbox_inches='tight',dpi=600)
    
    plt.show()
    
    return fig

if __name__ == "__main__":
    pass