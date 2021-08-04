#!/usr/bin/env python3

import os
from functools import reduce

import cv2
import numpy as np
## Important - don't remove these imports even though they seem unneeded
import pyglet
from pyglet.window import key

from agent import PurePursuitPolicy
from utils import launch_env, seed, makedirs, xminyminxmaxymax2xywfnormalized, run, \
    train_test_split

from setup import find_all_boxes_and_classes



class SkipException(Exception):
    pass

# Need to change this dataset directory if not running inside docker container... TODO fix
# MH: Outside container, this corresponds to ~/mooc-exercises/object-detection/solution/duckietown_dataset/
DATASET_DIR="/jupyter_ws/solution/duckietown_dataset"
IMAGE_SIZE=416
SPLIT_PERCENTAGE=0.8 # MH: % of images saved in train vs val folders


npz_index = 0 # counter for image names

def save_npz(img, seg, boxes, classes):
    global npz_index

    # MH: this is the function that saves an image and writes boxes in label
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f"{DATASET_DIR}/images/{npz_index}.jpg", img)
    # MH: uncomment to save also segmented image
    # cv2.imwrite(f"{DATASET_DIR}/images/{npz_index}_seg.jpg", seg)

    boxes = np.array([xminyminxmaxymax2xywfnormalized(box, IMAGE_SIZE) for box in boxes])
    with open(f"{DATASET_DIR}/labels/{npz_index}.txt", "w") as f:
        for i in range(len(boxes)):
            f.write(f"{classes[i]} "+" ".join(map(str,boxes[i]))+"\n")

    print("MH: Saved image: ", npz_index,".jpg")
    npz_index += 1

    
    
# some setup
seed(123)
MAX_STEPS = 1000 # MH: number of images saved. Changed to 200
nb_of_steps = 0

# we iterate over several maps to get more diverse data
possible_maps = [
    "loop_pedestrians",
    "udem1",
    "loop_dyn_duckiebots",
    "zigzag_dists"
]
env_id = 0 # MH: initialize with the first type of map
env = None

while True:
    if env is not None:
        # MH: comment out next line if line 99 is commented out or it will sop early
        # (following advice from https://github.com/duckietown/mooc-exercises/issues/10)
        # env.window.close()
        
        env.close()

    if env_id >= len(possible_maps):
        env_id = env_id % len(possible_maps) # MH: cycle with env_id in the possible_maps
    env = launch_env(possible_maps[env_id])
    print("MH: Using map: ", possible_maps[env_id], "...") #MH: for debugging
    
    policy = PurePursuitPolicy(env)
    obs = env.reset()
    
    #MH:looks like this starts a while loop for collecting images in a given map
    
    inner_steps = 0 # MH: 
    
    # MH get out after MAX_STEPS 
    if nb_of_steps >= MAX_STEPS:
        break 

    while True:
        # MH: get out after MAX_STEPS of 100 inner steps
        
        if nb_of_steps >= MAX_STEPS or inner_steps > 100:
            break

        action = policy.predict(np.array(obs))

        obs, rew, done, misc = env.step(action)
        seg = env.render_obs(True)


        obs = cv2.resize(obs, (IMAGE_SIZE, IMAGE_SIZE)) # MH this is the snapshot
        seg = cv2.resize(seg, (IMAGE_SIZE, IMAGE_SIZE)) # MH this is the segmented image

        # MH: uncomment next line to see segmented images in  a window, but then comment out also line 63 
        # env.render(segment=True)

        try:
            # MH extract boxes from segmented image
            boxes, classes = find_all_boxes_and_classes(seg)
        except SkipException as e:
            print(e)
            continue

        # MH: comment out to prevent from saving the images with the boxes
        """
        for box in boxes:
            pt1 = (box[0], box[1])
            pt2 = (box[2], box[3])
            cv2.rectangle(obs, pt1, pt2, (255,0,0), 2)
        """

        save_npz(obs, seg,boxes, classes)
        
        # MH these counters appear to control how often to output images but how?
        nb_of_steps += 1
        inner_steps += 1

        if done or inner_steps % 100 == 0:
            env.reset()  # MH: every 100 inner steps or if simu finished reset the environment

    #MH: stop cycling on mapswhen MAX_STEPS reached
    if nb_of_steps >= MAX_STEPS:
        break


all_image_names = [str(idx) for idx in range(npz_index)]
train_test_split(all_image_names, SPLIT_PERCENTAGE, DATASET_DIR)

#run(f"rm -rf {DATASET_DIR}/images {DATASET_DIR}/labels")

