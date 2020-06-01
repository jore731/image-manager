#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import sys
import re
import pathlib



def polarBarPlot(data, labelCol, valueCol, colorCol, graphTitle, 
                 save=True, **kwargs):
    r"""It represents a polar bar plot with radial labels 
    and title in the center.

    Parameters
    ----------
    data : pandas dataframe
        Dataframe containing the data.
        
    labelCol : string
        Name of the dataframe column containing the texts of the labels.
        
    valueCol : string
        Name of the dataframe column containing the data.
        
    colorCol : string, 
        Name of the dataframe column 
        containing the labels to use to color code the bars.
        
    graphTitle : string
        Title to place in the center of the graph.
        If no fileName is provided, it is used to name the file.
        
    save : boolean, optional
        If True, the figure is saved into a file.
    
    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    
    sort : boolean, optional, default True
        If true, order the dataframe in valueCol order.
        
    xSize : float, optional, default 8
        max horizontal size of the figure, in inches.
        
    ySize : float, optional, default 8.
        max vertical size of the figure, in inches.
        
    barColors : dict, optional, default False.
        Dict with label:color with label as colorCol column values 
        and values as colors in hex values. 
        If false the current palette is used.
        
    clearance : float, optional
        In data units, clearance of the data. 
        Used to represend behind bars with alpha.
        
    referLine : list of floats, optional
        References lines in fraction of max data units 
        or fraction of clearance if clearance is provided.
        Example:[0.25, 0.5, 0.75]
        
    palette : seaborn compatible palette, optional
         Can be the name of a seaborn palette, 
         a seaborn palette or a list interpretable 
         as a palette by seaborn.
        
    fileName : string, optional
        if not provided graphTitle will be used. 
        Non alphanumeric values will be deleted.
        
    Examples
    --------
    >>> data = pd.DataFrame.from_dict(
    ...            {"element":["SSXX{}".format(x) for x in range(10)] 
    ...                        + ["STXX{}".format(x) for x in range(20)],
    ...             "Type":["S1"]*10 + ["S2"]*20,
    ...             "magnitude": list(np.random.randint(5000, 
    ...                                                 10000, size=(30)))})
    >>> kwargs = dict(palette = "deep",
    ...               xSize = 8,
    ...               ySize = 8,
    ...               colors = False,
    ...               fileName = "polar Bar Plot Example",
    ...               clearance = 15000,
    ...               referLine = [0.5, 0.75],
    ...               barColors = {"S1": "g", "S2": "r"},
    ...               fontScale = 1)
    >>> polarBarPlot(data, "element", "magnitude", 
    ...              "Type", "test title", **kwargs)
    """
    
    """Version 1.0"""
    
    #we create a copy to avoid  modifying the original data
    data = data.copy()
    
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
    
    ################kwargs ############################################
    sort = kwargs.get("sort", True)
    xSize = kwargs.get("xSize", 8)
    ySize = kwargs.get("ySize", 8)
    barColors = kwargs.get("barColors", False)
    clearance = kwargs.get("clearance", False)
    referLine = kwargs.get("referLine", False)
    fontScale = kwargs.get("fontScale", 1)
    fileName = kwargs.get("fileName", graphTitle)
    palette = kwargs.get("palette", "deep")
    
    ######################## input validation #########################

    if not isinstance(data, pd.DataFrame):
        raise functionError("data is not a pandas dataframe")
        
    if not isinstance(graphTitle, str):
        try:
            graphTitle = str(graphTitle)
        except:
            raise functionError("graphTitle is not a string.")

    for col in [labelCol, valueCol, colorCol]:
        if not col in data.columns.values.tolist():
            raise functionError(
                             "{} is not a df column header name.".format(col))
    if save:
        if not isinstance(save, bool):
            raise functionError("save is not a boolean")  

    if sort:
        if not isinstance(sort, bool):
            raise functionError("sort is not a boolean")  
    
    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")
        
    if clearance:
        if not isinstance(clearance, (int, float)):
            raise functionError("clearance is not a float or a integer.")
            
    if barColors:
        if not isinstance(barColors, dict):
            raise functionError("barColors is not a dict")  
            
    if referLine:
        if isinstance(referLine, float):
            referLine = [referLine, ]
        elif not isinstance(referLine, (list, tuple)):
            raise functionError("referLine is not an iterable")  
    
    if not isinstance(fontScale, (int, float)):
        raise functionError("fontScale is not a float or a integer.")
        
    if not isinstance(fileName, str):
        try:
            fileName = str(fileName)
        except:
            raise functionError("fileName is not a string.")
            
    ######################## initial settings #########################

    sns.set(style="whitegrid", font_scale=fontScale)
    sns.set_palette(palette)
    
    if sort:
        data.sort_values(valueCol, inplace=True, ascending=False)
    
    radii = data[valueCol]
    theta = np.arange(np.pi/2, (5/2)*np.pi, 2*np.pi/len(radii))
    width = (2*np.pi)/len(radii)*0.9
    
    if barColors is False:
        colors = list(sns.color_palette().as_hex())
        barColors = dict(zip(list(data[colorCol].unique()), colors))
    
    ############# Figure creation #####################################
    
    fig = plt.figure(figsize=(xSize, ySize), dpi=100)
    ax = fig.add_subplot(111, projection='polar')
    
    
    if clearance:
        refBar = ax.bar(theta, [clearance]*len(radii), width=width, alpha=0.4)
        for bar, colorCode in zip(refBar, data[colorCol]):
            bar.set_color(barColors[colorCode])

    bars = ax.bar(theta, radii, width=width)

    ####### Axis hiding and offsetting #########
    
    # Transform half the width of the graph to data units
    # to offset the radius origin of the data that amount.
    figToAxeUnits = ax.transData.inverted()
    offset = figToAxeUnits.transform((1, 1))[1]/2
    ax.set_rorigin(-offset)
    
    ax.axis("off")
    ax.spines['polar'].set_visible(False)
    
    ############# Labeling ##########
    
    # Depending on the angle, set the aligment 
    # of the text, the angle of rotation and labels.
    rotations = np.rad2deg(theta)
    haList = ["right" if 270 > rad >= 90 else "left" for rad in rotations]
    
    rotations = [rad + 180 if 270 > rad >= 90 else rad for rad in rotations]
    
    labels = ["{} ({:g})".format(ac, float('{:.4g}'.format(value))) 
              for ac, value in zip(data[labelCol], data[valueCol])]
    
    # Radii position of the text
    if clearance:
        textHeight = [bar.get_height()*1.03 for bar in refBar]
    else:
        textHeight = [bar.get_height()*1.02 for bar in bars]
    
    #label creation
    for x, rotation, label, ha,  height in zip(
            theta, rotations, labels, haList, textHeight):
        
        ax.text(x, height, label, ha=ha, va='center', 
                rotation=rotation, rotation_mode="anchor")
    
    #bar coloring
    for bar, colorCode in zip(bars, data[colorCol]):
        bar.set_color(barColors[colorCode])
    
    ####### header #######
    ax.set_title(graphTitle, weight='bold',
                 position=(0.5, 0.5),
                 horizontalalignment='center', 
                 verticalalignment='center')
    
    #### reference lines ###
    
    # Use clearance as max reference, if not provided use max data value
    if referLine:
        for ref in referLine:
            if clearance:
                ax.plot(np.linspace(0, 2*np.pi, 100), 
                        np.ones(100)*clearance*ref, 
                        color='k', linestyle='--', alpha=0.4)
            else:
                href = data[valueCol].max()*ref
                ax.plot(np.linspace(0, 2*np.pi, 100), 
                        np.ones(100)*href, 
                        color='k', linestyle='--', alpha=0.4)
                
    ############Plot saving############################################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfilename = os.path.split(fullpath)
        
        # To create the file name, remove non alphanumeric chars
        filename = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,filename).with_suffix(".png"),
                    bbox_inches='tight',dpi=300)
    
    plt.show()
    
    return fig


if __name__ == "__main__":
    pass