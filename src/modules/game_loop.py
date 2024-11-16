import pygame
import time
from modules.lsystem_loader import load_system
from modules.config import screen
from modules.side_panel_functions import *

def load_l_system(l_sys_text, start, length, ratio):
    """Load the L-System based on the provided parameters."""
    system = load_system(l_sys_text, start, length, ratio)
    print(f"Loaded {l_sys_text}")
    return system

def update_color_theme(key):
    """Update the color theme based on the key pressed."""
    themes = {
        pygame.K_q: 'rainbow',
        pygame.K_w: 'ocean',
        pygame.K_e: 'fire',
        pygame.K_r: 'nature'
    }
    return themes.get(key, None)

def handle_generation(gen, gen_limit, system, color_theme):
    """Handle the generation and rendering of the L-System."""
    if gen < gen_limit:
        gen += 1
        print(f"Generation: {gen}")
        screen.fill((0, 0, 0))

        # Measure generation time
        start_time = time.time()
        try:
            system.generate()
        except:
            print("Please load a system first")
            return gen - 1
        generation_time = time.time() - start_time
        print(f"Generation Time: {generation_time:.4f} seconds")

        # Measure rendering time
        start_time = time.time()
        system.draw(screen, color_theme)
        rendering_time = time.time() - start_time
        print(f"Rendering Time: {rendering_time:.4f} seconds", end='\n\n')

    return gen

def main():
    gen = 0
    gen_limit = 0
    color_theme = 'rainbow'
    
    system = None
    l_systems_info = [
        #       index key           name    parameters: width, height, line length, length reduction ratio, generation limit, color theme
        {'key': pygame.K_1, 'name': 'dragon curve', 'params': (HEIGHT // 2, HEIGHT // 2, HEIGHT // 3, 0.72, 18), 'theme': 'rainbow'},
        {'key': pygame.K_2, 'name': 'planet', 'params': (HEIGHT // 2.5, HEIGHT // 2, HEIGHT // 4, 0.55, 7), 'theme': 'rainbow'},
        {'key': pygame.K_3, 'name': 'mandala', 'params': (HEIGHT // 2, HEIGHT // 2, HEIGHT // 2, 0.5, 7), 'theme': 'nature'},
        {'key': pygame.K_4, 'name': 'hex fractal', 'params': (HEIGHT // 1.5, HEIGHT // 1.7, HEIGHT // 5, 0.5, 5), 'theme': 'ocean'},
        {'key': pygame.K_5, 'name': 'pentigree', 'params': (HEIGHT // 2, HEIGHT // 2, HEIGHT // 6, 0.4, 6), 'theme': 'fire'},
        {'key': pygame.K_6, 'name': 'wings', 'params': (HEIGHT // 2, HEIGHT, HEIGHT // 4.5, 0.5, 8), 'theme': 'fire'},
        {'key': pygame.K_7, 'name': 'tree', 'params': (HEIGHT // 2.2, HEIGHT, HEIGHT // 11, 0.5, 8), 'theme': 'nature'},
        {'key': pygame.K_8, 'name': 'snowflake', 'params': (HEIGHT // 2, HEIGHT // 2, HEIGHT // 6, 0.5, 8), 'theme': 'ocean'},
        {'key': pygame.K_9, 'name': 'tentacle fractal', 'params': (HEIGHT // 2, HEIGHT // 2, HEIGHT // 4.5, 0.6, 10), 'theme': 'ocean'},
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Load L-System based on the key pressed
                for info in l_systems_info:
                    if event.key == info['key']:
                        start, height, length, ratio, gen_limit = info['params']
                        l_sys_text = LSystems_file_path[info['name']]
                        color_theme = info['theme']
                        system = load_l_system(l_sys_text, (start, height), length, ratio)
                        gen = 0
                        gen = handle_generation(gen, gen_limit, system, color_theme)
                        break
                
                # Update color theme
                new_color_theme = update_color_theme(event.key)
                if new_color_theme:
                    color_theme = new_color_theme
                    print(f"Color theme: {color_theme}")

                    # Redraw the current system with the new color theme
                    if system:  # Check if a system is loaded
                        screen.fill((0, 0, 0))  # Clear the screen
                        system.draw(screen, color_theme, reset_position=True)  # Reset position on theme change

                if event.key == pygame.K_SPACE:
                    gen = handle_generation(gen, gen_limit, system, color_theme)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                gen = handle_generation(gen, gen_limit, system, color_theme)

            draw_settings_panel(gen,gen_limit, color_theme, system)                
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
