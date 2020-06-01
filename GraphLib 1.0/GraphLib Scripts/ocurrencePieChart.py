#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import pathlib
import sys
import re
import seaborn as sns

def ocurrPieChart(df, countCol, graphTitle, save=True, **kwargs):
    r"""Generates a pie chart according to 
    the occurence of values in a column of a dataframe.
    
    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing the data.
        
    countCol : string
        Column of the df to count the ocurrence of the values.
        
    graphTitle : string, 
        title of the graph and name of the file 
        if fileName is not provided.
        
    save : boolean, optional
        If True, the figure is saved into a file.

    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    sufix : string, optional
        sufix to the labels
        
    xSize : float, optional, default 8, 
        max horizontal size of the figure, in inches.
        
    ySize : float, optional, default 8, 
        max vertical size of the figure, in inches.
        
    fontScale : float, optional, default 1, 
        global font scalation factor for every text of the figure.
        
    linewidth : float, default 0, 
        Contour line width for the pie slices 
        in pixels, if 0 no line is displayed.
        
    linecolor : strings, optional, default "k", 
        Colors to use for the contour lines to use, 
        hex value or named color.
        
    shadow : boolean, optional, default False
        If True, shadows are displayed for the pie.
        
    explode : float, optional, default 0, 
        exploding factor for the pie chart, it separates the pie slices.
        If 0, no explosion is performed.
    
    footnote : string, optional
        footnote text to display
   
    foonoteSize : float, optionial, default 18. 
        Font size of the footnote.
        
    footnoteColor : string, optional, default "grey"
        colors the text of the footnote, hex value or named color. 
        
    footnoteStyle : string, optional, default "italic"
        style for the footnote, 
        valid values: 'normal', 'italic', 'oblique'.
        
    palette : seaborn compatible palette, optional
         Can be the name of a seaborn palette, 
         a seaborn palette or a list interpretable 
         as a palette by seaborn.
        
    fileName : string, optional
        if not provided graphHeader will be used. 
        Non alphanumeric values will be deleted.
        
    Examples
    --------
    >>> df = pd.DataFrame(
    ...                {'element': ['elemXX', 'elemX1', 'elemX2', 
    ...                             'elemX3', 'elemX4', 'elemX5',
    ...                             'elemX6', 'elemX7', 'elemX8', 
    ...                             'elemX9', 'elem10', 'elem11',
    ...                             'elem12', 'elem13'],
    ...                 'groups': ['group1','group1','group1','group1',
    ...                            'group2','group2','group2','group3',
    ...                            'group4','group4','group4','group4',
    ...                            'group5','group5']})
    >>> ocurrPieChart(df,
    ...               countCol='groups',
    ...               graphTitle="Test table",
    ...               sufix=" elements",
    ...               fontScale=1.6,
    ...               palette="pastel",
    ...               linewidth=2,
    ...               linecolor="grey",
    ...               explode=0.03,
    ...               footnote="*footnote for test ",
    ...               footnoteStyle='italic',
    ...               fileName= "ocurr Pie Chart example"
    ...               )
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
            
    ################################Kwargs#############################
    
    sufix = kwargs.get("sufix", "")
    xSize = kwargs.get("xSize", 8)
    ySize = kwargs.get("ySize", 8)
    fontScale = kwargs.get("fontScale", 1.2)
    linewidth = kwargs.get("linewidth", 0)
    linecolor = kwargs.get("linecolor", "k")
    shadow = kwargs.get("shadow", False)
    explode = kwargs.get("explode", 0)
    footnote = kwargs.get("footnote", False)
    foonoteSize = kwargs.get("foonoteSize", 18)
    footnoteColor = kwargs.get("footnoteColor", "gray")
    footnoteStyle = kwargs.get("footnoteStyle", "italic")
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphTitle)
    
    ####################Input validation###############################
    
    if not isinstance(df, pd.DataFrame):
        raise functionError("Error: df is not a pandas dataframe")
    
    if not countCol in df.columns.values.tolist():
        raise functionError(
                         "{} is not a df column header name.".format(countCol))
    
    if not isinstance(graphTitle, str):
        try:
            graphTitle = str(graphTitle)
        except:
            raise functionError("graphTitle is not a string.")

    if not isinstance(sufix, str):
        try:
            sufix = str(sufix)
        except:
            raise functionError("sufix is not a string.")

    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")

    if not isinstance(fontScale, (int, float)):
        raise functionError("fontScale is not a float or a integer.")
    
    if not isinstance(linewidth, (int, float)):
        raise functionError("linewidth is not a float or a integer.")
    
    if not isinstance(shadow, bool):
        raise functionError("shadow is not a boolean.")
    
    if not isinstance(explode, (int, float)):
        raise functionError("explode is not a float or a integer.")

    if footnote:
        if not isinstance(footnote, str):
            try:
                footnote = str(footnote)
            except:
                raise functionError("footnote is not a string.")
        
        if not isinstance(foonoteSize, (int, float)):
            raise functionError("foonoteSize is not a float or a integer.")
        
        if not footnoteStyle in ('normal', 'italic', 'oblique'):
            raise functionError("footnoteStyle is"
                             " not one of 'normal', 'italic', 'oblique'")
    
    if not isinstance(fileName, str):
        try:
            fileName = str(fileName)
        except:
            raise functionError("fileName is not a string.")
    
    ####################initial settings and calculations##############
    sns.set(style="whitegrid", font_scale=fontScale)
    sns.set_palette(palette)
    
    #count the ocurrence and create the labels.
    counts = df[countCol].value_counts(dropna=True)
    values = counts.values
    labels = []
    for value in list(counts.index):
        labels.append("{}: ({}{})".format(value, counts[value], sufix))
    
    #####################Figure creation###############################
    fig, ax= plt.subplots(figsize=(xSize, ySize))
    
    ax.set_title(graphTitle, fontsize="large")
    
    ax.pie(values,
           labels=labels,
           autopct='%.2f%%',
           wedgeprops = {'linewidth': linewidth,
                         'ec': linecolor,
                         'linestyle': '-',
                         'hatch': '',
                         'alpha': 1},
           shadow =shadow,
           explode=[explode]*len(values)
           )
    
    ######################Footnote creation############################
    if footnote:
        ax.annotate(footnote,
                    (0, 0),
                    xycoords='axes fraction',
                    fontsize=foonoteSize,
                    ha='left',
                    va='top',
                    annotation_clip=False,
                    fontstyle=footnoteStyle,
                    color=footnoteColor)
    
    ##########################Figure Saving############################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path = os.path.split(fullpath)[0] #caller file path and name
        
        # To create the file name, remove non alphanumeric chars
        name = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,name).with_suffix(".png"),
                    bbox_inches='tight',dpi=600)
    
    plt.show()
    

if __name__ == "__main__":
    pass

