import random
import pygame

def roll_dice():
    sound_throw = pygame.mixer.Sound('resources/sound/dice.wav')
    sound_throw.play()
    return random.randint(1, 6)