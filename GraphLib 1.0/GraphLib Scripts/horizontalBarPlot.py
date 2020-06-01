# -*- coding: utf-8 -*-
"""

@author: u64053
"""
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import re
import seaborn as sns
from matplotlib.path import Path
import os
import sys
import pathlib

def hBarPlot(df, yCol, xCols, xLabel, graphTitle, save=True, **kwargs):
    r"""Represents a horizontal bar graph with vertical lines, 
    anotations and text under the graph.
    
    Parameters
    ----------
    df : pandas dataframe
         Dataframe with the data to represent.
         
    yCol : string
         df column name to represent in the y axis.
         
    xCols : string or list of strings
         df column or column names 
         to represent in the x axis. If multiple columns are used,
         stacked bars will be used.
         
    xLabel : string 
         label for the x axis.
         
    graphTitle : string
         Title of the graph, will be used as file name if not provided.
    
    save : boolean, optional
        If True, the figure is saved into a file.
    
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    colorCol : string, optional, default False
         df col to use as label to choose color. 
         If False all bars are colored equally.
         
    colorDict : list of dictionaries, default False
         List with as many elements as xCols
         with dicts with colorCol label:color to use to color the bars.
         Example: [{"S1": "g", "S2": "r"}, {"S1": "b","S2": "orange"}]
         
    xLim : float, optional, default False
         Limit of the x axis in x data units.
         
    nLim : integer, optional, default False.
         Limit of the number of elemnents of yCol 
         displayed in the y axis.
         
    ascending : boolean, optional, default False.
         False for higher values, True of lower values.
         
    vLabels : list of lists
         List of lists with annotations parameters in the format:
         [[x1, y1, text1, color1, style1] , 
         [x2, y2, text2, color2, style2] , ...]
             - x : float, x in data units where the vertical line is.
             - y : integer, y bar position to place the annotation.
             - text : string, text to display in the annotation.
             - color : string, rgb color for the line and annotation.
             - style : string, ("regular", "highlighted", "dashed", "regularD").
     
    yLabel : string, optional.
         Label for the y axis.
         
    xSize : float, optional, default 12
         Width of the figure in inches.
         
    ySize : float, optional, default 9 
         Height in inches.
         
    fontScale : float, optional, default 1
         Factor scale for the text.
         
    xTicksNum : integer, optional.
         Number of x axis ticks.
         
    palette : seaborn compatible palette, optional
         Can be the name of a seaborn palette, 
         a seaborn palette or a list interpretable 
         as a palette by seaborn.
         
    fileName : string, optional
         If not provided graphTitle will be used. 
         Non alphanumeric values will be deleted.
         
    orderCol : string, optional, default false.
         Column to use to order the df. 
         If false use the first element of xCols
         
    yElems : list of strings, optional
         List with the elements of the ycol you wish to represent.
         If not provided, all elements are represented. 
         It is not recomended to use it with the kw nLim.
         
    subText : string, optional.
         If not False, add text to the bottom of the graph.
   
    Examples
    --------
    >>> data={"AC":["STXXX", "STYYY", "SSZZZ", "SSAAA", 
    ...             "SSBBB", "SSBB1", "SSBB2", "SSBB3"],
    ...       "Type": ["S2", "S2", "S1", "S1", "S1", "S1", "S1", "S1"],
    ...       "FH":[500, 700, 1000, 1200, 860, 1300, 1100, 1350],
    ...       "FH Period":[50, 70, 100, 120, 86, 130, 110, 135]}
    >>> df = pd.DataFrame.from_dict(data)
    >>> v_labels=[[1200, 0, 'adf5646asdf2213', "b", "regular"],
    ...           [1600, 2, 'asd5456', "#6B8E23", "highlighted"],
    ...           [2400, 3, 'ads5456', "b", "dashed"]]
    >>> keywords=dict(xLim=6000,
    ...               vLabels=v_labels,
    ...               yLabel="label y",
    ...               colorCol="Type",
    ...               xSize=10,
    ...               ySize=7,
    ...               colorDict=[{"S1":"g", "S2":"r"}, 
    ...                          {"S1":"b","S2":"orange"}],
    ...               fontScale=1.2,
    ...               xTicksNum=4,
    ...               patette="deep")
    >>> hBarPlot(df, "AC", ["FH", "FH Period"], 
    ...          "FH [h]", "FH leaders", **keywords)
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
    
    #we create a copy to avoid modifying the original database
    df = df.copy() 
    
    ################################kwargs#############################
    xLim = kwargs.get("xLim", False)
    nLim = kwargs.get("nLim", False)
    vLabels = kwargs.get("vLabels", False)
    yLabel = kwargs.get("yLabel", False)
    xSize = kwargs.get("xSize", 12)
    ySize = kwargs.get("ySize", 9)
    fontScale = kwargs.get("fontScale", 1.2)
    xTicksNum = kwargs.get("xTicksNum", False)
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphTitle)
    ascending = kwargs.get("ascending", False)
    colorCol = kwargs.get("colorCol", False)
    colorDict = kwargs.get("colorDict", False)
    orderCol = kwargs.get("orderCol", False)
    yElems = kwargs.get("yElems", False)
    subText = kwargs.get("subText", False)
    
    #######################Params Validation###########################
    #Check for type match and particularities in every param 
    #input validation is not necesary in python
    #but it is performed here to enhance error handeling.
    
    if not isinstance(df, pd.DataFrame):
        raise functionError("df is not a pandas dataframe")
        
    if isinstance(xCols, (list, tuple)):
        for item in xCols:
            if not item in df.columns.values.tolist():
                raise functionError(
                        "xCols item "
                        "{} is not a df column header name.".format(item))
    elif isinstance(xCols, (str, int)):
        xCols = [xCols,]

    if not isinstance(xLabel, str):
        try:
            xLabel = str(xLabel)
        except:
            raise functionError("xLabel is not a string.")
            
    if not isinstance(graphTitle, str):
        try:
            graphTitle = str(graphTitle)
        except:
            raise functionError("graphTitle is not a string.")

    if xLim:
        if not isinstance(xLim, (int, float)):
            raise functionError("xLim is not an integer or a float")
    
    if nLim:
        if not isinstance(nLim, int):
            raise functionError("nLim is not an integer or a float")

    if not isinstance(ascending, bool):
        raise functionError("ascending is not boolean")
        
    if yLabel:
        if not isinstance(yLabel, str):
            try:
                yLabel = str(yLabel)
            except:
                raise functionError("yLabel is not a string.")
    
    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")
    
    if not isinstance(fontScale, (int, float)):
        raise functionError("fontScale is not a number")

    elif fontScale < 0:
        raise functionError("fontScale is negative. "
                            "Only positive values are allowed")
    
    #if only a dict is provided instead of a one item list
    if colorDict:
        if isinstance(colorDict, dict):
            colorDict = [colorDict,]
    if subText:
        if not isinstance(subText, str):
            raise functionError("subText is not an string.")
        
    #########Initial settings and calculations#########################
    sns.set(style="whitegrid", font_scale=fontScale)
    sns.set_palette(palette)
    
    #we represent bars from top to bottom in descending longitude
    if orderCol:
        df.sort_values(by=[orderCol], inplace=True, ascending=ascending)
    else:
        df.sort_values(by=[xCols[0]], inplace=True, ascending=ascending)
        
    if yElems:
        df = df.query(yCol+" in @yElems").reset_index()
    if nLim:
        df = df.head(nLim)
    
    #positions for the bars
    yPos = np.arange(len(df[yCol]))[::-1]
    
    #Definition of the text box arrow path, to use in the annotations
    def arrowBoxStyle(x0, y0, width, height, mutation_size, 
                         mutation_aspect=1):
        """
        Given the location and size of the box, return the path of
        the box around it.
         - *x0*, *y0*, *width*, *height* : location and size of the box
         - *mutation_size* : a reference scale for the mutation.
         - *aspect_ratio* : aspect-ration for the mutation.
        """
        # padding
        mypad = 0.5
        pad = mutation_size * mypad
    
        # width and height with padding added.
        width = width + 2 * pad
        height = height + 2 * pad
    
        # boundary of the padded box
        x0, y0 = x0 - pad, y0 - pad
        x1, y1 = x0 + width, y0 + height
    
        cp = [(x0, y0), (x1, y0), (x1, y1), (x0, y1),
              (x0-pad, (y0+y1)/2.), (x0, y0), (x0, y0)]
    
        com = [Path.MOVETO,
               Path.LINETO, Path.LINETO, Path.LINETO,
               Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    
        path = Path(cp, com)
    
        return path
    
    
    #################Figure creation###################################
    fig, ax = plt.subplots(figsize=(xSize, ySize))
    
    barlist =[]
    for xColCount, xCol in enumerate(xCols):
        #first column is added with no left reference
        if xColCount == 0:
            barlist.append(ax.barh(yPos, df[xCol], align='center'))
            leftRefer = list(df[xCol])
        #the rest use the previous sum as reference.
        else:
            barlist.append(ax.barh(yPos, 
                                   df[xCol], 
                                   left=leftRefer,
                                   align='center'))
            #sum this column to the left reference
            leftRefer = [sum(x) for x in zip(leftRefer, list(df[xCol]))]
            
    ax.set_yticks(yPos)
    ax.set_yticklabels(df[yCol])
    ax.set_title(graphTitle, fontsize="large")
    ax.set(xlabel=xLabel)
    
    #bar coloring
    colorNum=0
    if colorCol:
        #Create colorDict if not provided
        if colorDict is False:
            colorDict = []
            #asign as many colors of the palett to each 
            #unique value as xcols
            for count in range(len(xCols)):
                colorDict.append({})
                for label in list(df[colorCol].unique()):
                    
                    colorDict[count][label] = list(
                            sns.color_palette().as_hex())[colorNum]
                    colorNum += 1
        
        #Apply color to the cols
        for barsCount, bars in enumerate(barlist):
            for bar, label in zip(bars, df[colorCol]):
                bar.set_color(colorDict[barsCount][label])
    
    if xLim:
        ax.set_xlim(0, xLim)
        
    if yLabel:
        ax.set(ylabel=yLabel)

    #Vertical lines and annotations representation
    labCounter = 0 #used in error messages
    textExtraArtists = [] #list of the extra artist
    if vLabels:
        try :
            #add vertical lines
            for lab in vLabels:
                if lab[4] == "regular":
                    ax.axvline(x=lab[0], color=lab[3], linewidth=2)
                    
                if lab[4] == "regularD":
                    ax.axvline(x=lab[0], color=lab[3], linewidth=2, 
                               linestyle='dashed')
                    
                elif lab[4] == "highlighted":
                    ax.axvline(x=lab[0], color=lab[3], linewidth= 2)
                    
                elif lab[4] == "dashed": 
                    ax.axvline(x=lab[0], color="red", 
                               linestyle='dashed', linewidth= 2)
            
            #just in case the xLim changes with the labels
            xLimDim = ax.get_xlim()[1]  
            
            #label plotting
            for lab in vLabels:
                if xLim:
                    if xLim < lab[0]:
                        continue
                labCounter += 1
                if lab[4] == "regular" or lab[4] == "regularD":
                    textExtraArtists.append(
                            ax.text(lab[0] + (0.22/xSize)*xLimDim*fontScale, 
                            lab[1], lab[2], va= "center",
                            bbox=dict(boxstyle=arrowBoxStyle,
                                      facecolor=lab[3], alpha=1)))
                
                elif lab[4] == "highlighted": #regular with red contour
                    textExtraArtists.append(
                            ax.text(lab[0] + (0.22/xSize)*xLimDim*fontScale, 
                                    lab[1], lab[2], va= "center",
                                    bbox=dict(boxstyle=arrowBoxStyle,
                                              facecolor=lab[3],
                                              edgecolor='red',
                                              linewidth= 2, alpha=1)))
                
                #regular with red dashed line and red dashed contour
                elif lab[4] == "dashed":                    
                    textExtraArtists.append(
                            ax.text(lab[0] + (0.22/xSize)*xLimDim*fontScale,
                                    lab[1], lab[2], va= "center",
                                    bbox=dict(boxstyle=arrowBoxStyle,
                                              facecolor=lab[3],
                                              edgecolor='red',linewidth= 2,
                                              linestyle='dashed', alpha=1)))
                else: #if style is not a valid number
                    raise functionError
                    
        except functionError:
            raise functionError("Invalidad vLabels style argument in "
                             "annotation number {} ".format(labCounter) +
                             '"regular","highlighted","dashed, "regularD"" ' 
                             'are the valid values.')
        except:
            raise functionError(
                    "Invalid or missing param in v_lines "
                    "Invalid or missing param in annotation number {}"
                    .format(labCounter))
    
    #set x ticks
    xLim = ax.get_xlim()[1]
    if xTicksNum:
        try:
            ax.set_xticks(
                    [float(x)*(xLim/xTicksNum) 
                    for x in range(xTicksNum + 1)])
        except:
            raise functionError("xTicksNum is not an integer")
    
    if subText:
        textExtraArtists.append(ax.text(0, 0, subText, ha='left',
                                        va='top', transform=fig.transFigure))
            
    ############Plot saving############################################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfilename = os.path.split(fullpath)
        
        # To create the file name, remove non alphanumeric chars
        filename = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,filename).with_suffix(".png"),
                            bbox_extra_artists=textExtraArtists, 
                            bbox_inches='tight', dpi=300)
    plt.show()
    
    return fig


if __name__ == "__main__":
    pass
    

    