# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:48:25 2020

@author: Juani
"""

from math import log, sqrt
from scipy.stats import norm
from library.year_fractions import Actual360
from library.base import AbstractPricer


class BlackScholesFormulaPricer( AbstractPricer ):
    """
    This class implements the Black Scholes Formula for call/put options.
    """
    def initialize_model( self, model ):
        """ Model is already Black Scholes"""
        pass

    def initialize_pricer( self, parameters ):             
        if 'underlier_vol' in parameters:
            implied_vol_name = parameters['underlier_vol']
            self.implied_vol = self.market_data.get_vol_surface(implied_vol_name)
        else:
            raise Exception('underlier_vol not specified')
        
        super().initialize_pricer(parameters)
   
    def npv_cashflow( self, cashflow, time ):
        """
        This is the function that calculates the npv of each cashflow
        """
        T = cashflow.maturity
        K = cashflow.strike()
        year_fraction_tT = Actual360.year_fraction_for(time,T)
       
        r = self.zero_curve.get_zero_rate(time)
        
        underlier_name = cashflow.underlier_name()
        stock = self.market_data.get_stock(underlier_name)
        S_t = stock.get_price(time)
        
        v = self.implied_vol.get_volatility(time = time, strike = K, maturity = T)
        d_plus  = ( log( S_t/K ) + ( r + v**2 / 2 ) * year_fraction_tT ) / ( v * sqrt( year_fraction_tT ) )  
        d_minus = ( log( S_t/K ) + ( r - v**2 / 2 ) * year_fraction_tT ) / ( v * sqrt( year_fraction_tT ) ) 
        
        f = cashflow.call_put_factor()
        df = self.zero_curve.df(time, T)
    
        return f * ( norm.cdf(f * d_plus) * S_t - norm.cdf(f * d_minus) * K * df )

    
    
        
        
        
            
        
        
    