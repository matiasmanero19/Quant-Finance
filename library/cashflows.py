# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:18:16 2020

@author: juani
"""

class CashflowsList():
    """
    This class is the container for all the cashflows of a derivative
    """
    def __init__( self , *args, **kwargs ):
        self._cashflows = kwargs['cashflows'] if 'cashflows' in kwargs else []
        
    def calculate_npvs( self, pricer, time ):
        """
        This function computes the npv of all the cashflows.
        """
        for cashflow in self._cashflows:
            cashflow.calculate_npv( pricer = pricer, time = time )
        
    def npv( self ):
        """
        This function computes the sum of npvs of all the cashflows once they have been computed.
        """
        cashflows_npv = [cashflow.npv() for cashflow in self._cashflows]
        return float(sum(cashflows_npv))
        
    def add_cashflow( self, cashflow ):
        """
        This function add a new cashflow. It is used by the option to build its schedule of cashflows.
        """
        self._cashflows.append(cashflow)
        

class AbstractCashflow():
    """
    This class defines the interface for all the cashflows.
    """
    def __init__( self , *args, **kwargs ):
        self._npv = None
        self.maturity = kwargs['maturity']
        self.payoff = kwargs['payoff']
        
    def calculate_npv( self, time, pricer ):
        """
        This function computes the npv of the cashflow.
        """
        raise Exception('It must be implemented in a subclass')
    
    def npv( self ):
        """
        This function returns the npv once it has been computed.
        """
        return self._npv

    def strike( self ):
        return self.payoff.strike
    
    def underlier_name( self ):
        return self.payoff.underlier_name
    
    def call_put_factor( self ):
        return self.payoff.call_put_factor()    
    
    def as_cashflows_list( self ):
        """
        This function returns a CashflowList instance with a single cashflow.
        """
        cashflows = CashflowsList()
        cashflows.add_cashflow(self)
        return cashflows


class UnknownCashflow( AbstractCashflow ):
    
    def calculate_npv( self, pricer, time ):
        """
        This function computes the npv of the cashflow using a pricer.
        """
        npv = pricer.npv_cashflow( cashflow = self, time = time )
        self._npv = float(npv)
                
            
class KnownCashflow( AbstractCashflow ):
    
    def get_underlier_price( self, pricer, time ):
        underlier = pricer.market_data.get_stock(self.underlier_name()) 
        return underlier.get_price(time)
        
    def calculate_npv( self, pricer, time ):
        """
        This function computes the value of the cashflow at maturity.
        """
        npv = self.payoff.value_for( self.get_underlier_price( pricer, time ) )
        self._npv = npv
    