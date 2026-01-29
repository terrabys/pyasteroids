import pygame
import math
from powerup import PowerUp


class SpeedPowerUp(PowerUp):
    """Speed boost power-up that temporarily increases player speed."""
    
    COLOR = 'lime'
    ICON_COLOR = 'yellow'
    
    def _draw_icon(self, screen, x, y):
        """Draw a lightning bolt / arrow icon."""
        # Draw a forward-pointing arrow/chevron
        size = 6
        # Three chevrons to suggest speed
        for offset in [-4, 0, 4]:
            points = [
                (x + offset - 3, y - size),
                (x + offset + 3, y),
                (x + offset - 3, y + size),
            ]
            pygame.draw.lines(screen, self.ICON_COLOR, False, points, 2)

    def apply(self, player):
        """Give the player a speed boost."""
        player.activate_speed_boost()

    def get_name(self):
        return "Speed"
