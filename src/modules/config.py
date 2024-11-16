# config.py
import pygame
from modules.resource_path import resource_path as rp

LSystems_file_path = {
    'dragon curve': rp('assets/lSystems/dragon curve.txt'),
    'tree': rp('assets/lSystems/tree.txt'),
    'mandala': rp('assets/lSystems/mandala.txt'),
    'planet': rp('assets/lSystems/planet.txt'),
    'pentigree': rp('assets/lSystems/pentigree.txt'),
    'hex fractal': rp('assets/lSystems/hex fractal.txt'),
    'wings': rp('assets/lSystems/wings.txt'),
    'snowflake': rp('assets/lSystems/snowflake.txt'),
    'tentacle fractal': rp('assets/lSystems/tentacle fractal.txt'),
}

# Initialize Pygame
pygame.init()

# Set up the display
DISPLAY_INFO = pygame.display.Info()
WIDTH, HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h
SIDE_PANEL_START = HEIGHT
FPS = 60
DARKNESS_CONSTANT = 100

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lindenmayer Systems")
pygame.display.set_icon(pygame.image.load(rp('assets/images/icon.ico')))