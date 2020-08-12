from library.base import AbstractYearFraction 

    
class Actual365( AbstractYearFraction ):
    """ 
     This is the class for the object that computes year fractions using Actual/365 convention.
    """   
    @classmethod
    def year_fraction_for( cls, t0, t1 ):
        """
        This is the function that returns ths year fraction between t1 and t2 
        """  
        actual_diff = t1 - t0
        return actual_diff.days / 365
    

class Actual360( AbstractYearFraction ):
    """ 
     This is a class for the object that computes year fractions using Actual/360 convention.
    """   
    @classmethod
    def year_fraction_for( cls, t0, t1 ):
        """
        This is the function that returns ths year fraction between t1 and t2 
        """  
        actual_diff = t1 - t0
        return actual_diff.days / 360