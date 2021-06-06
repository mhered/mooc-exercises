#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np

# Heading control

# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your PIDController function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

# TODO: write your PID function for heading control!

def PIDController(v_0, theta_ref, theta_hat, prev_e, prev_int, delta_t):
    """
    Args:
        v_0 (:double:) linear Duckiebot speed (given).
        theta_ref (:double:) reference heading pose
        theta_hat (:double:) the current estimated theta.
        prev_e (:double:) tracking error at previous iteration.
        prev_int (:double:) previous integral error term.
        delta_t (:double:) time interval since last call.
    returns:
        v_0 (:double:) linear velocity of the Duckiebot 
        omega (:double:) angular velocity of the Duckiebot
        e (:double:) current tracking error (automatically becomes prev_e_y at next iteration).
        e_int (:double:) current integral error (automatically becomes prev_int_y at next iteration).
    """
        
    # TODO: these are random values, you have to implement your own PID controller in here
    # omega = np.random.uniform(-8.0, 8.0)
    # e = np.random.random()
    # e_int = np.random.random()
    
    # MH:
    e = theta_ref - theta_hat # current tracking error = actual heading - reference
    e_int = prev_int + e * delta_t # update integral term
    
    # anti-windup - keep integral error from growing too much: -LIM < e_int < LIM 
    LIM = 2 # this value from SOLUTION
    e_int = max(min(e_int,LIM),-LIM)
    
    e_der = (e - prev_e) / delta_t # derivative term

    # PID constants
    kp = 10
    ki = 0.2
    kd = 0.2
    
    # update omega
    omega = kp * e + kd * e_der + ki * e_int 
    
    
    return [v_0, omega], e, e_int
