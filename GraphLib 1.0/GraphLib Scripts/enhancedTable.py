#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.patches as patches
from math import floor, log10, isnan
import os
import sys
import re
import pathlib

def enhancedTable(df, fileName, rowLabelCol, save=True, **kwargs):
    r"""Represent a table or several tables. 
    Options to add a total row, header, labels...
        
    Parameters
    ----------
    df : pandas Dataframe
        Dataframe containing the data.
        
    fileName : string
        Filename to use to save the table, 
        non alphanumeric characters will be removed.
        
    rowLabelcol : string
        Name of the dataframe column of df to use as label values.
    
    save : boolean, optional
        If True, the figure is saved into a file.
       
    Returns
    ----------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    labelStyle : string, optional, default "label",
        Style of the labels, "label" or "column".
        
    totalRow : boolean, optional, default False
        If true add a new row with the total per colum.
        
    header : string, optional, default False
        If it has a value add a header cell with that value.
        
    tableNum : integer, optional, default 1.
        Number of tables to split the data in.
        
    layout : string, optional, default "vertical"
        Layout to place the tables relative to each others, can be
        'horizontal' or 'vertical'.
        
    fontSize : integer, optional, default False.
        Size of the font, if False, 
        let the code decide the best horizontal fit.
        
    xSize : float, optional, default 18
        Max horizontal size of the figure, in inches.
        
    ySize : float, optional, default 8.
        Max vertical size of the figure, in inches.
        
    rowLabelColor : string, optional, default "grey"
        Color to use for the labels, named colors or HEX values.
        
    colLabelColor : string, optional, default "grey"
        Color to use for the labels, named colors or HEX values.
        
    minimalistic : boolean, optional, default False. 
        If true, most of the cell lines are hidden.
        
    palette : seaborn palette or compatible, optional.
        Seaborn compatible palette, 
        can be the name of a seaborn palette, 
        a seaborn palette or a list interpretable 
        as a palette by seaborn.
    
    Examples
    --------
    >>> data={"Type":["S1", "S2"],
    ...       "F":[15000, 12000],
    ...       "FH":[21000, 15000],
    ...       "Total landings":[42000, 11000],
    ...       "FS landings":[10000, 2396],
    ...       "AR land":  [10, 1],
    ...       "RL": [100, 600],
    ...       "T&G": [8000, 9500],
    ...       "Bounces":[19000, 2000],
    ...       "Test Deploy":["not available", "not available"],
    ...       "In-flight  Deploy":[4000, 700],
    ...       "MNT probe Deploy":["not available", "not available"],
    ...       "Contacts":["not available", "not available"],
    ...       "Total Cycles":[45000, 16000],
    ...       "In-flight Cycles":[37000, 11000],
    ...       "MNT Cycles":[800, 444],
    ...       "Antena":[550, 333]}
    >>> df = pd.DataFrame.from_dict(data)
    >>> kw = dict(labelStyle="label",
    ...           totalRow=True,
    ...           header="test header",
    ...           tableNum=4,
    ...           layout="vertical",
    ...           fontSize=18,
    ...           xSize=16,
    ...           ySize=12,
    ...           rowLabelColor="grey",
    ...           colLabelColor='b')
    >>> fig = enhancedTable(df, "test table", rowLabelCol="Type",
    ...                     save=True, **kw)
    
    """
    
    "Version 1.0"
    
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
    
    #Create a copy to avoid modifying the original database
    df = df.copy() 
    
    #################Kwargs############################################
    labelStyle = kwargs.get("labelStyle", "label")
    totalRow = kwargs.get("totalRow", False)
    header = kwargs.get("header", False)
    tableNum = kwargs.get("tableNum", 1)
    layout = kwargs.get("layout", "vertical")
    fontSize = kwargs.get("fontSize", False)
    xSize = kwargs.get("xSize", 18)
    ySize = kwargs.get("ySize", 8)
    rowLabelColor = kwargs.get("rowLabelColor", "grey")
    colLabelColor = kwargs.get("colLabelColor", "grey")
    palette = kwargs.get("palette", "deep")
    
    ######################Input validation#############################
    #input validation is not necesary in python
    #but it is performed here to easily error handeling.
    if not isinstance(df, pd.DataFrame):
        raise functionError("df is not a pandas dataframe")
    
    if not isinstance(fileName, str):
        try:
            fileName = str(fileName)
        except:
            raise functionError("Filename is not a string.")
    
    if not rowLabelCol in df.columns.values.tolist():
        raise functionError("{} is not a df column header name.".format(
                                                                 rowLabelCol))

    if not labelStyle in ("label", "column"):
        raise functionError("labelStyle is not valid."
                            " Valid values are 'label', 'column.")

    if not isinstance(totalRow, bool):
        raise functionError("totalRow is not a boolean.")
        
    if header:
        if not isinstance(header, str):
            try:
                header = str(header)
            except:
                raise functionError("header is not a string.")
    
    if not layout in ("horizontal", "vertical"):
        raise functionError("layout is not valid. "
                         "Valid values are 'horizontal', 'vertical.")
    
    if not isinstance(fontSize, (int, float)):
        raise functionError("fontScale is not a float or a integer.")

    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")

    ###################Initial settings and calculation################
    sns.set(style="whitegrid")
    sns.set_palette(palette)
    
    def smartSum(serie):
        '''
        Custom agregator function to improve .sum() behaviours
        - if number sum as usual, 
        - if all strings are equal put that string 
        - if different strings return nothing
        '''
        res = 0
        for x in serie:
            if isinstance(x,(int, float)):
                res +=x
            elif isinstance(x,str):
                if list(serie).count(serie[0]) == len(serie):
                    return serie[0]
                else:
                    return ""
        return res
    
    def repre_map(x, sig=3):
        '''
        Important: only use to represent, do not modify a df with this map
        
        To represent dataframes in a visualy appealing way, 
        int numbers as ints, strings as strings, and 
        floats with less than 1% representation error
        Transform NaN values to empty strings
        '''
        if isinstance(x,float):
            if isnan(x):
                return ""
            elif (int(x) - x) == 0: #if is int return x
                return "{}".format(int(x))
            elif abs(x) >= 100:
                return "{}".format(int(x))
            elif abs(x) >= 10:
                return round(x, 1)
            elif abs(x) >= 1:
                return round(x, 2)
            else: #round to 3 significant figures
                return round(x, sig-int(floor(log10(abs(x))))-1)
        else:
            return x
    
    #if total is selected append a list containing totals,
    #for use "All" as label for this total row
    #for not numeric values leave totals empty.
    if totalRow:
        seriesAll = df.agg(smartSum)
        seriesAll[rowLabelCol]="All"
        df = df.append(seriesAll, ignore_index=True)

    #apply representation map to df
    #create new df with only the labels, 
    #and remove them from the original.
    df = df.applymap(repre_map)
    dfRowLabel = df[[rowLabelCol]]
    
    df.drop(rowLabelCol, axis=1, inplace=True)
    
    #create a list splitting the column in n=tableNum groups
    columPerAxList=[list(x) for x in np.array_split(df.columns,tableNum)]
    
    #choose table height depending if a header is added.
    if not header:
        tableHeight = 1
    else:
        tableHeight = (1 - (1/(len(df) + 2)))
    
    #######################figure creation#############################
    if layout == "horizontal":
        fig, axes = plt.subplots(figsize=(xSize, ySize), ncols=tableNum)
    else:
        fig, axes = plt.subplots(figsize=(xSize, ySize), nrows=tableNum)      
    
    tableItemList = []
    
    #to avoid errors when only an ax is made
    try: 
        axNums = range(0, len(axes.flat))
    except:
        axNums = [0,]
        
    for axNum in axNums:
        try:
            ax = axes.flat[axNum]
        except:
            ax = axes
        if labelStyle == "label":
            #Create a section of the df to represent in that table
            dfAx = df[columPerAxList[axNum]]
            
            cellText = []
            for row in range(len(dfAx)):
                cellText.append(dfAx.iloc[row])
            
            rowColorList=[rowLabelColor]*len(dfRowLabel[rowLabelCol])
            colColoursList=[colLabelColor]*len(columPerAxList[axNum])
            
            tableItemList.append(
                    ax.table(cellText=cellText,cellLoc='center',
                             rowLabels=dfRowLabel[rowLabelCol],
                             rowColours=rowColorList,
                             colLabels=dfAx.columns,
                             colColours=colColoursList, 
                             bbox=[0, 0, 1, tableHeight]
                             ))
        elif labelStyle == "column":
            # Create a section of the df to represent in that table 
            # and add the labels
            dfAx = pd.concat(
                      [dfRowLabel[[rowLabelCol]], df[columPerAxList[axNum]]], 
                      axis=1, sort=False)
            
            cellText = []
            cellcolor = []
            for row in range(len(dfAx)):
                cellText.append(dfAx.iloc[row])
                colorRow=[rowLabelColor] + ["w"]*len(columPerAxList[axNum])
                cellcolor.append(colorRow)

            tableItemList.append(
                    ax.table(cellText=cellText,cellLoc='center',
                             cellColours=cellcolor,
                             colLabels=dfAx.columns,
                             colColours=[colLabelColor]*(
                                     len(columPerAxList[axNum]) + 1),
                             bbox=[0, 0, 1, tableHeight]
                             ))
        
        if fontSize:
            tableItemList[axNum].auto_set_font_size(False)
            tableItemList[axNum].set_fontsize(fontSize)
        
        ax.axis('off')
        
        # Header we create a rectangle 
        # and annotate the text in the middle.
        if header:
            rect = patches.Rectangle((0,tableHeight),1,(1/(len(df)+2)),
                                     linewidth=1,
                                     edgecolor='k',
                                     facecolor=colLabelColor,
                                     clip_on=False
                                     )
            
            rectangle = ax.add_patch(rect)
            rx, ry = rectangle.get_xy()
            tableFontSize = tableItemList[axNum][0,0,].get_fontsize()
            
            headerObj = ax.annotate(header,
                                    (rx + rectangle.get_width()/2.0,
                                     ry + rectangle.get_height()/2.0),
                                    color='k',
                                    fontsize=tableFontSize, 
                                    ha='center', 
                                    va='center')
        
        #Change font color if the cell are too dark
        for (x, y), cell in tableItemList[axNum].get_celld().items():
            red, green, blue, alpha = cell.get_fc()
            L = (red*0.299 + green*0.587 + blue*0.114)*255
            if  L < (186):
                cell.get_text().set_color('w')
                if header:
                    headerObj.set_color('w')
                
                
    ##########################Figure Saving############################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfilename = os.path.split(fullpath) 
        
        # To create the file name, remove non alphanumeric chars
        name= re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,name).with_suffix(".png"), 
                    bbox_inches='tight', dpi=300)

    plt.show()
    
    return fig

if __name__ == "__main__":
    pass
                           