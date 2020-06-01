# -*- coding: utf-8 -*-
"""
@author: u64053
"""
import pandas as pd
import re
import seaborn as sns
import os
import sys
import matplotlib.pyplot as plt
import pathlib
import numpy as np

def scatterMatrix(df, graphTitle, groupCol, correCols=None, save=True, **kwargs):
    r"""Function to represent a scatter matrix with hist or kde in the diagonal
    
    Parameters
    ----------
    df : pandas dataframe
        Dataframe to plot.
        
    graphTitle : string
        Title for the plot, used as filename.
        
    groupCol : string
        Name of the df column to use to separate the df in groups.
        
    correCols : list of strings, optional
        List of the df columns to plot, 
        if None all columns except groupCol are used. 

    save : boolean, optional
        If True, the figure is saved into a file.
        
    Returns
    -------
    fig : seaborn PairGrid object
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    colors : Dict{label:color}, optional
        If provided, labels of the groupCol column and the color to use. 
        The default is False.
        
    markers : string or list of strings, optional
        markers to use for the different groups, 
        use the same if only a marker is provided.
        
    diagKind : string, optional, default "hist"
        Values: "hist", "kde" or "auto" the plot to use for the diagonal. 
        
    fontScale : float, optional, default 1.2
         Scale factor for the font size.
         
    palette : seaborn compatible palette, default "deep"
         Can be the name of a seaborn palette, 
         a seaborn palette or a list 
         interpretable as a palette by seaborn.
         
    fileName : string, optional
         File name to save, if not provided graphTitle will be used. 
         Non alphanumeric values will be deleted.
         
    {plot, diag, grid}_kwsdicts : dicts, optional
        Dictionaries of keyword arguments. 
        plot_kws are passed to the bivariate plotting function, 
        diag_kws are passed to the diagonal plotting function, 
        and grid_kws are passed to the PairGrid constructor
    
    Examples
    --------
    >>> df = pd.DataFrame.from_dict(
    ...         {"type": ["S1", "S2", "S1"]*20,
    ...          "var0": np.random.normal(5, 1, 60),
    ...          "var1": np.random.triangular(2, 3, 6, 60),
    ...          "var2": np.random.normal(5, 0.8, 60)})
    >>> scatterMatrix(df, graphTitle="scatter plot", groupCol="type", 
    ...               correCols=['var0', 'var1', 'var2'], 
    ...               colors={"S1": "b", "S2": "orange"},
    ...               markers=["d", "o"], diagKind='hist',
    ...               fontScale=1.2)
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
    
    ################################Kwargs#############################
    colors = kwargs.get("colors", False)
    markers = kwargs.get("markers", None)
    diagKind = kwargs.get("diagKind", "hist")
    fontScale = kwargs.get("fontScale", 1)
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphTitle)
    plot_kws = kwargs.get("plot_kws", None)
    diag_kws = kwargs.get("diag_kws", None)
    grid_kws = kwargs.get("grid_kws", None)

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
    
    if not isinstance(correCols, (list, tuple)):
        correCols = [correCols, ]
    for col in correCols:
        if not col in df.columns.values.tolist():
            raise functionError("{} is not a df column header name.".format(col))
    
    if not groupCol in df.columns.values.tolist():
        raise functionError("{} is not a df"
                            " column header name.".format(groupCol))
    
    if not isinstance(save, bool):
        raise functionError("save is not a boolean")
        
    
    if not diagKind in ["hist", "kde", "auto"]:
        raise functionError("diagKind is not a valid value.")
        
    if not isinstance(fontScale, (float, int)):
        raise functionError("fontScale is not a float")
    
    if not isinstance(fileName, str):
        try:
            fileName = str(fileName)
        except:
            raise functionError("fileName is not a string.")
    
    #######initial settings ###########################################
    sns.set(style="ticks", font_scale=fontScale)
    sns.set_palette(palette)

    if correCols is None:
        correCols = list(df.columns)
    
    if colors:
        hueOrder =  []
        palette = []
        for key, value in colors.items():
            hueOrder.append(key)
            palette.append(value)
    else:
        hueOrder = list(df[groupCol].unique())
        palette = sns.color_palette()
    
    
    fig = sns.pairplot(df[correCols + [groupCol]], hue=groupCol, 
                       hue_order=hueOrder, height=3, palette=palette, 
                       kind="scatter", markers=markers, diag_kind=diagKind,
                       plot_kws=plot_kws, grid_kws=grid_kws, diag_kws=diag_kws)
    fig.fig.suptitle(graphTitle, y=1.08)
    
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
