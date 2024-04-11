# this code was written by Daniel and (heavily) inspired by Aayush
# import sleep from time
import time
import pygame as pg
# make list of frames
frames = ['frame1', 'frame2', 'frame3', 'frame4']
# make index for frames to cycle
idx = 0
# start loop
while True:
    # delay for 1 second
    time.sleep(1)
    # print the frame # from idx
    print(frames[idx])
    # idx + 1
    idx = (idx + 1) % len(frames)