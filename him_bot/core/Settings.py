"""
    Himanshu Gwalani
    2017ucp1356
"""
from core.color import *
global path,history,running_module,name,headless_browser,visible_browser
global previous
                   
update_history  = lambda h:history.append(h)
update_previous = lambda:previous.append(running_module)

name = W+underline+"him's bot"+end
def add_module(p): global name;name = W+underline+"him's bot"+end+ W+" Module("+R+p+W+")"+end # Fuck lambda
def reset_name() : global name;name = W+underline+"him's bot"+end

path             = None            
running_module   = False           
headless_browser = False           
visible_browser  = False           
previous   = []                    
history    = [] 