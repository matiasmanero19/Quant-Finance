# -*- coding: utf-8 -*-
"""
Created on Mon May 25 13:20:17 2020

@author: Juani
"""

from library.base import AbstractDerivativeInstrument
from library.cashflows import CashflowsList, UnknownCashflow, KnownCashflow
import numpy as np


class StockOption( AbstractDerivativeInstrument ):
    """ 
     This is the class that represents stock options.
    """       
    def __init__( self , *args, **kwargs ):
        self.maturity = kwargs['maturity']
        self.payoff = Payoff.get_payoff(   
                                            payoff_name = kwargs['payoff_name'], 
                                            strike = kwargs['strike'],
                                            underlier_name = kwargs['underlier_name']                
                                        )
        
    def get_cashflows( self, time ):
        """
        This function returns the cashflow of a stock option
        """
        if time == self.maturity:
            return KnownCashflow( maturity = self.maturity, payoff = self.payoff ).as_cashflows_list()
        elif time >= self.maturity:
            return CashflowsList()
        return UnknownCashflow( maturity = self.maturity, payoff = self.payoff ).as_cashflows_list()
        

class Payoff():
    """ 
     This is the class that represents the payoff for stock options.
    """ 
    def __init__( self , *args, **kwargs ):
        self.underlier_name = kwargs['underlier_name']
        self.strike = kwargs['strike']
    
    @classmethod
    def get_payoff( cls, payoff_name, strike, underlier_name ):

        if payoff_name == 'call':
            return CallPayoff( strike = strike, underlier_name = underlier_name )
            
        if payoff_name == 'put':
            return PutPayoff( strike = strike, underlier_name = underlier_name )
    
    def value_for( self, S ):
        """
        This function returns the payoff for underlier value S
        """
        raise Exception('It must be implemented in the subclass')
    

class CallPayoff( Payoff ):
    """ 
     This is the class that represents the payoff for call options.
    """
    def call_put_factor( self ):
        """
        This function returns the call/put factor of the BS formula.
        """
        return 1
    
    def value_for( self, S ):
        """
        This function returns the payoff of a call with stock price S
        """
        return max(S - self.strike , 0)
    
    def values_for( self, S_T_samples ):     
        """
        For MonteCarlo calculation efficiency. It return an array of payoff from an array of underlier values
        """
        samples = len(S_T_samples)
        return np.maximum( np.array( S_T_samples - self.strike ), np.zeros(samples) )
        
    
class PutPayoff( Payoff ):
    """ 
     This is the class that represents the payoff for put options.
    """    
    def call_put_factor( self ):
        """
        This function returns the call/put factor of the BS formula.
        """
        return -1  
    
    def value_for( self, S ):
        """
        This function returns the payoff of a put with stock price S
        """
        return max(self.strike - S , 0)    
    
    def values_for( self, S_T_samples ):     
        """
        For MonteCarlo calculation efficiency. It return an array of payoff from an array of underlier values
        """
        samples = len(S_T_samples)
        return np.maximum( np.array( self.strike - S_T_samples ), np.zeros(samples) )  