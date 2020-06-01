#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import seaborn as sns
import pandas as pd
import math
import os
import sys
import re
import pathlib

def radarArrayGraph(df, titleCol, radiusCol, graphHeader, save=True, **kwargs):
    r"""It represents an array of radarGraphs, 
    with the possibility to use custom axes for each variable. 
    Can represent a reference value and deviation form reference.

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing the data.
        
    titleCol : string, 
        Dataframe column header containing 
        the elements of the graph, 
        one plot will be made for each element in this column 
        and the value of this colum will be used as title.
        
    radiusCol : list of strings,
        variables to represent in the radius of the plots.
        
    graphHeader: string
        Header to display for the graph, 
        will be used for naming the saved file.

    Returns
    -------
    fig : matplotlib figure object.
        figure that stores the generated graph.
    
    Other parameters
    ----------------
    numPlotCols : int, optional
        For the array of plots, number of columns. 
        If not provided a layout as squared as posible will be used.
        
    radTicksNum : int, optional, default 4
        Number of circular grid lines.
        
    xSize : float, optional, default 12
        Max horizontal size of the figure, in inches.
        
    ySize : float, optional, default 12
        max vertical size of the figure, in inches.
        
    multiScale : boolean, optional, default False.
        If True, activates multiple escale mode 
        for the radial axis of the plots.
        
    radLim : float, optional,
        if `multiScale` is False, maxiumun value for the radial axes.
        
    radiusMax : list of floats, optional
        if `multiScale` is True, maximun value for each 
        of the axes, use the order defined in `radiusCol`.
        
    fontScale : float, optional, default 1
        global scalation factor for every text of the figure.
        
    radTextSize :  string, optional, default "large"
        relative font size of the labels of the axes. 
        Valid values are  'xx-small', 'x-small', 'small', 
        'medium', 'large', 'x-large', 'xx-large'
        
    scaleTextSize : string, optional, default "small"
        relative font size of the labels of the plot grid. 
        Valid values are  'xx-small', 'x-small', 'small', 
        'medium', 'large', 'x-large', 'xx-large'
        
    titleTextSize : string, optional, default "large", 
        Relative font size of the title of each plot. 
        Valid values are  'xx-small', 'x-small', 'small', 
        'medium', 'large', 'x-large', 'xx-large'
        
    headerTextSize : string, optional, default "x-large"
        relative font size of the header of the figure. 
        Valid values are  'xx-small', 'x-small', 'small', 
        'medium', 'large', 'x-large', 'xx-large'
        
    headerVerPad : float, optional, default 0.08
        vertical padding for the header of the figure.
        
    color : string, optional, default False, 
        if false chooses the first color of the current palette.
        
    reference : list of strings, optional, default False, 
        if not false, value in the dataframe in 
        the col titleCol to use as a reference, 
        this register will be used as a reference 
        and not represented as a separated plot.
        
    referCol : string, optional
        Header of the col of the dataframe 
        to use as key to add references. 
        If not provided, all the itemps in `reference` are allways displayed.
        
    referColor : list of strings, optional,
        Colors to use to represent reference values. 
        Must have more elements than reference.
        
    devTable : boolean, optional, default False
        If true, a table with de deviation 
        from the reference is displayed.
        
    legTitle : string, optional, default "Ref. Deviation"
        text to display as the title of the deviation table.
        
    palette : seaborn compatible palette, 
         Can be the name of a seaborn palette, 
         a seaborn palette or a list 
         interpretable as a palette by seaborn.
         
    fileName : string, optional
         File name to save, if not provided graphHeader will be used. 
         Non alphanumeric values will be deleted.
        
    Examples
    --------
    >>> data={"AC": ["S1","S2","SXXX","SYYY","SZZZ","SAAA",
    ...              "SBBB","SBB1","SBB2","SBB3","SB34","SB67"],
    ...       "rad1": [1500, 1800, 1200, 1700, 1700, 1500, 
    ...                1860, 1900, 1720, 1650, 650, 1234],
    ...       "rad2": [1650, 1600, 1000, 1700, 1500, 1500, 
    ...                1860, 1900, 1720, 1650, 650 ,1234],
    ...       "rad4": [180, 800, 150, 700, 180, 500, 
    ...                160, 900, 720, 650, 650, 1234],
    ...       "rad5": [700, 400, 600, 500, 650, 550, 
    ...                520, 495, 605, 675, 650, 1234],
    ...       "rad6":[0.550, 0.600, 0.600, 0.500, 0.650,
    ...               0.55, 0.52, 0.495, 0.605, 0.675, 0.65, 0.1234],
    ...       "rad7":[1500, 1400, 1600, 1500, 1650, 1550, 
    ...               1520, 1495, 1605, 1675, 650, 1234],
    ...       "type":["na", "na", "S1", "S2", "S1",
    ...               "no data", "S1", "no data", "S1", "S2", "S1", "S2"]}
    >>> df = pd.DataFrame.from_dict(data)
    >>> radarArrayGraph(
    ...         df.head(6),
    ...         "AC",
    ...         ["rad7", "rad4", "rad6", "rad1", "rad2", "rad5"],
    ...         'radar Array Example', 
    ...         numPlotCols=2,
    ...         radTicksNum=5, 
    ...         xSize=12, 
    ...         ySize=10, 
    ...         radLim=False,
    ...         multiScale=True, 
    ...         devTable = True,
    ...         fontScale=1, 
    ...         radiusMax=[2000, 800, 1, 2000, 2500, 700], 
    ...         radTextSize="large", 
    ...         scaleTextSize="x-small", 
    ...         titleTextSize="large", 
    ...         headerTextSize="x-large", 
    ...         headerVerPad=0.08, 
    ...         color='#4299E1',
    ...         reference=["S1", "S2"],
    ...         referCol="type",
    ...         palette=['#ED8936', '#48BB78', '#F56565', '#9F7AEA',
    ...                  '#38B2AC', '#ED64A6', '#A0AEC0', 
    ...                  '#ECC94B', '#4299E1'])
    """
    
    """Version 1.0"""
    
    #copy the dataframe to avoid modifying it
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
            if self.message:
                return 'functionError, {0} '.format(self.message)
            else:
                return 'functionError, undefined function error'
    
    
    #########################Radar axis function definition############
    def radarFactory(numVars):
        """Create a radar chart with `numVars` axes.
        This function creates a RadarAxes projection and registers it.
    
        Parameters
        ----------
        numVars : int
            Number of variables for radar chart.
        """
        # calculate evenly-spaced axis angles
        theta = np.linspace(0, 2*np.pi, numVars, endpoint=False)
    
        class RadarAxes(PolarAxes):
    
            name = 'radar'
            # use 1 line segment to connect specified points
            RESOLUTION = 1
    
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # rotate plot to place the first axis at the top
                self.set_theta_zero_location('N')
    
            def fill(self, *args, closed=True, **kwargs):
                """Override fill so that line is closed by default"""
                return super().fill(closed=closed, *args, **kwargs)
    
            def plot(self, *args, **kwargs):
                """Override plot so that line is closed by default"""
                lines = super().plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)
    
            def _close_line(self, line):
                x, y = line.get_data()
                #  markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.concatenate((x, [x[0]]))
                    y = np.concatenate((y, [y[0]]))
                    line.set_data(x, y)
    
            def set_varlabels(self, labels, radSize):
                
                self.set_thetagrids(np.degrees(theta), labels, size=radSize)
    
            def _gen_axes_patch(self):
                # The Axes patch must be centered at (0.5, 0.5) 
                #and of radius 0.5
                # in axes coordinates.
                return RegularPolygon((0.5, 0.5), numVars,
                                      radius=.5, edgecolor="k")
    
            def _gen_axes_spines(self):
    
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(numVars))
                # unit_regular_polygon gives a polygon of radius 1 
                # centered at(0, 0) but we want a polygon of radius 0.5 
                # centered at (0.5, 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            
            def set_rgrids_plus(self, radTicksNum, radMax, scaleTextSize):
                #if multiple Scale is selected, 
                #to represent the grid labels in the radial axes
                #we write labels in the grid positions.
                for angle,radiusMax in zip(theta,radMax):
                    for rad in [float(x)*(1/radTicksNum) for x in 
                                range(1, radTicksNum + 1)]:
                        # change format of the grid
                        if rad*radiusMax < 1: 
                            self.text(angle, rad,
                                      "{0:.2f}".format(rad*radiusMax),
                                      alpha=0.7, 
                                      size=scaleTextSize)
                        elif rad*radiusMax < 10:
                            self.text(angle, rad,
                                      "{0:.1f}".format(rad*radiusMax),
                                      alpha=0.7, 
                                      size=scaleTextSize)
                        else :
                            self.text(angle, rad,
                                      "{0:.0f}".format(rad*radiusMax),
                                      alpha=0.7, 
                                      size=scaleTextSize)
    
        register_projection(RadarAxes)
        
        
        return theta

    ############################Kwargs#################################
    
    numPlotCols = kwargs.get("numPlotCols", False)
    radTicksNum = kwargs.get("radTicksNum", 4)
    xSize = kwargs.get("xSize", 12)
    ySize = kwargs.get("ySize", 12)
    multiScale = kwargs.get("multiScale", False)
    radLim = kwargs.get("radLim", False)
    radiusMax = kwargs.get("radiusMax", False)
    fontScale = kwargs.get("fontScale", 1)
    radTextSize = kwargs.get("radTextSize", "large")
    scaleTextSize = kwargs.get("scaleTextSize", "small")
    titleTextSize = kwargs.get("titleTextSize", "large")
    headerTextSize = kwargs.get("headerTextSize", "x-large")
    headerVerPad = kwargs.get("headerVerPad", 0.08)
    color = kwargs.get("color", False)
    reference = kwargs.get("reference", False)
    referCol = kwargs.get("referCol", False)
    referColor = kwargs.get("referColor", False)
    devTable = kwargs.get("devTable", False)
    palette = kwargs.get("palette", "deep")
    fileName = kwargs.get("fileName", graphHeader)
    legTitle = kwargs.get("legTitle", "Ref. Deviation")
    
    ############################Parameter Validation###################
    #Check for type match and particularities in every param 
    #not neccesary but helps to inform the user
    if not isinstance(df, pd.DataFrame):
        raise functionError("df is not a pandas dataframe")
    
    if not titleCol in df.columns.values.tolist():
        raise functionError(
                         "{} is not a df column header name.".format(titleCol))
        
    if not referCol in df.columns.values.tolist():
        raise functionError(
                         "{} is not a df column header name.".format(referCol))    
    
    if len(radiusCol) < 3:
        raise functionError("not enough "
                         "variables in radiusCols, choose at least 3")
    
    for radius in radiusCol:
        if not radius in df.columns.values.tolist():
            raise functionError("{}".format(radius) +
                             " is not a df column header name.")
    
    if not isinstance(graphHeader, str):
        try:
            graphHeader = str(graphHeader)
        except:
            raise functionError("graphHeader is not a string.")
    
    if not isinstance(numPlotCols, int):
        raise functionError("numPlotCols is not an integer.")

    if not isinstance(radTicksNum, int):
        raise functionError("radTicksNum is not an integer.")
    
    if not isinstance(xSize, (int, float)):
        raise functionError("xSize is not a float or a integer.")

    if not isinstance(ySize, (int, float)):
        raise functionError("ySize is not a float or a integer.")
    
    if not isinstance(multiScale, bool):
        raise functionError("multiScale is not a boolean.")
    
    if multiScale:
        if radiusMax:
            for radius in radiusMax:
                if not isinstance(radLim, (int, float)):
                    raise functionError("radLim is"
                                     " not a float or a integer.")
    else:
        if radLim:
            if not isinstance(radLim, (int, float)):
                raise functionError("radLim is not a float or a integer.")

    if not isinstance(fontScale, (int, float)):
        raise functionError("fontScale is not a float or a integer.")
    
    for textsize in (radTextSize, radTextSize, titleTextSize, headerTextSize):
        if not textsize in ('xx-small', 'x-small', 'small', 'medium',
                            'large', 'x-large', 'xx-large'):
            raise functionError("textsize is not a valid"
                             " text size value, valid values are: "  
                             "'xx-small', 'x-small', 'small', 'medium',"
                             " 'large', 'x-large', 'xx-large'")
    
    if not isinstance(headerVerPad, (int, float)):
        raise functionError("headerVerPad is not a float or a integer.")
    
    if reference:
        if isinstance(reference, (str, int)):
            reference = [reference,] 
    
    for ref in reference: 
        if not ref in df[titleCol].tolist():
            raise functionError("reference value {}".format(ref) + 
                             " not found in dataFrame" + 
                             " column {}".format(titleCol))
        
    if referColor:
        if len(reference) > len(referColor):
            raise functionError("not enough elements in referColor.")
    
    ############################Initial settings#######################
    extraArtistList = []
    
    # For radius limits representation 
    # we use the greater closest 10^n or (10^n)/2 or (10^n)/5
    if not radLim: 
        radLim = 10 ** math.ceil(math.log10(df[radiusCol].max().max()*1.01))
        if radLim/5 > df[radiusCol].max().max()*1.01:
            radLim = radLim/5
        elif radLim/2 > df[radiusCol].max().max()*1.01:
            radLim = radLim/2
        
    if multiScale:
        radLim = 1 #if multiscale we normalize to 1 our scale and value
        if not radiusMax:
            radiusMax = []
            for radius in radiusCol:
                
                radmax = 10 ** math.ceil(math.log10(df[radius].max()*1.01))
                if radmax/5 > df[radius].max()*1.01:
                    radmax = radmax/5
                elif radmax/2 > df[radius].max()*1.01:
                    radmax = radmax/2
                
                radiusMax.append(radmax)
                
    # Set color palette and 
    # get a main color for representation if not provided.
    sns.set(style="whitegrid", font_scale=fontScale)
    sns.set_palette(palette)
    
    if color is False:
        color = list(sns.color_palette().as_hex())[0]

    # Split the data in references and data 
    # and generete color for references.
    if reference:
        dfRef = pd.DataFrame()
        for ref in reference:
            dfRef = pd.concat([dfRef,df[df[titleCol] == ref]])
            df = df[df[titleCol] != ref]
            df.reset_index(drop=True, inplace=True)
        
        dfRef.reset_index(drop=True, inplace=True)
    
        if not referColor:
            stdColorlist = list(sns.color_palette().as_hex())
            # to avoid repeating the main color
            if color in stdColorlist: 
                stdColorlist.remove(color) 
            
            referColor = stdColorlist[:len(dfRef[titleCol])]
    
    #numPlotCols if not specified forces a square layout.
    if not numPlotCols:
        numPlotCols = int(math.sqrt(len(df[titleCol])))
        
    #the number of plot rows is calculated to fit all the plots
    if len(df[titleCol]) == 0:
        raise functionError("No data in the dataframe")
        
    numRows = int(np.ceil(len(df[titleCol])/numPlotCols))
    
    theta = radarFactory(len(radiusCol)) 
    
    #######################Figure creation#############################
    fig, axes = plt.subplots(figsize=(xSize, ySize), nrows=numRows, 
                             ncols=numPlotCols,
                             subplot_kw=dict(projection='radar'))
    
    fig.subplots_adjust(wspace=0.5, hspace=0.6,
                        top=(1 - headerVerPad), bottom=0.05)

    # For each axes plotted, if there is a row with data plot it
    #if not, empty the lables and ticks
    try: #to avoid errors when only an ax is made
        rows = range(0, len(axes.flat))
    except:
        rows = [0,]
    for row in rows:
        try:
            ax = axes.flat[row]
        except:
            ax = axes
        if row in range(0, len(df[titleCol])):
            ax.set_ylim(0, radLim)
            
            if multiScale:
                ax.set_rgrids_plus(radTicksNum, radiusMax,
                                   scaleTextSize)
                ax.set_rgrids(
                        [float(x)*(radLim/radTicksNum) 
                        for x in range(1, radTicksNum + 1)]
                        ,[])
            else:
                ax.set_rgrids(
                        [float(x)*(radLim/radTicksNum) 
                        for x in range(1, radTicksNum + 1)]
                        )
            
            ax.set_title(df[titleCol][row], weight='bold',
                         position=(0.5, 1),
                         horizontalalignment='center', 
                         verticalalignment='center',
                         size=titleTextSize)
            
            ###finding the reference to represent
            #if a reference colum exist use that single value
            #if not use all the values in the reference param
            referList = [] 
            if referCol:
                referList.append(df[referCol][row]) 
            else:
                for ref in reference:
                    referList.append(ref)
                    
            #representation
            if multiScale is False:
                #Create a list with the data in the order of radiusCols
                caseData = [] 
                for col in radiusCol:
                    caseData.append(df[col][row])
                    
                ax.plot(theta, caseData, color, lw=2)
                ax.fill(theta, caseData, color, alpha=0.4)
                
                # if reference are used,
                # check if the reference is applicable,
                # plot it and put a legend
                refData = False
                if reference:
                    for ref_row in range(0, len(dfRef[titleCol])):
                        if dfRef[titleCol][ref_row] in referList:
                            refData = []
                            for col in radiusCol:
                                refData.append(dfRef[col][ref_row])
                            ax.plot(theta,refData,
                                    label=dfRef[titleCol][ref_row],
                                    color=referColor[ref_row], ls="--",lw=2)
                            extraArtistList.append(
                                    ax.legend(loc='upper left',
                                              bbox_to_anchor=(1.1, 0)))
            #if multiScale, reescale each variable dividing by the max
            elif multiScale is True: 
                caseData = []
                for col, radMax in zip(radiusCol, radiusMax):
                    caseData.append(df[col][row]/radMax)
                    
                ax.plot(theta, caseData, color, lw=2)
                ax.fill(theta, caseData, color, alpha=0.4)
                
                # if reference are used,
                # check if the reference is applicable,
                # plot it and put a legend
                refData = False
                if reference:
                    for ref_row in range(0, len(dfRef[titleCol])):
                        if dfRef[titleCol][ref_row] in referList:
                            refData = []
                            for col, radMax in zip(radiusCol, radiusMax):
                                refData.append(dfRef[col][ref_row]/radMax)
                            ax.plot(theta, refData,
                                    label=dfRef[titleCol][ref_row],
                                    color=referColor[ref_row], ls="--", lw=2)
                            extraArtistList.append(
                                    ax.legend(loc='upper left',
                                    bbox_to_anchor=(1.1, 0)))
            ax.set_varlabels(radiusCol, radTextSize)
            
            #Deviation table
            if devTable:
                if refData:
                    deviation = {}
                    for col, case, ref in zip(radiusCol, caseData, refData):
                        deviation[col] = "{}: {:g}%".format(
                                col,float('{:.3g}'.format(
                                                    ((case - ref) / ref)*100)))
            
                    devStr = '\n'.join([deviation[col] for col in deviation])
                    devStr = legTitle+"\n" + devStr
                    extraArtistList.append(
                            ax.text(1.1, 0, devStr, 
                                    transform=ax.transAxes, va="bottom", 
                                    ha="left",
                                    bbox={'fc': 'w', 
                                          "boxstyle":"round,pad=0.3", 
                                          "ec": "grey"}))
        #if all the data was already represented, hide axis and grid
        else:
            ax.grid(False)
            ax.axis('off')
    
    header=fig.text(0.5, 1.01, graphHeader,
                    horizontalalignment='center',
                    va="bottom",
                    weight='bold',size=headerTextSize)
    extraArtistList.append(header)
    
    ############Plot saving############################################
    if save is True:
        #Path to save in, path of the caller of the function
        fullpath = os.path.abspath(sys.modules['__main__'].__file__)
        path, callerfilename = os.path.split(fullpath)
        
        # To create the file name, remove non alphanumeric chars
        filename = re.sub(r'\W+', '', fileName.title())
        
        plt.savefig(pathlib.Path(path,filename).with_suffix(".png"),
                    bbox_extra_artists=extraArtistList, 
                    bbox_inches='tight',dpi=300)
    
    plt.show()
    return fig

if __name__ == '__main__':
    pass
