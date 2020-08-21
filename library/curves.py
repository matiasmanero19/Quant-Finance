# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 18:55:56 2020

@author: Juani
"""

from math import exp
from library.base import AbstractZeroCurve


class FlatZeroCurve( AbstractZeroCurve ):
    """
    This class implements a flat zero curve. 
    """
    def add_close_zero_rate( self, time, zero_rate ):
        self.add_close( time, zero_rate )
        
    def add_point_without_recalibration( self, time, strike, maturity, volatility ):
        raise Exception('No calibration for flat volatility surface')
        
    def get_zero_rate( self, time ):
        """
        This function returns the constant zero rate for t. 
        """
        return self.get_close( time )
        
    def df( self, t, T ):
        """
        This function computes the discount factor for t between t and T. 
        """
        zero_rate = self.get_zero_rate(t)
        year_fraction = self.year_fraction.year_fraction_for(t,T)
        return exp( - zero_rate * year_fraction )


    