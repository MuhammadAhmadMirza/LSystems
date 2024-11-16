import pygame
from modules.config import *

# Define color mappings for L-Systems and Themes
LSYSTEM_COLORS = {
    "tree": (0, 255, 0),        # Green
    "mandala": (0, 255, 0),       # Green
    "planet": (0, 0, 255),    # Blue
    "dragon curve": (255, 0, 0)       # Red
}

THEME_COLORS = {
    "ocean": (0, 150, 255),     # Brighter Blue
    "nature": (0, 255, 0),      # Green
    "fire": (255, 0, 0)         # Red
}

def generate_rainbow_gradient(num_segments):
    """Generate a neon rainbow gradient."""
    
    def gradient_color(start_color, end_color, steps):
        """Generate a list of colors forming a gradient between start and end colors."""
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1)
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            gradient.append((r, g, b))
        return gradient

    colors = [
        (255, 0, 0),    # Bright Red
        (255, 0, 255),  # Bright Magenta
        (0, 0, 255),    # Bright Blue
        (0, 255, 255),  # Bright Cyan
        (0, 255, 0)     # Bright Green
    ]
    
    gradient_colors = []
    for i in range(len(colors) - 1):
        segment_steps = num_segments // (len(colors) - 1)
        gradient_colors += gradient_color(colors[i], colors[i + 1], segment_steps)
    
    return gradient_colors

def render_multicolor_text(font, text):
    """Render each letter of the text with gradient colors."""
    gradient = generate_rainbow_gradient(len(text))
    surfaces = []
    for i, char in enumerate(text):
        color = gradient[i % len(gradient)]
        surfaces.append(font.render(char, True, color))
    return surfaces

def get_generation_color(current_gen, max_gen):
    """Compute a redder color as the generation approaches the maximum."""
    if max_gen == 0:
        return (255, 0, 0)  # Default to pure red if max_gen is zero
    
    ratio = min(current_gen / max_gen, 1.0)  # Clamp between 0 and 1
    return (
        int(255 * ratio), 
        int(255 * (1 - ratio)), 
        int(255 * (1 - ratio))
    )

def draw_text(font, text_lines, start_position, max_width, line_height=30, margin=2):
    """Render multiline text with automatic wrapping."""
    current_y = start_position[1]

    for line in text_lines:
        words = line.split(' ')
        current_line = ""
        
        for word in words:
            test_line = current_line + word + ' '
            text_surface = font.render(test_line, True, (255, 255, 255))
            
            if text_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    text_surface = font.render(current_line.strip(), True, (255, 255, 255))
                    text_rect = text_surface.get_rect(topleft=(start_position[0], current_y))
                    screen.blit(text_surface, text_rect)
                    current_y += line_height + margin
                current_line = word + ' '

        if current_line:
            text_surface = font.render(current_line.strip(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(topleft=(start_position[0], current_y))
            screen.blit(text_surface, text_rect)
            current_y += line_height + margin

    return current_y

def draw_system_info(generation, max_generation, current_theme, system, start_y):
    """Display L-System, theme, and generation with appropriate colors."""
    info_font_size = 24
    info_font = pygame.font.Font(rp('assets/fonts/opensans.ttf'), info_font_size)

    # Remove system_color to keep the system name color constant (white)
    theme_color = THEME_COLORS.get(current_theme, (255, 255, 255))
    generation_color = get_generation_color(generation, max_generation)

    # Set system name to white
    system_name = system.__str__() if system else "None"
    system_surface = info_font.render(f"Current L-System:   {system_name}", True, (255, 255, 255))

    if current_theme == "rainbow":
        theme_surfaces = render_multicolor_text(info_font, f"Current Theme: {current_theme}")
    else:
        theme_surface = info_font.render(f"Current Theme:   {current_theme}", True, theme_color)

    generation_surface = info_font.render(f"Generation:   {generation}/{max_generation}", True, generation_color)

    axiom_str = system.axiom if system else 'None'
    axiom_surface = info_font.render(f"Axiom:   {axiom_str}", True, (255, 255, 255))
    rule_text = (", ".join([f"{key}: {value.strip()}" for key, value in system.rules.items()])) if system else 'None'
    rule_surface = info_font.render(f"Rule:   {rule_text if system else 'None'}", True, (255, 255, 255))
    theta_str = "Angle:   " + (f"{round(system.dtheta, 2)}  radians" if system else 'None')
    theta_surface = info_font.render(theta_str, True, (255, 255, 255))

    line_spacing = 30
    screen.blit(system_surface, (SIDE_PANEL_START + 10, start_y))

    if current_theme == "rainbow":
        x_offset = SIDE_PANEL_START + 10
        for surface in theme_surfaces:
            screen.blit(surface, (x_offset, start_y + line_spacing))
            x_offset += surface.get_width()
    else:
        screen.blit(theme_surface, (SIDE_PANEL_START + 10, start_y + line_spacing))

    screen.blit(generation_surface, (SIDE_PANEL_START + 10, start_y + 2 * line_spacing))
    screen.blit(axiom_surface, (SIDE_PANEL_START + 10, start_y + 3 * line_spacing))
    screen.blit(rule_surface, (SIDE_PANEL_START + 10, start_y + 4 * line_spacing))
    screen.blit(theta_surface, (SIDE_PANEL_START + 10, start_y + 5 * line_spacing))

def draw_settings_panel(generation, max_generation, current_theme, system):
    """Draw the settings panel with headings, descriptions, and system info."""
    pygame.draw.rect(screen, (30, 30, 30), (SIDE_PANEL_START, 0, WIDTH - HEIGHT, HEIGHT))

    heading = "Lindenmayer Systems"
    font_size = 50
    font = pygame.font.Font(None, font_size)

    text_surface = font.render(heading, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SIDE_PANEL_START + (WIDTH - HEIGHT) // 2, 30))

    screen.blit(text_surface, text_rect)

    current_y = text_rect.bottom + 10

    description = [
        "L-systems are a mathematical model used to simulate the",
        "growth processes of mandalas and generate complex natural forms.",
        "",
        "How They Work:",
        "1. Axiom (Initiator): Start with an initial string or symbol representing the system's state.",
        "2. Production Rules: Define how each symbol can be replaced with others. These rules determine the system's evolution.",
        "3. Iterations: Apply the production rules repeatedly to generate longer strings.",
        "4. Interpretation: Convert the final string into a geometric structure, typically using graphical commands to visualize the output.",
        "",
        "CONTROLS:",
        "1. [1 to 8]                               to select L-systems",
        "2. [Q]   [W]   [E]   [R]              to select themes",
        "3. SPACE                                to go to the next generation",
        ""
    ]

    description_font_size = 22
    description_font = pygame.font.Font(rp('assets/fonts/opensans.ttf'), description_font_size)

    current_y = draw_text(description_font, description, (SIDE_PANEL_START + 10, current_y), WIDTH - HEIGHT - 20, 28)

    draw_system_info(generation, max_generation, current_theme, system, current_y)
