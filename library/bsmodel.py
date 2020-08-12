# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 17:41:53 2020

@author: Juani
"""

from math import sqrt, exp
import numpy as np
from library.base import AbstractModel

class BlackScholesModel( AbstractModel ):
    """
    Black-Scholes Model in the Risk Neutral measure
    
    Attributes:
        r(float): constant risk free rate.
        vol(float): constant local volatility.   
    """  
    def __init__( self , *args, **kwargs ):
        self.r = kwargs['rate']
        self.vol = kwargs['volatility']
    
    def dS( self, S_t, dt ):
        """
        Infinitesimal change of the stock price during dt
        """
        return self.r * S_t * dt + self.vol * S_t * np.random.normal(0, 1) * sqrt(dt)

    
    def S_T( self, S_t, tT, w ):
        """
        S(T) Change of the stock price between t and T
        """
        return S_t * exp( ( self.r - self.vol**2 / 2 ) * tT + self.vol * sqrt(tT) * w )
    
    def S_T_samples( self, S_t, tT, w_samples ):
        """
        For MonteCarlo calculation efficiency. It return an array of S(T) from an array of normal distributed values 
        """
        return S_t * np.exp( ( self.r - self.vol**2 / 2 ) * tT + self.vol * sqrt(tT) * w_samples )        #np.exp calculates the exp of each element of a list