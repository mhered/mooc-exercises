#!/usr/bin/env python
# coding: utf-8

# In[1]:


def DT_TOKEN():
    # todo change this to your duckietown token
    #MH: done
    dt_token = "dt1-3nT8KSoxVh4Mf7PxTXk9sKZcmV6hpzdyQsdfMm3Ue7XVqgg-43dzqWFnWd8KBa1yev1g3UKnzVxZkkTbfQfWaw2WuwuD28RjssMoU8SqDonvxd6YWy"
    return dt_token

def MODEL_NAME():
    # todo change this to your model's name that you used to upload it on google colab.
    # if you didn't change it, it should be "yolov5"
    return "yolov5"

# In[2]:


def NUMBER_FRAMES_SKIPPED():
    # todo change this number to drop more frames
    # (must be a positive integer)
    # MH: was "return 0", changed to return 2 meaning I run once every 3 frames
    return 0

# In[3]:


# `class` is the class of a prediction
def filter_by_classes(clas):
    # Right now, this returns True for every object's class
    # Change this to only return True for duckies!
    # In other words, returning False means that this prediction is ignored.
    
    # MH: was "return True"
    if clas == 0:
        print("\n clas: ", clas, " is duckie, considered\n")
        return True
    else:
        print("\n clas: ", clas, " is NOT a duckie, ignored\n")
        return False

# In[4]:


# `scor` is the confidence score of a prediction
def filter_by_scores(scor):
    # Right now, this returns True for every object's confidence
    # Change this to filter the scores, or not at all
    # (returning True for all of them might be the right thing to do!)
    if scor > 0.4:
        print("\n scor: ", scor, " is high, considered\n")
        return True
    else:
        print("\n scor: ", scor, " is too low, ignored\n")
        return False

# In[7]:


# `bbox` is the bounding box of a prediction, in xyxy format
# So it is of the shape (leftmost x pixel, topmost y pixel, rightmost x pixel, bottommost y pixel)
def filter_by_bboxes(bbox):
    # Like in the other cases, return False if the bbox should not be considered.

    # MH: consider only duckies that are close
    IMAGE_SIZE = 416
    print("\n bbox: ",bbox,"\n")

    if bbox[3]>.60*IMAGE_SIZE:
        print("In lower 40% of image (Close!): considered")
        return True
    elif (bbox[3]-bbox[1])>.20*IMAGE_SIZE: 
        print("Taller than 20% of image (Close!): considered")
        return True
    else:
        print("Too high or too small in image (Far!): ignored")
        return False
