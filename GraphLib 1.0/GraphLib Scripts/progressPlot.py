#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns
import os
import sys
import pathlib
import matplotlib.ticker as ticker


def progressPlot(df, xCol, yCols, graphTitle, save=True, **kwargs):
    r"""Plot progression lines from the data of a dataframe. 
    To represent multiple columns as dependant variables 
    and one column as independant variable. 
    Allows to cumulate values, represent horizontal lines and
    a design reference line.
    
    Parameters
    ----------
    df : pandas dataframe
         Datafrane with the data to represent.
         
    xCol : string
         df column name to represent in the x axis.
         
    yCols : list of strings
         df columns names to represent in the x axis.

    graphTitle : string
        Title of the graph.
        If no fileName is provided, it is used to name the file.
        
    save : boolean, optional
        If True, the figure is saved into a file.
        
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    cumulative : boolean, optional, default False
         If True cumulate the input dataframe.
         
    xLabel : string, optional
         Label for the y axis.
         
    yLabel : string, optional
         Label for the y axis.
         
    legendLoc : string, optional, default "best"
         Legend location, accepts standart legend locations 
         for matplotlib, plus "out top right","out center right", 
         "out lower right" for placing the legend out of 
         the plotting area and "none" for hidding the legend.
         
    yLim : float, optional
         Limit of the y axis in y data units.
         
    xLim : float, optional
         Limit of the x axis in x data units.
         
    xSize : float, optional default 10
          Width of the figure in inches.
         
    ySize :  float, optional, default 6
         Height in inches.
         
    fontScale : float, optional, default 1.2
         Scale factor for the font size.
         
    xTicksNum : float, optinal
         Number of ticks in the x axis.
         
    yTicksNum : float, optional,
         Number of ticks in the y axis.
         
    hLines : list of lists, optional
        Used to display horizontal lines, one list for each line.
        Each list containing a 3 or 4 elements list for each line:
            - first, the y cordinate for the horizontal line, 
            - second, the color for the horizontal line, 
            - third, linestyle for the line, i.e. "-", "--", "-.-"
            - fourth, label value to display in the legend (optional)
     
    gridMinor : boolean, optional, default True
         If True, minor grid is displayed.
         
    designLine : boolean, optional, default False
         If True, the design reference line is represented.
         
    designSlope : float, optional, default 1
         Slope for the design line.
         
    designIntercept : float, optional, default 0
        Intercept for the design line.
         
    designColor : string, optional, default "k", 
        named color or hex code for the 
        design reference line.
        
    designLabel : string, optional
         Label for the design reference line, 
         it will be displayed in the legend.
         
    markerShape : string, optional, default "o"
         Shape of the marker. 
         Check matplotlib.markers for the possible values.
         
    markerFill : string, optional, default "w", 
        color to fill the marker, 
        named color or hex code, use "none" for transparent circles and
        None to fill the circles with the color of the edges.
        
    markerSize : float, optional, default 5
        Size of the markers.
         
    markerEdgeWidth : float, optional, default 2
         linewidth ot the edges of the markers.
         
    palette : seaborn compatible palette, 
         Can be the name of a seaborn palette, 
         a seaborn palette or a list 
         interpretable as a palette by seaborn.
    
    fileName : string, optional
         If not provided graphTitle will be used. 
         Non alphanumeric values will be deleted.
         
        
    Examples
    --------
    >>> df_test = pd.DataFrame.from_dict(
    ...                 {"var0":[1.2, 1.1, 1.3, 1, 1.2, 1.1, 1.2, 1.3],
    ...                  "var1":[0.175,0.17,0.18,0.17,0.186,0.19,0.172,0.165],
    ...                  "var2":[0.13,0.12,0.13,0.1225,0.126,0.139,0.13,0.12],
    ...                  "var3":[0.1600, 0.1500, 0.1650, 0.1550, 
    ...                              0.1520, 0.1495, 0.1605, 0.1675]})
    >>> progressPlot(
    ...            df=df_test,
    ...            xCol="var0",
    ...            yCols=["var1", "var2", "var3"],
    ...            graphTitle="Test",
    ...            yLabel="Test y",
    ...            xLabel="Test x",
    ...            legendLoc ="out top right",
    ...            cumulative=True,
    ...            yLim=1.6,
    ...            xLim=10,
    ...            xTicksNum=10,
    ...            yTicksNum=8,
    ...            hLines=[[1.4, "black", "-", "Clearance"], 
    ...                    [1.1, "r", "--", "Clearance2"]],
    ...            xSize=11,
    ...            ySize=6,
    ...            gridMinor=True,
    ...            designLine=True,
    ...            designSlope=0.2,
    ...            designColor="b",
    ...            designLabel="Design"
    ...            )
    """
    
    """Version 1.0"""
    
    #we create a copy to avoid  modifying the original data
    df = df.copy()
    
    class functionError(Exception):
        """Custom error class defined to differentiate our errors
        from the standard errors"""
        
        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None
    
        def __str__(self):
            if self.message:
                return 'functionError, {0} '.format(self.message)
            else:
                return 'functionError, undefined function error'
    
    
    #########################kwargs####################################
    cumulative = kwargs.get("cumulative", False)
    xLabel = kwargs.get("xLabel", False)
    yLabel = kwargs.get("yLabel", False)
    legendLoc = kwargs.get("legendLoc", "best")
    yLim = kwargs.get("yLim", False)
    xLim = kwargs.get("xLim", False)
    xSize = kwargs.get("xSize", 10)
    ySize = kwargs.get("ySize", 6)
    fontScale = kwargs.get("fontScale", 1.2)
    yTicksNum = kwargs.get("yTicksNum", False)
    xTicksNum = kwargs.get("xTicksNum", False)
    hLines = kwargs.get("hLines", False)
    gridMinor = kwargs.get("gridMinor", True)
    
    designLine = kwargs.get("designLine", False)
    if designLine:
        designSlope = kwargs.get("designSlope", 1)
        designIntercept = kwargs.get("designIntercept", 0)
        designColor = kwargs.get("designColor", "k")
        designLabel = kwargs.get("designLabel", None)

    markerShape = kwargs.get("markerShape", 'o')
    markerFill = kwargs.get("markerFill", None)
    markerSize = kwargs.get("markerSize", 5)
    markerEdgeWidth = kwargs.get("markerEdgeWidth", 2)
    
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphTitle)
    
    #########################Params Validation#########################
    #Check for type match and particularities in every param 
    if not isinstance(df, pd.DataFrame):
        raise functionError("df is not a pandas dataframe")
    
    if not xCol in df.columns.values.tolist():
        raise functionError("xCol is not a df column header name.")
    
    for col in yCols:
        if not col in df.columns.values.tolist():
            raise functionError("{} is not a df column header name.".format(col))

    if not isinstance(graphTitle, str):
        try:
            graphTitle = str(graphTitle)
        except:
            raise functionError("graphTitle is not a string.")
            
    if not isinstance(cumulative, bool):
        raise functionError("cumulative is not a boolean")
    
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
    
    #possible legendLoc values.
    posLeyeLocValues=['best', 0, 'upper right', 1, 'upper left', 2, 
                      'lower left', 3, 'lower right', 4,'right', 5,
                      'center left', 6, 'center right', 7, 'lower center', 8,
                      'upper center', 9, 'center', 10, "none", "out top right",
                      "out center right", "out lower right"]
    if legendLoc:        
        if not legendLoc in posLeyeLocValues:
            raise functionError("legendLoc is not a valid value.")
    
    if xLim:
        if not isinstance(xLim, (int, float)):
            raise functionError("xLim is not an integer or a float")

    if yLim:
        if not isinstance(yLim, (int, float)):
            raise functionError("yLim is not an integer or a float")

    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")
    
    if not isinstance(fontScale, (int, float)):
        raise functionError("fontScale is not a float or a integer.")
    
    if xTicksNum:
        if not isinstance(xTicksNum, int):
            raise functionError("xTicksNum is not a integer.")

    if yTicksNum:
        if not isinstance(yTicksNum, int):
            raise functionError("yTicksNum is not a integer.")
    
    if not isinstance(gridMinor, bool):
        raise functionError("gridMinor is not a boolean")

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
            
    if not isinstance(markerSize, (int, float)):
        raise functionError("markerSize is not an integer or a float")
    
    if not isinstance(markerEdgeWidth, (int, float)):
        raise functionError("markerEdgeWidth is not an integer or a float")
        
    ##############Initial calculations and settings####################
    sns.set(style="whitegrid",  font_scale=fontScale)
    sns.set_palette(palette)
    
    if cumulative:
        df = df.cumsum()
        
    markerStyle = dict(marker=markerShape, 
                       mfc=markerFill, 
                       markersize=markerSize, 
                       markeredgewidth=markerEdgeWidth)
    
    ############figure creation########################################
    fig, ax = plt.subplots(figsize=(xSize, ySize))

    for varCount, var in enumerate(yCols):
    # Plot each yCols separated
        ax.plot(df[xCol], df[var], label=var, **markerStyle)
    
    if yLabel:
        ax.set_ylabel(yLabel)
        
    if xLabel:
        ax.set_xlabel(xLabel)
    
    ax.set_title(graphTitle, fontsize="large")
    
    if yLim:
        ax.set(ylim=(0, yLim))
    if xLim:
        ax.set(xlim=(0, xLim))
        
    if yTicksNum:
        ax.set_yticks(
                [float(x)*(yLim/yTicksNum) 
                for x in range(yTicksNum + 1)])
    if xTicksNum:
        ax.set_xticks(
                [float(x)*(xLim/xTicksNum) 
                for x in range(xTicksNum + 1)])

    #horizontal lines creation
    if hLines:
        for line in hLines:
            try:
                #Put a label if provided 
                if len(line) == 3 :
                    ax.axhline(y=line[0], color=line[1], linewidth= 2,
                               linestyle=line[2])
                else :
                    ax.axhline(y=line[0], color=line[1], linewidth= 2, 
                               linestyle=line[2], label=line[3])
            except:
                raise functionError("Wrong argument in hLines")
    
    #Design line
    if designLine:
        xRange = ax.get_xlim()
        ax.plot(xRange, [x*designSlope + designIntercept for x in xRange],
                scalex=False, scaley=False, color=designColor,
                linestyle='dashed', label=designLabel)
    
    #Grid minor addition
    if gridMinor:
        ax.get_xaxis().set_minor_locator(ticker.AutoMinorLocator())
        ax.get_yaxis().set_minor_locator(ticker.AutoMinorLocator())
        ax.grid(b=True, which='minor', color='.8', linewidth=1, 
                linestyle='--', alpha=0.5)
    
    
    #######Legend creation#############################################
    #list with the standart valid matplotlib legend values
    stdLeyeLocList = ['best', 0, 'upper right', 1, 'upper left', 2, 
                      'lower left', 3, 'lower right', 4, 'right', 5, 
                      'center left', 6, 'center right', 7, 'lower center', 8,
                      'upper center', 9, 'center', 10]
    
    # put legend as usual if is a standart name, 
    # nothing if "none", custom if others 
    if legendLoc in stdLeyeLocList:
        ax.legend(loc=legendLoc)
    
    elif legendLoc == "out top right":
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    elif legendLoc == "out center right":
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
    elif legendLoc == "out lower right":
        ax.legend(loc='lower left', bbox_to_anchor=(1, 0))
    
    elif legendLoc == "none":
        pass
    
        
    ############Plot saving############################################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfilename = os.path.split(fullpath) 
        
        # To create the file name, remove non alphanumeric chars
        filename = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path, filename).with_suffix(".png"),
                            bbox_inches='tight', dpi=600)
    plt.show()
    
    return fig

if __name__ == '__main__':
    pass
