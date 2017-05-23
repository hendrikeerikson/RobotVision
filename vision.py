import cv2
from copy import deepcopy
from constants import *
import numpy as np


def biggest_p(points):
    floor = np.asarray(points).transpose()
    x = floor[0]
    y = floor[1]

    mean = np.mean(y)
    deviation = np.std(y)

    # find the bar where the edge of the floor is furthest away but is in the deviation roof
    p_x = np.inf
    p_y = np.inf

    for i, val in enumerate(y):
        if abs(val - mean) < DEV_ROOF * deviation:
            if val < p_y:
                p_y = val
                p_x = BAR_SIZE * i

    return int(p_x), int(p_y)


def find_dir(frame):
    floor = []

    # reshape and flip
    frame = frame.reshape((HEIGHT, WIDTH, 3))
    frame = cv2.flip(frame, 0)

    # keep a copy of the original color image
    original = deepcopy(frame)

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to gray scale
    frame = cv2.bilateralFilter(frame, 8, 25, 25)  # blur to reduce noise

    edges = cv2.Canny(frame, 50, 100)  # returns an image with edges only

    # walk from bottom of the screen upwards until you find a line
    for x in range(0, WIDTH - 1, BAR_SIZE):
        for y in range(HEIGHT - 5, 0, -1):
            if edges.item(y, x) == 255:
                floor.append((x, y))
                break

        # if no line was found, append the top of the screen
        else:
            floor.append((x, 0))

    # draw the floor line and fill it in with additional lines
    for i in range(len(floor) - 1):
        cv2.line(original, floor[i], floor[i+1], (0, 255, 0), 1)

    for i in range(len(floor)):
        cv2.line(original, (i*BAR_SIZE, HEIGHT - 1), floor[i], (0, 255, 0), 1)

    # find the point where the floor edge is furthest away
    point = biggest_p(floor)

    # draw the point found on the screen
    cv2.circle(original, point, 5, (0, 0, 255))

    # show the final image
    if DISPLAY:
        cv2.imshow('final', original)

    return point
