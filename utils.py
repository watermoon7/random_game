import random
import numpy as np
import pygame


def chance(probability: float):
    if random.random() > probability:
        return True
    return False


def add(*args):
    if all(isinstance(arg, (int, float, str, bool)) for arg in args):
        return sum(args)
    else:
        result = np.array(args[0])
        for arg in args[1:]:
            result = result + np.array(arg)
        return result


def search_colors(prompt: str):
    for color in pygame.color.THECOLORS:
        if prompt in color:
            print(color, pygame.color.THECOLORS[color])
