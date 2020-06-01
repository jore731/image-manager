# -*- coding: utf-8 -*-
"""
@author: U64053

"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt

from math import ceil
import re
import seaborn as sns
import os
import sys

def boxPlotter(df, graphTitle, boxCols, save=True, **kwargs):
    r"""Represents a box plot from the data of a dataframe.

    Parameters
    ----------
    df : pandas DataFrame
        dataframe containing the data to plot.
        
    graphTitle : string
        title of the plot, used as fileName if not provided.
        
    boxCols : list of strings
        Columns of df to plot in the boxplots.
    
    save : boolean, optional
        If True, the figure is saved into a file.
        
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    tickLabels : list of strings, optional
        Labels for the box plot, must have the same lenght as boxCols. 
        If not provided, boxCols is used.
        
    colors : list of strings, optional
        Colors to color the boxplos, must have the same lenght as boxCols. 
        If not provided the default palette is used.
        
    xLabel : string, optional
        Label for the x axis.
        
    yLabel : string, optional
        Label for the y axis.
        
    showMeans : boolean, optional, default is True
        Show mean marker.
        
    showFliers : boolean, optional, default is True
        Show fliers markers.
        
    notch : boolean, optional, default False
        Activate notched boxes.
        
    xSize : float, optional, default is 10.
        X dimension of the figure in inches.
        
    ySize : float, optional, default is 6.
        Y dimension of the figure in inches.
        
    yLim : list of floats (min, max), optional
        It is used to set y axis limits. 
        
    cappkw : dict, optional, {"color": "k"}
        Specifies the style of the caps. 
        
    boxeskw : dict, optional, default is {"color":"k"}
        Specifies the style of the box. 
        
    whiskerskw : dict, optional, default is {"color":"k"}
        Specifies the style of the whiskers. 
        
    flierskw : dict, optional
        Specifies the style of the fliers. 
        The default is {"marker":'.', "markeredgecolor":"k"}.
        
    medianskw : dict, optional, default {"color":"k"}
        Specifies the style of the median. 
        
    meankw : dict, optional
        Specifies the style of the mean. 
        The default is {"marker":"o", 
        "markerfacecolor":"lightgrey", 
        "markeredgecolor":"k", "markersize":"5"}.
        
    palette : seaborn compatible palette, default "deep"
         Can be the name of a seaborn palette, 
         a seaborn palette or a list 
         interpretable as a palette by seaborn.
         
    fileName : string, optional
         File name to save, if not provided graphTitle will be used. 
         Non alphanumeric values will be deleted.
    
    Examples
    --------
    >>> data = {"loc" + str(x): np.random.normal(5, 1, 80) for x in range(1, 17)}
    >>> data["AC"] = ["AC0" + str(ac) for ac in range(1, 81)]
    >>> df = pd.DataFrame(data)
    >>> boxPlotter(df, "test title", 
    ...           ["loc1", "loc2", "loc3", "loc4", "loc5"], 
    ...           yLabel="y label test", 
    ...           xLabel="x label test",
    ...           tickLabels=["first", 2, 3, 4, 5],
    ...           flierskw = {"marker":'.', "markeredgecolor":"red"},
    ...           palette = "muted")
    """

    """Version 1.0"""
    
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
            print('calling str')
            if self.message:
                return 'functionError, {0} '.format(self.message)
            else:
                return 'functionError, undefined function error'

    ##########kwargs###################
    whis = kwargs.get("whis", 1.5)
    tickLabels = kwargs.get("tickLabels", None)
    colors = kwargs.get("colors", None)
    xLabel = kwargs.get("xLabel", None)
    yLabel = kwargs.get("yLabel", None)
    showMeans = kwargs.get("showMeans", None)
    showFliers = kwargs.get("showFliers", True)
    notch = kwargs.get("notch", False)
    xSize = kwargs.get("xSize", 10)
    ySize = kwargs.get("ySize", 6)
    yLim = kwargs.get("yLim", None)
    fileName = kwargs.get("fileName", None)
    palette = kwargs.get("palette", "deep")
    cappkw = kwargs.get("cappkw", {"color": "k"})
    boxeskw = kwargs.get("boxeskw", {"color":"k"})
    whiskerskw = kwargs.get("whiskerskw", {"color":"k"})
    flierskw = kwargs.get("flierskw", {"marker":'.', "markeredgecolor":"k"})
    medianskw = kwargs.get("medianskw", {"color":"k"})
    meankw = kwargs.get("meankw", {"marker":"o", "markerfacecolor":"lightgrey", 
                                   "markeredgecolor":"k", "markersize":"5"})
    
    ######################Input validation#############################
    #input validation is not necesary in python
    #but it is performed here to easily error handeling.
    if not isinstance(df, pd.DataFrame):
        raise functionError("df is not a pandas dataframe")
        
    if not isinstance(graphTitle, str):
        try:
            graphTitle = str(graphTitle)
        except:
            raise functionError("graphTitle is not a string.")
    
    if not isinstance(boxCols, (list, tuple)):
        boxCols = [boxCols, ]
    for col in boxCols:
        if not col in df.columns.values.tolist():
            raise functionError("{} is not a df column header name.".format(col))
            
    if not isinstance(save, bool):
        raise functionError("save is not a boolean")
    
    if not len(tickLabels) == len(boxCols):
        raise functionError("tickLabels length is not correct")
        
    if not len(colors) == len(boxCols):
        raise functionError("colors length is not correct") 

    if not isinstance(xLabel, str):
        try:
            xLabel = str(xLabel)
        except:
            raise functionError("xLabel is not a string.")
            
    if not isinstance(yLabel, str):
        try:
            yLabel = str(yLabel)
        except:
            raise functionError("yLabel is not a string.")
            
    for boolean in (showMeans, showFliers, notch):
        if not isinstance(boolean, bool):
            raise functionError("{} is not a boolean".format(boolean))
            
    for size in (xSize, ySize):
        if not isinstance(size, (float, int)):
            raise functionError("{} is not a float")

    if not isinstance(fileName, str):
        try:
            fileName = str(fileName)
        except:
            raise functionError("fileName is not a string.")
            
    #######initial settings ###########################################
    if fileName is None:
        fileName = graphTitle
     
    #Figure and bloxplot creation
    sns.set_style("whitegrid", {'axes.edgecolor': '0.3'})
    
    sns.set_palette(palette)
    
    if tickLabels is None:
        tickLabels = boxCols
        
    if colors is None:
        n = ceil(len(boxCols)/10)
        colors = (sns.color_palette()*n)[:len(boxCols)]
        
    data = [list(df[col]) for col in boxCols]
    
    fig, ax = plt.subplots(figsize=(xSize, ySize), dpi=150)
    
    bplot = ax.boxplot(data, 
                        notch=notch, 
                        vert=True, 
                        whis=whis, 
                        patch_artist=True,
                        capprops=cappkw,
                        boxprops=boxeskw,
                        whiskerprops=whiskerskw,
                        flierprops=flierskw,
                        medianprops=medianskw,
                        meanprops=meankw, 
                        labels=tickLabels,
                        showmeans=showMeans,
                        showfliers=showFliers,
                        )
    
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        
    #Axis style
    ax.grid(axis='x')
    ax.set_title(graphTitle)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    if yLim:
        ax.set_ylim(yLim[0], yLim[1])
     
    ############Plot saving############################################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfilename = os.path.split(fullpath) 
        
        # To create the file name, remove non alphanumeric chars
        filename = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,filename).with_suffix(".png"),
                            bbox_inches='tight',dpi=600)
    plt.show()

    return fig

if __name__ == "__main__":
    pass