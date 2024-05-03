import pygame
import math
import sys

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60
SUN_RADIUS = 30
SUN_POS = (WIDTH // 2, HEIGHT // 2)
AU = 100  # 100 pixels = 1 Astronomical Unit

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (80, 80, 80)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_RED = (139, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

# Information about planets and the sun
planet_info = {
    "Mercury": "Land mass: Low, Mostly made of: Rock, Metal",
    "Venus": "Land mass: High, Mostly made of: Carbon dioxide, Nitrogen",
    "Earth": "Land mass: High, Mostly made of: Nitrogen, Oxygen",
    "Mars": "Land mass: Medium, Mostly made of: Carbon dioxide, Nitrogen",
    "Jupiter": "Massive, Mostly made of: Hydrogen, Helium",
    "Saturn": "Large, Mostly made of: Hydrogen, Helium",
    "Uranus": "Ice giant, Mostly made of: Water, Methane, Ammonia",
    "Neptune": "Ice giant, Mostly made of: Water, Methane, Ammonia",
    "Sun": "Solor System"
}

# Planet class
class Planet:
    def __init__(self, name, radius, color, distance, orbital_speed):
        self.name = name
        self.radius = radius
        self.color = color
        self.distance = distance
        self.orbital_speed = orbital_speed
        self.angle = 0
        self.x = SUN_POS[0] + self.distance * math.cos(math.radians(self.angle))
        self.y = SUN_POS[1] + self.distance * math.sin(math.radians(self.angle))

    def draw(self, win):
        # Orbit path
        pygame.draw.circle(win, GREEN, SUN_POS, self.distance, 1)
        # Line to sun
        pygame.draw.line(win, WHITE, (int(self.x), int(self.y)), SUN_POS, 1)
        # Planet
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
        # Info text
        speed_text = font.render(f"{self.orbital_speed:.2f} deg/frame", True, WHITE)
        angle_text = font.render(f"{self.angle:.2f}°", True, WHITE)
        win.blit(speed_text, (self.x + self.radius + 5, self.y - 10))
        win.blit(angle_text, (self.x + self.radius + 5, self.y + 10))

    def update(self):
        self.angle = (self.angle + self.orbital_speed) % 360
        self.x = SUN_POS[0] + self.distance * math.cos(math.radians(self.angle))
        self.y = SUN_POS[1] + self.distance * math.sin(math.radians(self.angle))

    def is_clicked(self, pos):
        return math.hypot(self.x - pos[0], self.y - pos[1]) <= self.radius

# Planets data with more planets added
planets = [
    Planet("Mercury", 5, GRAY, 0.39 * AU, 0.15),
    Planet("Venus", 9, WHITE, 0.72 * AU, 0.12),
    Planet("Earth", 10, BLUE, 1 * AU, 0.1),
    Planet("Mars", 7, RED, 1.52 * AU, 0.08),
    Planet("Jupiter", 20, ORANGE, 2.2 * AU, 0.04),  
    Planet("Saturn", 16, LIGHT_BLUE, 3 * AU, 0.032),  
    Planet("Uranus", 13, DARK_RED, 3.7 * AU, 0.024),  
    Planet("Neptune", 13, BLUE, 4.5 * AU, 0.02),  
]

# Sun information
def draw_sun_info():
    text = font.render(planet_info["Sun"], True, WHITE)
    screen.blit(text, (20, 20))

# Main loop
running = True
selected_planet = None
while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        if event.type is pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for planet in planets:
                if planet.is_clicked(pos):
                    selected_planet = planet
                    break

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, YELLOW, SUN_POS, SUN_RADIUS)  # Draw the sun

    for planet in planets:
        planet.update()
        planet.draw(screen)

    # Display selected planet info
    if selected_planet:
        info_text = font.render(planet_info[selected_planet.name], True, WHITE)
        screen.blit(info_text, (20, HEIGHT - 30))

    draw_sun_info()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
