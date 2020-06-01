#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u64053
"""

import sqlite3

def stdColor(colorCod, series=False, color=False, reverse=False):
    r"""Function to generate a color or color palette 
    from the standart TEASP color database 
    using the color code chosen.
    
    If a color and a series is selected the color code is given. 
    If only a series is selected, 
    all the colors in that serie are given in order: 
    ["INDIGO", "ORANGE", "GREEN", "RED", "PURPLE", "TEAL", "PINK",
    "GRAY", "YELLOW", "BLUE"]
    
    If only a color is selected, a monocrome palette is given, 
    from light to dark.
    
    Parameters
    ----------
    colorCod : string. 
        Color code to use, valid inputs "hex","dec","rgb".
        
    series : integer, optional.
        from lighter to darker, color brightness. 
        Valid inputs: [100, 200, 300, 400, 500, 600, 700, 800, 900]
        
    color : string, optional.
        Name of the color to select. 
        Valid values ["INDIGO", "ORANGE", "GREEN", "RED", 
        "PURPLE", "TEAL", "PINK", "GRAY", "YELLOW", "BLUE"]
        
    reverse : boolean, optional.
        If True reverse the order of the color palette.
        
    Returns
    -------
    colorOut : string or list of strings.
        Color or list with the colors in the desired format.
        
    Examples
    --------
    
    Create a list of hex or RGB values of the color series 500:
        
    >>> listHex = stdColor('hex', series=500, reverse=False)
    >>> listRGB = stdColor('rgb', series=500, reverse=False)
    
    Create a list of decimal values of shades of Blue:
        
    >>> stdColor('dec', color="BLUE", reverse=False)
    
    Obtain the RGB color code of the Blue of the series 500:
        
    >>> blueRGB = stdColor('rgb', color="BLUE", series=500)
   
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
                return 'functionError has been raised'

    #Parameters
    dbPath = "/home/IntercambiosSHM/U64053/EFA_Master_DB.db3"
    table = "COLOR_PALETTE"
    order = ["INDIGO", "ORANGE", "GREEN", "RED", "PURPLE", "TEAL", "PINK", 
             "GRAY", "YELLOW", "BLUE"] #list to order the colors.
    
    #dict to relate param with the table columns
    columChoice = {'hex':'HEX', 'dec':'DECIMAL', 'rgb':'R, G, B'} 

    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    
    #choose the column to ask for depending to the color code
    try:
        col = columChoice[colorCod]
    except:
        raise functionError("param is not a valid value."
                         " Valid values are 'hex', 'dec','rgb'.")
    
    if series and color:
        # Single color request
        query = "SELECT {} FROM {} WHERE NAME = ? AND SERIES = ?".format(
                                                                    col, table)
        consulta = cur.execute(query, (color, series)).fetchone()
        
        if consulta is None:
            raise functionError("No register matching"
                             " your request was found")
        if colorCod == 'hex':
            return('#' + consulta[0])
        elif colorCod == 'dec':
            return(consulta[0])
        elif colorCod == 'rgb': # rgb normalized to [0,1]
            return([x/255 for x in consulta])
        
    elif color:
        # Monocrome scale request
        criteria = "color" #used to display info error.
        query = "SELECT {} FROM {} WHERE NAME = ?".format(col, table)
        consulta = cur.execute(query, (color,)).fetchall()
        
    elif series:
        # Full palette request
        criteria = "serie" #used to display info error.
        query = "SELECT NAME,{} FROM {} WHERE SERIES = ?".format(col, table)
        consulta = cur.execute(query, (series,)).fetchall()
        #in case of wanting a multicolor palette 
        #we order it in the typical seaborn color order.
        #we use a try to avoid a failure in case 
        #the name of the colors in the database changes
        #in that case just leave the colors in the order of the database.
        try:
            consulta.sort(key=lambda x: order.index(x[0]))
        except:
            pass
        
        #Remove the NAME value from "consulta"
        if colorCod == 'rgb':
            consulta = [[x[1], x[2], x[3]] for x in consulta]
        else:
            consulta = [[x[1],] for x in consulta]
        
    elif series is False and color is False:
        raise functionError("at least one of series"
                            " or color need to be specified.")

    if reverse:
        consulta.reverse()
    
    colorOut = []
    if colorCod == 'hex':
        for color in consulta:
            colorOut.append("#" + color[0]) 

    elif colorCod == 'dec':
        for color in consulta:
            colorOut.append(color[0]) 
            
    elif colorCod == 'rgb': # rgb normalized to [0,1]
        for color in consulta:
            colorOut.append([x/255 for x in color])   
    
    if colorOut == []:
        raise functionError("No register matching"
                            " your {} was found".format(criteria))
    return colorOut

if __name__ == "__main__":
    pass