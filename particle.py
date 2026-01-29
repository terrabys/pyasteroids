import random
import math
import pygame


def lerp_color(color1, color2, t):
    """Linearly interpolate between two colors."""
    if isinstance(color1, str):
        color1 = pygame.Color(color1)
    if isinstance(color2, str):
        color2 = pygame.Color(color2)
    if isinstance(color1, tuple):
        color1 = pygame.Color(*color1)
    if isinstance(color2, tuple):
        color2 = pygame.Color(*color2)
    
    r = int(color1.r + (color2.r - color1.r) * t)
    g = int(color1.g + (color2.g - color1.g) * t)
    b = int(color1.b + (color2.b - color1.b) * t)
    return (r, g, b)


class Particle:
    """Individual particle with physics and rendering."""
    
    def __init__(self, x, y, color, velocity, lifetime, size=None, fade_color=None):
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.color = color
        self.fade_color = fade_color if fade_color else (30, 30, 30)  # Fade to dark
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size if size is not None else random.uniform(2, 5)
        self.drag = 0.98

    def update(self, dt):
        self.position += self.velocity * dt
        self.velocity *= self.drag
        self.lifetime -= dt

    def draw(self, screen):
        if not self.is_alive():
            return
        life_ratio = self.lifetime / self.max_lifetime
        size = max(1, int(self.size * life_ratio))
        # Color fades as particle dies
        draw_color = lerp_color(self.fade_color, self.color, life_ratio)
        pygame.draw.circle(screen, draw_color, (int(self.position.x), int(self.position.y)), size)

    def is_alive(self):
        return self.lifetime > 0

    @classmethod
    def create_radial(cls, x, y, color, speed, angle, lifetime, size=None, fade_color=None):
        """Factory method to create a particle with radial velocity."""
        velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        return cls(x, y, color, velocity, lifetime, size, fade_color)


class LineParticle(Particle):
    """Particle that renders as a line in the direction of velocity."""
    
    def __init__(self, x, y, color, velocity, lifetime, size=None, length=None):
        super().__init__(x, y, color, velocity, lifetime, size)
        self.length = length if length is not None else random.uniform(8, 20)

    def draw(self, screen):
        if not self.is_alive():
            return
        
        # Calculate line based on velocity direction
        life_ratio = self.lifetime / self.max_lifetime
        current_length = max(2, self.length * life_ratio)
        
        # Line extends opposite to velocity (trail behind)
        if self.velocity.length() > 0:
            direction = self.velocity.normalize()
        else:
            direction = pygame.Vector2(1, 0)
        
        # Start point is current position, end point trails behind
        start = self.position
        end = self.position - direction * current_length
        
        # Color fades as particle dies
        draw_color = lerp_color(self.fade_color, self.color, life_ratio)
        
        # Line thickness based on size
        thickness = max(1, int(self.size * life_ratio * 0.5))
        
        pygame.draw.line(screen, draw_color, 
                        (int(start.x), int(start.y)), 
                        (int(end.x), int(end.y)), 
                        thickness)

    @classmethod
    def create_radial(cls, x, y, color, speed, angle, lifetime, size=None, length=None):
        """Factory method to create a line particle with radial velocity."""
        velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        return cls(x, y, color, velocity, lifetime, size, length)
