#!/usr/bin/env python
# coding: utf-8

# In[16]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

import cv2
import numpy as np


def get_steer_matrix_left_lane_markings(shape):
    """
        Args:
            shape: The shape of the steer matrix (tuple of ints)
        Return:
            steer_matrix_left_lane: The steering (angular rate) matrix for Braitenberg-like control 
                                    using the masked left lane markings (numpy.ndarray)
    """
    
    # steer_matrix_left_lane = np.random.rand(*shape)
    m = shape[0]
    n = shape[1]
    
    C = 0
    A = (3*n)/4 - C
    B = (3*n)/(4*m)
        
    steer_matrix_left_lane = np.zeros(shape)

    for i in range(0,m):
        for j in range(0,n):
            if j > (A - B * i): 
                steer_matrix_left_lane[i,j] = -1
    """
    steer_matrix_left_lane = np.zeros(shape)
    steer_matrix_left_lane[:,int(2/5*n):n]=-1
    """
    return steer_matrix_left_lane

# In[17]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK


def get_steer_matrix_right_lane_markings(shape):
    """
        Args:
            shape: The shape of the steer matrix (tuple of ints)
        Return:
            steer_matrix_right_lane: The steering (angular rate) matrix for Braitenberg-like control 
                                     using the masked right lane markings (numpy.ndarray)
    """
    
    # steer_matrix_right_lane = np.random.rand(*shape)
    m = shape[0]
    n = shape[1]
    
    C = 0
    A = n/4 + C
    B = (3*n)/(4*m)
    
    steer_matrix_right_lane = np.zeros(shape)

    for i in range(0,m):
        for j in range(0,n):
            if j < (A + B*i): 
                steer_matrix_right_lane[i,j] = 1
    """
    steer_matrix_right_lane = np.zeros(shape)
    steer_matrix_right_lane[:,0:int(3/5*n)]= 1
    """
    
    return steer_matrix_right_lane

# In[19]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

import cv2
import numpy as np


def detect_lane_markings(image):
    """
        Args:
            image: An image from the robot's camera in the BGR color space (numpy.ndarray)
        Return:
            left_masked_img:   Masked image for the dashed-yellow line (numpy.ndarray)
            right_masked_img:  Masked image for the solid-white line (numpy.ndarray)
    """
    
    # Most of our operations will be performed on the grayscale version
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the image to HSV for color-based filtering
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, w = image_gray.shape
    # mask_left_edge = np.random.rand(h, w)
    # mask_right_edge = np.random.rand(h, w)
    
    # 1) mask_ground
    mask_ground = np.ones((h,w), dtype=np.uint8)
    horizon = 115 # MH: adjusted manually 170 for real, 115 for simu images
    mask_ground[0:horizon, :] = 0
    
    # 2) mask_left & mask_right
    fifth_width = int(w/5) # MH: arbitrarily 3/5 of the width either side
    mask_right = np.ones((h,w), dtype=np.uint8)
    mask_right[:,0:2*fifth_width] = 0
    mask_left = np.ones((h,w), dtype=np.uint8)
    mask_left[:,3*fifth_width:w + 1] = 0

    # 3) Calculate gradients
    #    3.1) Smooth image with a Gaussian filter
    SIGMA = 1 # MH: 4 for real images, 1 for simu
    image_smoothed = cv2.GaussianBlur(image_gray,(0,0), SIGMA)

    #    3.2) Find gradients with Sobel filters
    sobelx = cv2.Sobel(image_smoothed,cv2.CV_64F,1,0)
    sobely = cv2.Sobel(image_smoothed,cv2.CV_64F,0,1)

    # 4) mask_sobelx_pos, mask_sobelx_neg & mask_sobely_neg 
    #    Generate masks that identifies pixels based on the sign of their x-derivative and y-derivative
    mask_sobelx_pos = np.uint8(sobelx > 0)
    mask_sobelx_neg = np.uint8(sobelx < 0)
    mask_sobely_neg = np.uint8(sobely < 0)
    # mask_sobely_pos = (sobely > 0)
    
    # 5) mask_mag
    Gmag = np.sqrt(sobelx*sobelx + sobely*sobely)
    THRESHOLD = 40 # MH: 30 for real images, 40 for simu
    mask_mag = np.uint8(Gmag > THRESHOLD)

    # 6) mask_yellow & mask_white
    SCALES = [.5,2.55,2.55] # MH: to scale from HSV picker to OpenCV scale

    white_lower_hsv = np.asarray(np.array([0, 0, 35]) * SCALES, dtype=np.int)
    white_upper_hsv = np.asarray(np.array([260, 20, 105]) * SCALES, dtype=np.int)
    yellow_lower_hsv = np.asarray(np.array([40, 25, 45]) * SCALES, dtype=np.int) # MH: [40, 45, 45] for real images, [40, 25, 45] for simu
    yellow_upper_hsv = np.asarray(np.array([60, 105, 90]) * SCALES, dtype=np.int)

    mask_white = np.uint8(cv2.inRange(image_hsv, white_lower_hsv, white_upper_hsv))
    mask_yellow = np.uint8(cv2.inRange(image_hsv, yellow_lower_hsv, yellow_upper_hsv))

    # Complete set of masks
    mask_left_edge = mask_ground * mask_left * mask_mag * mask_sobelx_neg * mask_sobely_neg * mask_yellow
    mask_right_edge = mask_ground * mask_right * mask_mag * mask_sobelx_pos * mask_sobely_neg * mask_white
    
    return (mask_left_edge, mask_right_edge)
