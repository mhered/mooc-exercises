#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

# Lateral control

# TODO: write the PID controller using what you've learned in the previous activities

# Note: y_hat will be calculated based on your DeltaPhi() and poseEstimate() functions written previously 

def PIDController(
    v_0, # assume given (by the scenario)
    y_ref, # assume given (by the scenario)
    y_hat, # assume given (by the odometry)
    prev_e_y, # assume given (by the previous iteration of this function)
    prev_int_y, # assume given (by the previous iteration of this function)
    delta_t): # assume given (by the simulator)
    """
    Args:
        v_0 (:double:) linear Duckiebot speed.
        y_ref (:double:) reference lateral pose
        y_hat (:double:) the current estimated pose along y.
        prev_e_y (:double:) tracking error at previous iteration.
        prev_int_y (:double:) previous integral error term.
        delta_t (:double:) time interval since last call.
    returns:
        v_0 (:double:) linear velocity of the Duckiebot 
        omega (:double:) angular velocity of the Duckiebot
        e_y (:double:) current tracking error (automatically becomes prev_e_y at next iteration).
        e_int_y (:double:) current integral error (automatically becomes prev_int_y at next iteration).
    """
    
    # TODO: these are random values, you have to implement your own PID controller in here
    # update current tracking error = reference - current
    
    # y_margin = 0.05 # trick to avoid crash
    # e_y = (y_ref + y_margin) - y_hat 

    e_y = y_ref - y_hat 

    
    # update integral error = previous integral error + current error x time step
    e_int_y = prev_int_y + e_y * delta_t
    
    # anti-windup - keep integral error from growing too much: -LIM < e_int_y < LIM 
    LIM = 200 # this value from SOLUTION of PID 5 exercise
    e_int_y = max(min(e_int_y,LIM),-LIM)
    
    # update derivative term = delta error / time step
    e_der_y = (e_y - prev_e_y) / delta_t
   
    """
    # PID constants
    kp = 5
    ki = 0.05
    kd = 120
    """
    
    kp = 4
    ki = 0
    kd = 90
    
    # update omega
    omega = kp * e_y + kd * e_der_y + ki * e_int_y 
    # int("e: ",e_y, "  e_int: ",e_int_y, "  e_der: ",e_der_y, "  w: ",omega)
    
    return [v_0, omega], e_y, e_int_y

