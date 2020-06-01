#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import re
import seaborn as sns
import os
import sys
import pathlib

def vBarPlot(df, xCol, barCols, yLabel, graphTitle, save=True, **kwargs):
    r""" It represents a vertical appilated bar graph with legend,
    and a table at the bottom
    
    Parameters
    ----------
    df : pandas dataframe
         Dataframe with the data to represent.
         
    xCol : string
         df column name to represent in the x axis.
         
    barCols : list of strings
         df columns names to represent in the y axis as bars.
         
    yLabel : string
         Label for the y axis.
         
    graphTitle : string
         Title of the graph. 
         Will be used as a filename if fileName is not provided.
         
    save : boolean, optional
        If True, the figure is saved into a file.
        
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    legendLoc : string, optional, default "best". 
         Legend location, accepts standart legend locations 
         for matplotlib, plus "out top right","out center right", 
         "out lower right" for placing the legend out of 
         the plotting area and "none" for hidding the legend.
         
    yLim : float, optional 
         Limit of the y axis in y data units.
         
    tableCols : list of strings, optional, default False, 
         List of df cols headers to use as rows 
         in the table under the plot. 
         If not provided, the table will not be generated
         
    tableEdge : string, optional, default "open", 
         Border style for the table 
         valid values are: 'open', 'closed', 'horizontal', 'vertical'
         
    width : float, optional
         Width of the bars between 0 and 1.
         
    xSize : float, optional default 10
         Width of the figure in inches.
         
    ySize :  float, optional, default 6
         Height in inches.
         
    fontScale : float, optional, default 1.2 
         Global scale factor for the font size.
         
    yTicksNum : float, optional
         Number of ticks in the y axis.
         
    orderBy : string, optional
         `df` column header name to use 
         to order x axis in ascending order.
         
    hLines : list of lists, optional
        Used to display horizontal lines, 
        each list containing a 3 elements, one list for each line:
            - first, the y cordinate for the horizontal line
            
            - second, the color for the horizontal line
            
            - third, linestyle to use for the line
            
            - fourth, label of the line, to use in the legend (optional)
            
    palette : seaborn compatible palette, 
         Can be the name of a seaborn palette, 
         a seaborn palette or a list 
         interpretable as a palette by seaborn.
         
    fileName : string, optional
         File name to save, if not provided graphTitle will be used. 
         Non alphanumeric values will be deleted.
       
    Examples
    --------
    >>> data = {"AC": ["SXXX","SYYY","SZZZ","SAAA","SBBB","SBB1","SBB2","SBB3"],
    ...         "type": ["S1","S2","S2","S1","S1","S2","S2","S1"],
    ...         "bar1": [1750,1700,1800,1500,1860,1900,1720,1650],
    ...         "bar2": [1750,1700,1800,1500,1860,1900,1720,1650],
    ...         "bar3": [600,500,650,550,520,495,605,675],
    ...         "label1": ["Loc 1","Loc 2","TL","Loc 4","TL","TL","TL","TL"],
    ...         "label2": ["Loc 1","Loc 2","TL","Loc 4","TL","TL","TL","TL"]}
    >>> df_test = pd.DataFrame.from_dict(data)
    >>> vBarPlot(df=df_test,
    ...          xCol="AC",
    ...          barCols=["bar1", "bar3"],
    ...          yLabel="var units",
    ...          graphTitle="vertical Bar Plot Example",
    ...          legendLoc="out center right",
    ...          yLim= 2500, 
    ...          tableCols=["type", "label1"],
    ...          tableEdge="open", 
    ...          width=False, 
    ...          xSize=10,  
    ...          ySize=6, 
    ...          fontScale=1.3, 
    ...          yTicksNum=6,
    ...          orderBy="bar1",
    ...          hLines=[[1200, "red","-"], [2000, "g","--" ,"Green line"]]
    ...          )
         
    """
    
    "Version 1.0"
    
    #copy the dataframe to avoid modifying it
    df = df.reset_index().copy()
    
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
    
    legendLoc = kwargs.get("legendLoc", "best")
    yLim = kwargs.get("yLim", False)
    tableCols = kwargs.get("tableCols", False)
    tableEdge = kwargs.get("tableEdge", "open")
    width = kwargs.get("width", False)
    xSize = kwargs.get("xSize", 10)
    ySize = kwargs.get("ySize", 6)
    fontScale = kwargs.get("fontScale", 1.2)
    yTicksNum = kwargs.get("yTicksNum", False)
    orderBy = kwargs.get("orderBy", False)
    hLines = kwargs.get("hLines", False)
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphTitle)
    
    #########################Params Validation#########################
    #Check for type match and particularities in every param 
    #not needed in python but helps comunicating errors to the user
    if not isinstance(df, pd.DataFrame):
        raise functionError("df is not a pandas dataframe")
    
    if not xCol in df.columns.values.tolist():
        raise functionError("xCol is not a df column header name.")
    
    if isinstance(barCols, (list, tuple)):
        for item in barCols:
            if not item in df.columns.values.tolist():
                raise functionError(
                        "barCols item "
                        "{} is not a df column header name.".format(item))
            
    elif isinstance(barCols, (str, int)):
        barCols = [barCols,] 

    if not isinstance(yLabel, str):
        try:
            yLabel = str(yLabel)
        except:
            raise functionError("yLabel is not a string.")

    if not isinstance(graphTitle, str):
        try:
            graphTitle = str(graphTitle)
        except:
            raise functionError("graphTitle is not a string.")
            
            
    #possible legendLoc values.
    posLeyeLocValues=['best', 0, 'upper right', 1, 'upper left', 2, 
                      'lower left', 3, 'lower right', 4,'right', 5,
                      'center left', 6, 'center right', 7, 'lower center', 8,
                      'upper center', 9, 'center', 10, "none", "out top right",
                      "out center right", "out lower right"]
    if legendLoc:        
        if not legendLoc in posLeyeLocValues:
            raise functionError("legendLoc is not a valid value.")
    
    if yLim:
        if not isinstance(yLim, (int, float)):
            raise functionError("yLim is not an integer or a float")
    
    if tableCols:
        if isinstance(tableCols, (list, tuple)):
            for item in tableCols:
                if not item in df.columns.values.tolist():
                    raise functionError(
                            "tableCols item"
                            " {} is not a df column header name.".format(item))
                
        elif isinstance(tableCols, (str, int)):
            tableCols = [tableCols,] 
    
    if not tableEdge in ['open', 'closed', 'horizontal', 'vertical']:
        raise functionError(
                "tableEdge is not a valid value" 
                " valid values are: 'open', "
                "'closed', 'horizontal', 'vertical'")
    
    if width:
        if not isinstance(width, (int, float)):
            raise functionError("width is not a float or a integer.")
    
    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")
    
    if not isinstance(fontScale, (int, float)):
        raise functionError("fontScale is not a float or a integer.")
    
    if yTicksNum:
        if not isinstance(yTicksNum, int):
            raise functionError("yTicksNum is not a integer.")
    
    if orderBy:
        if not orderBy in df.columns.values.tolist():
            raise functionError("orderBy is not a df column header name.")
    
    ##############Initial calculations and settings####################
    sns.set(style="whitegrid", font_scale=fontScale)
    sns.set_palette(palette)
    
    if orderBy:
        df.sort_values(by=[orderBy], inplace=True) 
    
    x = np.arange(len(df[xCol]))  # the label locations
    
    #to avoid bars overlapping we check if the width is too big
    if width:
        if width > (1/len(barCols)) :
            width = 1/len(barCols)
            print("Width too big for correct display"
                  ", reduced to {0:.2f}".format(width))
    else:
        width = 1/(len(barCols) + 1)
    
    ############figure creation########################################
    fig, ax = plt.subplots(figsize=(xSize, ySize))

    for barCount, bar in enumerate(barCols):
    # Plot each column separated, placing the bar displaced to fit all.
        ax.bar(x - (len(barCols)*width)/2 + (barCount + 0.5)*width, 
               df[bar], width, label=str(bar))
    
    ax.set_ylabel(yLabel)
    ax.set_title(graphTitle)
    ax.set_xticks(x)
    ax.set_xticklabels(df[xCol])
    
    if yLim:
        ax.set(ylim=(0, yLim))
        
    if yTicksNum:
        ax.set_yticks(
                [float(x)*(yLim/yTicksNum) 
                for x in range(yTicksNum + 1)])

    
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
    
    ############################Table Creation#########################
    cell_text = []
    if tableCols:
        for row in tableCols:
            cell_text.append(
            [ "{:g}".format(float('{:.3g}'.format(x))) 
            if isinstance(x, float) else str(x) for x in df[row]]) 
        
        theTable = plt.table(cellText=cell_text,
                             cellLoc="center", 
                             rowLoc="right",
                             colLabels=df[xCol], 
                             edges="open", 
                             rowLabels=tableCols)
        ax.get_xaxis().set_ticks([])
        
        # Reescaling of the table to give vertical padding 
        # and keep cells in the center of the xticks
        theTable.scale(0.95, 1.4*fontScale)
        
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

if __name__ == '__main__':
    pass