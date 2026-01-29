import pygame
import math
from powerup import PowerUp


class ShieldPowerUp(PowerUp):
    """Shield power-up that protects the player from one hit."""
    
    COLOR = 'deepskyblue'
    ICON_COLOR = 'cyan'
    
    def _draw_icon(self, screen, x, y):
        """Draw a shield icon (hexagon shape)."""
        # Draw a small shield/hexagon shape
        size = 6
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 90)
            px = x + math.cos(angle) * size
            py = y + math.sin(angle) * size
            points.append((px, py))
        pygame.draw.polygon(screen, self.ICON_COLOR, points, 1)

    def apply(self, player):
        """Give the player a shield."""
        player.activate_shield()

    def get_name(self):
        return "Shield"
