# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:36:30 2020

@author: Juani
"""

class MarketData():
    """
    This class is the container for all the market data objects. A Named market data object should be provided for look up.
    """
    def __init__( self , *args, **kwargs ):
        self._stocks = kwargs['stocks'] if 'stocks' in kwargs else {}
        self._vol_surfaces = kwargs['vol_surfaces'] if 'vol_surfaces' in kwargs else {}
        self._zero_curves = kwargs['zero_curves'] if 'zero_curves' in kwargs else {}
    
    def add_stock( self, stock ):
        if not stock.name:
            raise Exception('Name should be provided')
        self._stocks[stock.name] = stock
        
    def add_volatility_surface( self, vol_surface ):
        if not vol_surface.name:
            raise Exception('Name should be provided')
        self._vol_surfaces[vol_surface.name] = vol_surface
        
    def add_zero_curve( self, zero_curve ):
        if not zero_curve.name:
            raise Exception('Name should be provided')
        self._zero_curves[zero_curve.name] = zero_curve
        
    def get_vol_surface( self, name ):
        return self._vol_surfaces[name]
    
    def get_stock( self, name ):
        return self._stocks[name]
    
    def get_zero_curve( self, name ):
        return self._zero_curves[name]
        