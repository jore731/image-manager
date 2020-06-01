# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pathlib
import re
import seaborn as sns
import os
import sys

def stackedbars(dflist, repreCols, groupCol, graphTitle, save=True, **kwargs):
    r"""Function to represent stacked bar graph normaliced to 100%. 
    Data from multiple datasets with the same columns.
    A column will be used to aggregate the rows in multiple groups.
    
    Parameters
    ----------
    
    dflist : list of pandas DataFrames
        list of dataframes containing the data, must all have the same columns.
        
    repreCols : list of strings
        list of string with the dataframe columns to represent.
        
    groupCol : string
        column of the dataframe to use
        
    graphTitle : string
        title of the graph and filename for saving.
        
    save : boolean, optional
        If True, the figure is saved into a file.
        
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    
    yLabel : string, optional.
        label for the y axis.
        
    yTicksNum : integer, optional
        Number of ticks in the y axis.
        
    width : float, optional.
        width betwwen 0 and 1 of the bars.
        
    colorDict : dict, optional.
        dictionary with label:color being labels, 
        groupCol column elements.
        
    legendLoc : string, optional, default "best"
         Legend location, accepts standart legend locations 
         for matplotlib, plus "out top right","out center right", 
         "out lower right" for placing the legend out of 
         the plotting area and "none" for hidding the legend.
        
    inverse_order : boolean, optional.
        inverse the order of the bars.
        
    xSize : float, optional.
        x size of the figure in inches.
        
    ySize : float, optional.
        y size of the figure in inches.
        
    palette : seaborn compatible palette, 
         Can be the name of a seaborn palette, 
         a seaborn palette or a list 
         interpretable as a palette by seaborn.
         
    fileName : string, optional
         File name to save, if not provided graphHeader will be used. 
         Non alphanumeric values will be deleted.
        
    Examples
    --------
    >>> df_test1 = pd.DataFrame.from_dict(
    ...             {"type":["S1", "S2", "S1", "S2", "S1", "S1", "S1", "S1"],
    ...              "var0":[1.2, 1.1, 1.3, 1, 1.2, 1.1, 1.2, 1.3],
    ...              "var1":[4, 5, 8, 3, 5, 2, 7, 3],
    ...              "var2":[0.13, 0.12, 0.13,0.12, 0.12, 0.13, 0.13, 0.12],
    ...              "var3":[0.16, 0.15, 0.16, 0.15, 0.15, 0.14, 0.16, 0.16]})
    >>> df_test2 = pd.DataFrame.from_dict(
    ...             {"type":["S1new", "S2new", "S1new", "S2new", 
    ...                      "S1new", "S1new", "S1new", "S1new"],
    ...              "var0":[2.2, 1.1, 1.3, 2, 1.2, 2.1, 1.2, 2.3],
    ...              "var1":[4, 5, 6, 3, 5, 6, 7, 6],
    ...              "var2":[0.13, 0.16, 0.63,0.12, 0.12, 0.6, 0.13, 0.6],
    ...              "var3":[1.16, 0.16, 0.16, 0.15, 0.15, 1.14, 0.16, 0.16]}) 
    >>> dflist = [df_test1, df_test2]
    >>> stackedbars(dflist, 
    ...             repreCols=['var0', 'var1', 'var2', 'var3'], 
    ...             groupCol="type", 
    ...             graphTitle="metric by type", 
    ...             save = True,
    ...             normalize=True, 
    ...             yLabel= "Test label y", 
    ...             colorDict = {"S1":"darkgreen", "S1new": "green", 
    ...                          "S2":"darkblue", "S2new": "blue"}, 
    ...             inverse_order=False,
    ...             legendLoc="out top right",
    ...             fileName="stacked Bars Example")
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
            if self.message:
                return 'functionError, {0} '.format(self.message)
            else:
                return 'functionError, undefined function error'

    ############kwargs#######################
    
    normalize = kwargs.get("normalize", True)
    yLabel = kwargs.get("yLabel", None)
    yTicksNum = kwargs.get("yTicksNum", 5)
    width = kwargs.get("width", None)
    colorDict = kwargs.get("colorDict", None)
    legendLoc = kwargs.get("legendLoc", "best")
    inverse_order = kwargs.get("inverse_order", True)
    xSize = kwargs.get("xSize", 6)
    ySize = kwargs.get("ySize", 4)
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphTitle)

    #########################Params Validation#########################
    #Check for type match and particularities in every param 
    #not needed in python but helps comunicating errors to the user
    for df in dflist:
        if not isinstance(df, pd.DataFrame):
            raise functionError("an element of dflist is"
                                " not a pandas dataframe")

    for dfCount, df in enumerate(dflist):
        for col in repreCols:
            if not col in df.columns.values.tolist():
                raise functionError(
                        "repreCols item "
                        "{} is not a dflist[{}]"
                        " column header name.".format(col, dfCount))
                
        if not groupCol in df.columns.values.tolist():
            raise functionError("groupCol is not a dflist[{}]"
                                " column header name".format(dfCount))
        
    if not isinstance(save, bool):
        raise functionError("save is not a boolean")
    
    if not yLabel is None:
        if not isinstance(yLabel, str):
            raise functionError("yLabel is not a string")
        
    if not isinstance(yTicksNum, int):
        raise functionError("yTicksNum is not an integer")
     
    if not width is None:
        if not isinstance(width, (float, int)):
            raise functionError("width is not a float")
        
    #possible legendLoc values.
    posLeyeLocValues=['best', 0, 'upper right', 1, 'upper left', 2, 
                      'lower left', 3, 'lower right', 4,'right', 5,
                      'center left', 6, 'center right', 7, 'lower center', 8,
                      'upper center', 9, 'center', 10, "none", "out top right",
                      "out center right", "out lower right"]
    if legendLoc:        
        if not legendLoc in posLeyeLocValues:
            raise functionError("legendLoc is not a valid value.")
            
    if not isinstance(inverse_order, bool):
        raise functionError("inverse_order is not a boolean")
        
    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")
        
    if not isinstance(fileName, str):
        try:
            fileName = str(fileName)
        except:
            raise functionError("fileName is not a string.")
            
    ################initial settings###############
    
    sns.set_palette(palette)
    
    cols = repreCols + [groupCol,]
    
    if isinstance(dflist, pd.DataFrame):
        dflist = [dflist, ]
    
    if width is None:
        width = 1/(len(dflist) + 1)
    
    #group by groupCol values
    for dfCount, df in enumerate(dflist):
        df1 = df[cols].groupby(groupCol).sum().reset_index().set_index(groupCol)
        df1 = df1.sort_index(ascending=inverse_order)
        dflist[dfCount] = df1
    
    #normalize to percentaje of column sum
    if normalize is True:
        for df in dflist:
            for col in repreCols:
                suma = df[col].sum()
                for index in df.index:
                    if suma == 0:
                        df.loc[index, col] = 0
                    else:
                        df.loc[index, col] = (df.loc[index, col] / suma)*100
    
    x = np.arange(len(repreCols))  # the label locations
    
    #create list with the decalage of the locations of the bars.
    if len(dflist) == 1:
        decalist = [0,]
    else:
        decalist = []
        decal0  = - width*len(dflist)/2 + width/2
        for dfcount, _ in enumerate(dflist):
            decalist.append(decal0 + width*dfcount)
            
            
    #figure creation
    fig, ax = plt.subplots(figsize=(xSize, ySize))
    
    for dfCount, df in enumerate(dflist):
        bar=[]
        for idxCount, idx in enumerate(df.index):
            if not colorDict is None:
                color = colorDict[idx]
            else:
                color = None
                
            if idxCount == 0:
                bar.append(ax.bar(x=(x + decalist[dfCount]), 
                                  height=df.loc[idx], width=width, 
                                  label=idx, color=color))
                left = df.loc[idx]
            else:
                bar.append(ax.bar(x=(x + decalist[dfCount]), 
                                  height=df.loc[idx], width=width, label=idx,
                                  bottom=left, 
                                  color=color))
                left = [x + y for x, y in zip(left, list(df.loc[idx]))]
    
    
    if normalize is True:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_ylim(0, 100)
    
    ax.yaxis.set_major_locator(plt.MaxNLocator(yTicksNum))
    ax.set_ylabel(yLabel)
    ax.set_title(graphTitle)
    ax.set_xticks(x)
    ax.set_xticklabels(repreCols)
    

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
        
        plt.savefig(pathlib.Path(path,filename).with_suffix(".png"),
                            bbox_inches='tight',dpi=600)

    plt.show()
    
    return fig
    
if __name__ == "__main__":
    pass


    
