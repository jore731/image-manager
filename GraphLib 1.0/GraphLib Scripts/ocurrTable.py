#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import os
import pathlib
import sys
import re


def ocurrenceTable(df, groupColumns, countColumn, fileName, 
                   save=True, **kwargs):
    r"""Represents ocurrence and prints a grouped table 
    from a python dataframe.
    
    It Aggregates the diferent values of 
    the Dataframes groupColumns to count occurrence in countColumn.
    
    It allows to add totals by column or row.
    
    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing the data.
        
    groupColumns : list of strings
        df columns names to display as grouped columns.
        
    countColumn : string
        df column name to count ocurrence.
        
    fileName : string
        filename to use to save the table, 
        non alphanumeric characters will be removed.
        
    save : boolean, optional
        If True, the figure is saved into a file.
    
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    colColor : string, optional, default "grey"
        Colors of the header row, hex value or named color. 
        
    fontSize : float, optional,
        Font size of the table
        
    xSize : float, optional, default 8, 
        max horizontal size of the figure, in inches.
        
    ySize : float, optional, default 8, 
        max vertical size of the figure, in inches.
        
    rowColoring : boolean, optional, default True
        if True the cells are colored following the palette provided.
        
    totalRow : boolean, optional, default False,  
        if True a "total per row" column will be generated.
        
    totalCol : boolean, optional, default False, 
        if True a "total per column" row will be generated.
        
    footnote : string, optional
        footnote text to display
        
    footnoteStyle : string, optional, default "italic"
        style for the footnote, 
        valid values: 'normal', 'italic', 'oblique'.
        
    footnoteColor : string, optional, default "grey"
        colors the text of the footnote, hex value or named color. 
        
    palette : seaborn compatible palette, optional
         Can be the name of a seaborn palette, 
         a seaborn palette or a list interpretable 
         as a palette by seaborn.
        
    Examples
    --------
    >>> df = pd.DataFrame({
    ...            "Tranche":["T1","T1","T1","T1","T1","T1","T1","T1","T1","T1",
    ...                       "T2","T2","T2","T2","T2","T2","T2","T2","T2","T2",
    ...                       "T3","T3","T3","T3","T3","T3","T3","T3","T3","T3"],
    ...            "Batch":[1,1,1,1,1,2,2,2,3,3,
    ...                     2,2,3,3,3,3,3,3,3,3,
    ...                     4,4,4,4,4,4,4,4,4,4],
    ...            "Block":["1A","1A","1B","1B","1C","2B","2B","2B","2C","2D",
    ...                     "8A","8A","8A","8B","8B","8B","8C","8C","8C","8D",
    ...                     "20","30","30","30","20","20","20","20","20","20"],
    ...            "Conf":["S2","S2","S2","S1","S2","S1","S2","S1","S2","S1",
    ...                    "S2","S1","S2","S1","S2","S1","S2","S1","S2","S1",
    ...                    "S2","S1","S2","S1","S2","S1","S2","S1","S2","S1"]
    ...            })
    >>>  ocurrenceTable(df,
    ...                 groupColumns=["Tranche","Batch","Block"],
    ...                 colColor="grey",
    ...                 countColumn="Conf",
    ...                 palette="deep",
    ...                 fontSize=18,
    ...                 xSize=8,
    ...                 ySize=8,
    ...                 totalRow=True,
    ...                 totalCol=True,
    ...                 fileName="test ocurrence table",
    ...                 footnote="*footnote for test"
    ...                 )
    """
    
    """Version 1.0"""
    
    #we create a copy to avoid  modifying the original database
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
    

    def extraCell(x, y, w, h, text, fontSize, color="w", fill=True):
        """Extra cell creator

        Parameters
        ----------
        x : float
            x position of the cell
        y : float
            y position of the cell
        w : float
            width of the cell
        h : float
            height of the cell
        text : string
            text of the cell
        fontSize : float
            cont Size of the cell
        color : string, optional, default white
            Color of the cell
        fill : boolean, optional, default True
            If True, the cell is filled with color.

        Returns
        -------
        rectangle : matplotlib rectangle object
            rectangle of the cell

        """
        
        rect = patches.Rectangle((x, y), w, h,
                                 linewidth=1,
                                 edgecolor='k',
                                 facecolor=color,
                                 clip_on=False,
                                 fill=fill)
        
        rectangle = ax.add_patch(rect)
        rx, ry = rectangle.get_xy()
        ax.annotate(text,
                    (rx + rectangle.get_width()/2.0,
                     ry + rectangle.get_height()/2.0),
                    color='k',
                    fontsize=fontSize, 
                    ha='center', 
                    va='center',
                    annotation_clip=False)
        return rectangle
    
    #########################Kwargs####################################
    
    colColor = kwargs.get("colColor", "grey")
    fontSize = kwargs.get("fontSize", False)
    xSize = kwargs.get("xSize", 8)
    ySize = kwargs.get("ySize", 8)
    rowColoring = kwargs.get("rowColoring", True)
    totalRow = kwargs.get("totalRow", False)
    totalCol = kwargs.get("totalCol", False)
    footnote = kwargs.get("footnote", False)
    footnoteStyle = kwargs.get("footnoteStyle", "italic")
    footnoteColor = kwargs.get("footnoteColor", "grey")
    palette = kwargs.get("palette", "deep")

    #########################Input validation##########################
    
    if not isinstance(df, pd.DataFrame):
        raise functionError("df is not a pandas dataframe")
    
    if not countColumn in df.columns.values.tolist():
        raise functionError("{} is not a df "
                         "column header name.".format(countColumn))
    
    for col in groupColumns:
        if not col in df.columns.values.tolist():
            raise functionError("{} is not a"
                             " df column header name.".format(col)) 
    
    if isinstance(fileName, str):
        try:
            fileName = str(fileName)
        except:
            raise functionError("fileName is not a string.")

    if not isinstance(fontSize, (int, float)):
        raise functionError("fontSize is not a float or a integer.")

    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")

    if not isinstance(rowColoring, bool):
        raise functionError("rowColoring is not a boolean.")
    
    if not isinstance(totalRow, bool):
        raise functionError("Error: totalRow is not a boolean.")

    if not isinstance(totalCol, bool):
        raise functionError("totalCol is not a boolean.")
    
    if footnote:
        if isinstance(footnote, str):
            try:
                footnote = str(footnote)
            except:
                raise functionError("footnote is not a string.")
                
        if not footnoteStyle in ('normal', 'italic', 'oblique'):
            raise functionError("footnoteStyle is not "
                             "one of 'normal', 'italic', 'oblique'")
    
    #########################Initial settings and calculations#########
    
    sns.set_palette(palette)
    
    # Drop columns not used as groups or to count ocurrence
    checkColumn = groupColumns + [countColumn,]
    for column in df.columns:
        if not column in checkColumn:
            df.drop(column, axis=1, inplace=True)
    
    #separate countColumn by labels
    df = pd.concat([df, pd.get_dummies(df[countColumn])], axis=1, sort=False)
    
    df.drop([countColumn], axis=1, inplace=True)
    df = df.groupby(groupColumns).sum()
    df = df.reset_index()
    
    ###### figure creation ############################################
    fig, ax = plt.subplots(figsize=(xSize, ySize))
    
    # Original traditional table representation
    cellText = []
    for row in range(len(df)):
        cellText.append(df.iloc[row])
    
    theTable = ax.table(cellText=cellText,cellLoc='center',
                        colLabels=df.columns,
                        colColours=[colColor]*len(df.columns),
                        bbox=[0, 0, 1, 1]
                        )
    
    if not fontSize:
        theTable.auto_set_font_size(True)
        fontSize = theTable[0,0].get_fontsize()
    tableFontSize = fontSize
    ax.axis('off')
    
    # A white rectangle is put in front of the table to hide it.
    # We don't directly hide the table because 
    # we want the edges of the original table.
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor='w'))
    
    h = 1/(len(cellText) + 1)
    w = 1/(len(cellText[0]))
    
    # Paint headers
    for colnum, column in enumerate(df.columns):
        
        extraCell(w*(colnum), 1 - h, w, h, column, tableFontSize, colColor)
    
    
    # For each grouped column find unique values with counts.index
    # For each unique values find the [start,stop] rows 
    # where the value is repeated
    groupList = []
    x = 0
    for col in groupColumns:
        x += 1
        values = df[col].value_counts(dropna=True).index
        for value in values:
            y = 0
            while y in range(len(df[col])):
                if df[col][y] == value:
                    start = y
                    stop = y
                    y += 1
                    while y in range(len(df[col])) and df[col][y] == value:
                        stop = y
                        y += 1
                    groupList.append([str(value), x, start, stop])
                else:
                    y += 1
    
    # Color painting using the first column as color labels
    if rowColoring:
        colorGroupList = [group for group in groupList if group[1] == 1]
        colorList = list(sns.color_palette().as_hex())
        
        colorCounter = -1
        for value, dummy, start, stop in colorGroupList:
            colorCounter += 1
            for x in range(1, len(df.columns) + 1):
                rect = patches.Rectangle((w*(x - 1), 1 - h*(stop + 2)),
                                         w,
                                         h*(stop - start + 1),
                                         linewidth=0,
                                         facecolor=colorList[colorCounter],
                                         alpha=(1-((x-1)/(len(df.columns)+1)))
                                         )
                ax.add_patch(rect)
    
    # Create rectangles in top of the table making "merged" cells for groupColumns
    for value, x, start, stop in groupList:
        
        extraCell(w*(x - 1), 1 - h*(stop + 2),
                  w, h*(stop - start + 1), value, tableFontSize, fill=False)
    
    # Create a new table for the not grouped data
    dfData = df[[col for col in df.columns if not col in groupColumns]]
    
    cellTextData = []
    for row in range(len(dfData)):
        cellTextData.append(dfData.iloc[row])
    
    dataTable = ax.table(cellText=cellTextData, cellLoc='center', 
                         bbox=[w*len(groupColumns), 
                               0, 1 - w*len(groupColumns), 1 - h],
                         zorder=10)
    
    dataTable.auto_set_font_size(False)
    dataTable.set_fontsize(tableFontSize)
    
    for row in range(0, len(dfData)):
        for column in range(0, len(dfData.columns)):
            dataTable[row, column].set_fill(False)
    
    if totalRow:
        totalsRow = []
        for row in range(len(dfData)):
            try:
                totalsRow.append(dfData.iloc[row].sum())
            except:
                totalsRow.append("")
            
            extraCell(1, 1 - h*(row + 2), w, h, totalsRow[row], tableFontSize)
                        
        # Add total row header
        extraCell(1, 1 - h, w, h, "Total", tableFontSize, colColor)
        
    if totalCol:
        totalsCol = []
        for ncol, col in enumerate(dfData.columns):
            try:
                totalsCol.append(dfData[col].sum())
            except:
                totalsCol.append("")
            
            extraCell(w*(len(groupColumns) + ncol), 0 - h, w, h,
                      totalsCol[ncol], tableFontSize)

    #Add global total if row and col totals
    if totalRow and totalCol:
        try:
            extraCell(1, 0 - h, w, h, sum(totalsCol), tableFontSize)
        except:
            pass

    # Footnote addition
    if footnote:
        if totalRow:
            footHeight = -2*h
        else:
            footHeight = -h
            
        ax.annotate(footnote,
                    (0, footHeight),
                    fontsize=tableFontSize,
                    ha='left',
                    va='bottom',
                    annotation_clip=False,
                    fontstyle=footnoteStyle,
                    color=footnoteColor)

    ##########################Figure Saving############################
    if save is True:
        # Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfileName = os.path.split(fullpath)
        
        # To create the file name, remove non alphanumeric chars
        name = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,name).with_suffix(".png"),
                    bbox_inches='tight')
    
    plt.show()
    
    return fig
    
if __name__ == "__main__":
    pass

    df = pd.DataFrame({
               "Tranche":["T1","T1","T1","T1","T1","T1","T1","T1","T1","T1",
                          "T2","T2","T2","T2","T2","T2","T2","T2","T2","T2",
                          "T3","T3","T3","T3","T3","T3","T3","T3","T3","T3"],
               "Batch":[1,1,1,1,1,2,2,2,3,3,
                        2,2,3,3,3,3,3,3,3,3,
                        4,4,4,4,4,4,4,4,4,4],
               "Block":["1A","1A","1B","1B","1C","2B","2B","2B","2C","2D",
                        "8A","8A","8A","8B","8B","8B","8C","8C","8C","8D",
                        "20","30","30","30","20","20","20","20","20","20"],
               "Conf":["S2","S2","S2","S1","S2","S1","S2","S1","S2","S1",
                       "S2","S1","S2","S1","S2","S1","S2","S1","S2","S1",
                       "S2","S1","S2","S1","S2","S1","S2","S1","S2","S1"]
               })
    ocurrenceTable(df,
                    groupColumns=["Tranche","Batch","Block"],
                    colColor="grey",
                    countColumn="Conf",
                    palette="deep",
                    fontSize=18,
                    xSize=8,
                    ySize=8,
                    totalRow=True,
                    totalCol=True,
                    fileName="test ocurrence table",
                    footnote="*footnote for test"
                    )

