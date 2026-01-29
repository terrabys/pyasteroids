import pygame
import math
from powerup import PowerUp


class RocketPickup(PowerUp):
    """Pickup that gives the player rocket ammo."""
    
    COLOR = 'orange'
    ICON_COLOR = 'red'
    
    def _draw_icon(self, screen, x, y):
        """Draw a rocket icon."""
        # Small rocket shape
        size = 6
        # Rocket body (triangle)
        points = [
            (x, y - size),      # Tip
            (x - 3, y + size),  # Back left
            (x + 3, y + size),  # Back right
        ]
        pygame.draw.polygon(screen, self.ICON_COLOR, points)
        # Flame
        flame_points = [
            (x - 2, y + size),
            (x, y + size + 4),
            (x + 2, y + size),
        ]
        pygame.draw.polygon(screen, 'yellow', flame_points)

    def apply(self, player):
        """Give the player rocket ammo."""
        player.rocket_weapon.add_ammo(1)

    def get_name(self):
        return "Rocket"
