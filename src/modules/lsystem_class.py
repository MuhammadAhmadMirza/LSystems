import pygame
import math

class LSystem():
    def __init__(self, name, axiom, rules, dtheta, start, length, ratio):
        self.name = name
        self.axiom = axiom
        self.sentence = axiom
        self.rules = rules
        self.theta = math.pi / 2
        self.dtheta = dtheta
        self.start = start
        self.x, self.y = start
        self.length = length
        self.ratio = ratio
        self.positions = []
        self.color_cache = {}

    def __str__(self):
        return self.name

    def generate(self):
        self.x, self.y = self.start
        self.theta = math.pi / 2
        self.length *= self.ratio

        # Generate the sentence iteratively based on the last sentence
        newStr = "".join(self.rules.get(char, char) for char in self.sentence)
        self.sentence = newStr

    def generate_gradient(self, start_color, end_color, num_segments):
        """Generates a gradient color list from start_color to end_color."""
        return [
            (
                int(start_color[0] + (end_color[0] - start_color[0]) * i // (num_segments - 1)),
                int(start_color[1] + (end_color[1] - start_color[1]) * i // (num_segments - 1)),
                int(start_color[2] + (end_color[2] - start_color[2]) * i // (num_segments - 1))
            )
            for i in range(num_segments)
        ]

    def cache_colors(self, color_scheme, num_segments):
        """Cache the generated colors to avoid redundant calculations."""
        if (color_scheme, num_segments) not in self.color_cache:
            if color_scheme == 'rainbow':
                colors = self.generate_rainbow(num_segments)
            elif color_scheme == 'ocean':
                colors = self.generate_ocean(num_segments)
            elif color_scheme == 'nature':
                colors = self.generate_nature(num_segments)
            elif color_scheme == 'fire':
                colors = self.generate_fire(num_segments)
            else:
                raise ValueError(f"Invalid color scheme: {color_scheme}")
            self.color_cache[(color_scheme, num_segments)] = colors
        return self.color_cache[(color_scheme, num_segments)]

    def generate_rainbow(self, num_segments):
        colors = [
            (255, 0, 0), (255, 0, 255), (0, 0, 255),
            (0, 255, 255), (0, 255, 0)
        ]
        gradient_colors = []
        for i in range(len(colors) - 1):
            gradient_colors += self.generate_gradient(colors[i], colors[i + 1], num_segments // (len(colors) - 1))
        return gradient_colors

    def generate_ocean(self, num_segments):
        dark_blue = (0, 0, 255)
        light_blue = (173, 216, 230)
        return self.generate_gradient(dark_blue, light_blue, num_segments)

    def generate_nature(self, num_segments):
        brown_to_dark_green = self.generate_gradient((139, 69, 19), (0, 100, 0), num_segments // 3)
        dark_green_to_light_green = self.generate_gradient((0, 100, 0), (0, 255, 0), num_segments // 3)
        light_green_to_turquoise = self.generate_gradient((0, 255, 0), (64, 224, 208), num_segments // 3)
        return brown_to_dark_green + dark_green_to_light_green + light_green_to_turquoise


    def generate_fire(self, num_segments):
        dark_red_to_yellow = self.generate_gradient((139, 0, 0), (255, 255, 0), num_segments)
        return dark_red_to_yellow

    def draw(self, screen, color_scheme='nature', reset_position=False):
        num_segments = len(self.sentence)

        # Get cached colors
        colors = self.cache_colors(color_scheme, num_segments)

        # Reset position if required
        if reset_position:
            self.x, self.y = self.start
            self.theta = math.pi / 2  # Reset angle if necessary

        for i, char in enumerate(self.sentence):
            current_color = colors[i % len(colors)]  # Cycle through colors
            
            if char in ['F', 'G']:  # Draw forward
                x2 = self.x - self.length * math.cos(self.theta)
                y2 = self.y - self.length * math.sin(self.theta)
                pygame.draw.line(screen, current_color, (self.x, self.y), (x2, y2))
                self.x, self.y = x2, y2
            elif char == '+':  # Turn right
                self.theta += self.dtheta
            elif char == '-':  # Turn left
                self.theta -= self.dtheta
            elif char == '[':  # Save position
                self.positions.append({'x': self.x, 'y': self.y, 'theta': self.theta})
            elif char == ']':  # Restore position
                position = self.positions.pop()
                self.x, self.y, self.theta = position['x'], position['y'], position['theta']
