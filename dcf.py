
# import numpy as np
#import pandas as pd 
#import matplotlib.pyplot as plt

def growth_value(FCF_t0,g,r,n):
    r = r/100
    g = g/100
    value=0
    t=0
    for k in range(n):
        tk = ((FCF_t0*((1+g)**(k))))/((1+r)**(k))
        t +=  tk
        value =t
    global terminal_FCF,g1,r1,n1
    terminal_FCF = tk  
    r1 = r 
    n1 = n 
    return t

def perpetuity_value(tg, tr, g):
        g = g/100 #move this to EV function, maybe wrap it into a function of its own so that its clear whats happening (are we just dividing by a 100 or anaylsing a 100 companies)
        tg = tg/100
        tr = tr/100
        FCF_n = terminal_FCF
        terminal_value = (FCF_n * (1+g))/((tr-tg))
        discounted_TV = terminal_value / (1+r1)**n1
        return discounted_TV

def enterprise_value(FCF_t0, g,r,n,tg,tr):
    # if we just call growth_value(FCF_t0,g,r,n) then we are calling the function itself rather than its output. 
    return growth_value(FCF_t0,g,r,n) + perpetuity_value(tg, tr, g)


def share_value(enterprise_value,cash,debt,sharecount):
        # enterprise_value1 = enterprise_value --> not neccessary in this case,quite confusing too. We are just reassigning variables. Usually you'd do it for copy like reasons 
        return ((enterprise_value+cash-debt)/(sharecount))

