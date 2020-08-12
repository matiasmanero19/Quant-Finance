# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:06:11 2020

@author: Juani
"""

from library.base import AbstractVolatilitySurface


class FlatVolatilitySurface( AbstractVolatilitySurface ):
    """ 
    This class represents a flat volatility surface. There is no dependency on strikes and maturities. It represents the 
    implied volatility of the Black-Scholes model. 
    """
    
    def add_close_volatility( self, time, strike, maturity, volatility ):
        self.add_close( time, volatility )
        
    def add_point_without_recalibration( self, time, strike, maturity, volatility ):
        raise Exception('No calibration for flat volatility surface')
        
    def get_volatility( self, time, strike, maturity ):
        return self.get_close( time )
    
    
    
    