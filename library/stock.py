from library.base import AbstractMarketObject


class Stock( AbstractMarketObject ):
    """ 
     This is the class that represents stocks.
    """   
    def add_close_price( self, time, price ):
        self.add_close( time, price )
    
    def get_price( self, time ):
        return self.get_close( time )
    
    def shift_price(self, time, shift):
        self.shift_close(time, shift)
        
    def plot( self, t1, t2 ):
        self.time_series_between_times(t1,t2).plot()
        
        
                
            
        
        

