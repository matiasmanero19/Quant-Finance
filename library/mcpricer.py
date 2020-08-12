# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 12:45:23 2020

@author: Juani
"""

import numpy as np
from library.year_fractions import Actual360
from library.base import AbstractPricer

    
class SimpleMonteCarloPricer( AbstractPricer ):
    """
    This class implements the a simple MonteCarlo pricer.
    """
    def initialize_model( self, model ):
        self.model = model
        

    def initialize_pricer( self, parameters ):        
        if 'samples' in parameters:
            self.samples = parameters['samples']
        else:
            raise Exception('number of samples not specified')
            
        super().initialize_pricer(parameters)
    
    
    def npv_cashflow( self, cashflow, time ):
        """
        This is the function that calculates the npv of each cashflow
        """     
        T = cashflow.maturity
        year_fraction_tT = Actual360.year_fraction_for(time,T)
        
        underlier_name = cashflow.underlier_name()
        stock = self.market_data.get_stock(underlier_name)
        S_t = stock.get_price(time)
          
        w_samples = np.random.normal(0, 1, self.samples)
        S_T_samples = self.model.S_T_samples( S_t, year_fraction_tT, w_samples )

#        this is not efficient        
#        sample_payoffs = [cashflow.payoff().value_for(S_T) for S_T in S_T_samples]
        
        sample_payoffs = cashflow.payoff.values_for( S_T_samples )
        
        average_payoff = np.sum(sample_payoffs) / self.samples
        
        df = self.zero_curve.df(time, T)
        
        return df * average_payoff
     
    

    
    
    
    
    
    
    
    
    
    
    
    