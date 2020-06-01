#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
import pandas as pd
import pathlib
import re
import os
import sys

def scatterHist(df, xCol, yCol, graphTitle, save=True, **kwargs):
    r"""Represents a center scatter plot of the kind "hex", "scatter" or "kde",
    and a top and right (border) histogram plots.
    
    Parameters
    -------------
    df : pandas dataframe
         Dataframe with the data to represent.
         
    xCol : string
         df column name to represent in the x axis.
        
    yCol : string
         df column name to represent in the y axis.

    graphTitle : string
        title of the graph and filename for saving.
        
    save : boolean, optional
        If True, the figure is saved into a file.
        
    Returns
    -------
    
    fig : seaborn JoinGrid object.
        object that stores the generated graph.
        
    Other parameters
    ----------------
    
    cKind : string, {"hex", "kde", "scatter"}, optional, default "scatter"
        Kind of plot to use for the center plot. 
        The options are "hex" for a hexagonal grid plot, 
        "kde" for a kernel density estimate plot (or level surfaces) 
        and "scatter" for the typical scatter plot.
    
    xLabel : string, optional
        Label for the x axis. If not provided xCol is used.
        
    yLabel : string, optional
        Label for the y axis. If not provided yCol is used.
        
    size : float, optional, default 7
        Size of the figure in inches.
    
    centerPropor : float, optional, default 5
        Relative size of the center to the margins.
        
    plotSeparation : float, optional, default 0.1
        Separation between the border plots and the center plot.
        
    cColor : string, optional
        hex value or named color to use in the center plot.
        
    cKdeFill : boolean, optional, default True
        If true it fills the center plot kde surfaces, 
        if False, draw only the borders. Only if cKind is "kde"
    
    cHexGrid : integer, optional, default 20.
        Number of hexagonal grids along a axis for the center plot.
        Only if cKind is "hex".
        
    cHexGridColor : string, optional, default "w"
        hex value or named color to use in the center plot 
        for the hex grid borders. Only if cKind is "hex"
        
    bColor : string, optional
        hex value or named color to use in the border plots.
        
    bBins : integer, optional, default 20
        Number of bins (columns) of the border plots.
        
    bRug : boolean, optional, default True
        It switches on and off the rug representation in the border plot.
        
    bKde : boolean, optional, default True
        It switches on and off the kde line representation in the border plots.
        
    bHist : boolean, optional, default True
         It switches on and off the histogram representation in the border plots.       
        
    palette : seaborn compatible palette, optional
         Can be the name of a seaborn palette, 
         a seaborn palette or a list interpretable 
         as a palette by seaborn.
         
    fileName : string, optional
         If not provided graphTitle will be used. 
         Non alphanumeric values will be deleted.
         
    Examples
    --------
    
    >>> rs = np.random.RandomState()
    >>> x = rs.normal(size=200)
    >>> y = rs.normal(size=200)
    >>> df =pd.DataFrame({"X_coord": x, "Y_coord": y})
    >>> scatterHist(df, xCol="X_coord", yCol="Y_coord", 
    ...             graphTitle="Test Title", save=True,
    ...             cKind="hex", fileName="scatt Hist Test",
    ...             xLabel="x label", yLabel="y label")
    
    """
    
    "Version 1.0"
    
    ############kwargs###############################
    xLabel = kwargs.get("xLabel", xCol)
    yLabel = kwargs.get("yLabel", yCol)
    size = kwargs.get("size", 7)
    centerPropor = kwargs.get("centerPropor", 5)
    plotSeparation = kwargs.get("plotSeparation", 0)
    cKind = kwargs.get("cKind", "scatter")
    cColor = kwargs.get("cColor", None)
    cKdeFill = kwargs.get("cKdeFill", True)
    cHexGrid = kwargs.get("cHexGrid", 20)
    cHexGridColor = kwargs.get("cHexGridColor", "w")
    bColor = kwargs.get("bColor", None) 
    bBins = kwargs.get("bBins", 20) 
    bRug = kwargs.get("bRug", True) 
    bKde = kwargs.get("bKde", True) 
    bHist = kwargs.get("bHist", True) 
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphTitle)
    
    ############initial settings#######################
    
    df = df.copy()

    sns.set_palette(palette)
    
    sns.set(style="ticks")
    
    # Make a colormap based off the plot color
    if cColor is None:
        cColor = sns.color_palette()[0]

    color_rgb = mplcolors.colorConverter.to_rgb(cColor)
    colors = [sns.utils.set_hls_values(color_rgb, l=l)  
              for l in np.linspace(1, 0.05, 12)]
    
    ccmap = sns.blend_palette(colors, as_cmap=True)
    
    if bColor is None:
        bColor = cColor
    
    if cKind == "kde":
        cplot = sns.kdeplot
        ckwargs = {"cmap":ccmap, "n_levels": 20, "shade":cKdeFill}
        
    elif cKind == "scatter":
        cplot = sns.scatterplot
        ckwargs = {"color": cColor}
        
    elif cKind == "hex":
        cplot = plt.hexbin
        ckwargs = {"cmap":ccmap, "color":cHexGridColor, "gridsize":cHexGrid}
        
    fig = sns.JointGrid(x=xCol, y=yCol, 
                      data=df, height=size, 
                      ratio=centerPropor, 
                      space=plotSeparation)
    
    fig.plot_joint(cplot, **ckwargs)
    
    fig.plot_marginals(sns.distplot, color=bColor,
                                 bins=bBins, rug=bRug, kde=bKde, hist=bHist)
    fig.fig.suptitle(graphTitle, 
                   fontsize="x-large", ha="center", va='bottom', 
                   x=0.5)
    
    fig.set_axis_labels(xLabel, yLabel)
    
    ############Plot saving############################################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfilename = os.path.split(fullpath) 
        
        # To create the file name, remove non alphanumeric chars
        filename = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,filename).with_suffix(".png"),
                            bbox_inches='tight',dpi=600)

    plt.plot()
    
    return fig


    
    


