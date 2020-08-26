# -*- coding: utf-8 -*-
"""
Created on Mon May 25 12:19:45 2020

@author: Juani
"""

import pandas as pd
import datetime


class AbstractMarketObject():
    """ 
    This defines the interface for objects that are market observables. 
    
    Attributes:
        _time_series_close: It could be any object or variable that it is used by the concret class to build the object for t. 
    
    """   
    def __init__( self , *args, **kwargs ):
        self._time_series_close = kwargs['time_series'] if 'time_series' in kwargs else pd.Series()
        self._time_series_shifts = pd.Series()
        self.name = kwargs['name']  if 'name' in kwargs else pd.Series()
        self.days_rolled = datetime.timedelta(0)
    
    def add_close( self, time, close ):
        self._time_series_close[time] = close
        
    def get_close( self, time ):
        rolled_time = time + self.days_rolled
        close = self._time_series_close.asof(rolled_time)      
        return close + self._time_series_shifts.asof(rolled_time) if rolled_time in self._time_series_shifts.index.values else close
    
    def shift_close( self, time, shift ):
        self._time_series_shifts[time] = shift
        
    def unshift( self ):
        self._time_series_shifts = pd.Series()
        
    def roll( self, days ):
        self.days_rolled = days
        
    def unroll( self ):
        self.days_rolled = datetime.timedelta(0)
        
    def time_series_between_times( self, t1, t2 ):
        return self._time_series_close[t1:t2]

    def plot( self, t1, t2 ):
        raise Exception('It must be implemented in a subclass')  


class AbstractDerivativeInstrument( AbstractMarketObject ):
    """ 
    This defines the interface for objects that are derivatives. 
    """
    
    def get_cashflows( self, time ):
        """
        This function returns all the future cashflows of the derivative 
        """
        raise Exception('It must be implemented in a subclass')
        
    def get_cashflows_shifted( self, time ):
        """
        This function returns all the future shifted cashflows of the derivative used for risk calculations
        """
        raise Exception('It must be implemented in a subclass')
    
    def npv( self, t, pricer ):
        """
        It returns the npv of the derivative for time t and given a pricer 
        """
        return pricer.npv(time = t)


class AbstractPricer():
    """ 
     This defines the interface for pricers. 
    """
    
    def __init__( self , *args, **kwargs ):
        self.option = kwargs['option']
        self.market_data = kwargs['market_data']
        
    def initialize_pricer( self, parameters ): 
        if 'zero_curve' in parameters:
            zero_curve_name = parameters['zero_curve']
            self.zero_curve = self.market_data.get_zero_curve(zero_curve_name)
        else:
            raise Exception('zero_curve not specified')
    
    def npv( self, time ):
        """
        It returns the sum of the npv of all the relevant cashflows from the option for time t.
        """
        cashflows = self.option.get_cashflows(time)
        cashflows.calculate_npvs( pricer = self, time = time )
        return cashflows.npv()
    
    def npv_shifted( self, time, shift ):
        """
        It returns the sum of the shifted npv of all the relevant cashflows from the option for time t.
        """
        shifted_cashflows = self.option.get_cashflows_shifted(time, shift)
        shifted_cashflows.calculate_npvs( pricer = self, time = time )
        return shifted_cashflows.npv()
    
    
    def npv_cashflow( self, cashflow, time ):
        """
        This is the function that calculates the npv of each cashflow
        """
        raise Exception('It must be implemented in a subclass')


class AbstractZeroCurve( AbstractMarketObject ):
    """ 
     This defines the interface for zero curves. 
    """
    
    def __init__( self , *args, **kwargs ):
        self.year_fraction = kwargs['year_fraction']
        super().__init__( *args, **kwargs )
    
    def df( self, t, t1 ):
        """
        This function computes the discount factor for t between t and t1
        """
        raise Exception('It must be implemented in a subclass')

    def fwd_df( self, t, t1, t2 ):
        """
        This function computes the discount factor for t between t1 and t2 
        """
        raise Exception('It must be implemented in a subclass')


class AbstractYearFraction():
    """ 
     This defines the interface for the objects that compute year fractions.
    """   
    @classmethod
    def year_fraction_for( cls, t0, t1 ):
        """
        This is the function that returns ths year fraction between t1 and t2 
        """  
        raise Exception('It must be implemented in a subclass')

class AbstractModel():
    """ 
     This defines the interface for models. 
    """
    pass


class AbstractVolatilitySurface( AbstractMarketObject ):
    """ 
     This defines the interface for volatility surfaces.
    """   
    def add_point( self, time, strike, maturity, volatility ):
        pass
        
    def add_point_without_recalibration( self, time, strike, maturity, volatility ):
        pass
    
    def calibrate( self, time ):
        pass
        
    def get_volatility( self, time, strike, maturity ):
        pass



