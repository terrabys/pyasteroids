import pygame
import math
import random
from circleshape import CircleShape
from constants import POWERUP_LIFETIME

POWERUP_RADIUS = 15
POWERUP_SPEED = 30


class PowerUp(CircleShape):
    """Base class for all power-ups. Inherits from CircleShape for collision detection."""
    
    # Override in subclasses
    COLOR = 'white'
    ICON_COLOR = 'white'
    
    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_RADIUS)
        self.lifetime = POWERUP_LIFETIME
        self.bob_timer = 0.0
        self.bob_offset = 0.0
        # Give a small random velocity
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(1, 0).rotate(angle) * POWERUP_SPEED

    def update(self, dt):
        """Update powerup position and lifetime."""
        self.position += self.velocity * dt
        self.wrap_around_screen()
        
        # Bobbing animation
        self.bob_timer += dt * 3
        self.bob_offset = math.sin(self.bob_timer) * 3
        
        # Decrease lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        """Draw the powerup with pulsing effect."""
        # Pulsing effect based on lifetime
        pulse = 0.7 + 0.3 * math.sin(self.bob_timer * 2)
        
        # Blink faster when about to expire
        if self.lifetime < 3.0:
            if int(self.lifetime * 5) % 2 == 0:
                return
        
        # Draw outer ring
        draw_y = self.position.y + self.bob_offset
        pygame.draw.circle(screen, self.COLOR, 
                          (int(self.position.x), int(draw_y)), 
                          int(self.radius * pulse), 2)
        
        # Draw icon (override in subclasses)
        self._draw_icon(screen, self.position.x, draw_y)

    def _draw_icon(self, screen, x, y):
        """Override in subclasses to draw specific power-up icon."""
        pass

    def apply(self, player):
        """Apply the power-up effect to the player. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement apply()")

    def get_name(self):
        """Return the name of the power-up for UI display."""
        return "Power-Up"
