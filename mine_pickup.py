import pygame
import math
from powerup import PowerUp


class MinePickup(PowerUp):
    """Pickup that gives the player mine ammo."""
    
    COLOR = 'red'
    ICON_COLOR = 'darkred'
    
    def _draw_icon(self, screen, x, y):
        """Draw a mine icon (circle with spikes)."""
        size = 5
        # Core circle
        pygame.draw.circle(screen, self.ICON_COLOR, (int(x), int(y)), size)
        # Spikes
        for i in range(4):
            angle = math.radians(i * 90 + 45)
            spike_end = (
                x + math.cos(angle) * (size + 4),
                y + math.sin(angle) * (size + 4)
            )
            pygame.draw.line(screen, self.ICON_COLOR, (x, y), spike_end, 2)

    def apply(self, player):
        """Give the player mine ammo."""
        player.mine_weapon.add_ammo(1)

    def get_name(self):
        return "Mine"
