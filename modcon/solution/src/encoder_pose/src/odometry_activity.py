#!/usr/bin/env python
# coding: utf-8

# In[10]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

#TODO: write a correct function

def DeltaPhi(encoder_msg, prev_ticks):
    """
        Args:
            encoder_msg: ROS encoder message (ENUM)
            prev_ticks: Previous tick count from the encoders (int)
        Return:
            rotation_wheel: Rotation of the wheel in radians (double)
            ticks: current number of ticks (int)
    """    
  
    # TODO: these are random values, you have to implement your own solution in here
    # ticks = prev_ticks + int(np.random.uniform(0, 10))     
    # delta_phi = np.random.random()
    
    # MH: SOLUTION
    
    N_tot = encoder_msg.resolution # number of ticks per wheel revolution
    alpha = 2*np.pi / N_tot # wheel rotation per tick in radians

    ticks = encoder_msg.data # incremental count of ticks from the encoder
    delta_ticks = ticks - prev_ticks # delta ticks 
    delta_phi = delta_ticks * alpha # total rotation of left wheel 

    return delta_phi, ticks

# In[11]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your odometry function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

# TODO: write the odometry function

import numpy as np 

def poseEstimation( R, # radius of wheel (assumed identical) - this is fixed in simulation, and will be imported from your saved calibration for the physical robot
                    baseline_wheel2wheel, # distance from wheel to wheel; 2L of the theory
                    x_prev, # previous x estimate - assume given
                    y_prev, # previous y estimate - assume given
                    theta_prev, # previous orientation estimate - assume given
                    delta_phi_left, # left wheel rotation (rad)
                    delta_phi_right): # right wheel rotation (rad)
    
    """
        Calculate the current Duckiebot pose using the dead-reckoning approach.

        Returns x,y,theta current estimates:
            x_curr, y_curr, theta_curr (:double: values)
    """
    
    # TODO: these are random values, you have to implement your own solution in here
    # x_curr = np.random.random() 
    # y_curr = np.random.random() 
    # theta_curr = np.random.random()
    
    # MH: SOLUTION
    d_left = delta_phi_left * R
    d_right = delta_phi_right * R
    d_A = (d_right + d_left) / 2 # robot distance travelled in robot frame [meters]
    d_theta = (d_right - d_left)/baseline_wheel2wheel # [radians]

    x_curr = x_prev + d_A * np.cos(theta_prev)
    y_curr= y_prev + d_A * np.sin(theta_prev)
    theta_curr = theta_prev + d_theta
    
    
    return x_curr, y_curr, theta_curr
