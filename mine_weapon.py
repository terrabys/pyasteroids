import pygame
from weapon import Weapon
from mine import Mine
from constants import MINE_MAX_AMMO


class MineWeapon(Weapon):
    """Mine deployer that drops proximity mines behind the ship."""
    
    def __init__(self):
        super().__init__(max_ammo=MINE_MAX_AMMO, start_ammo=0)
    
    def fire(self, x, y, rotation, velocity):
        """Deploy a mine behind the ship."""
        if not self.use_ammo(1):
            return []
        
        # Deploy mine slightly behind ship position
        back = pygame.Vector2(0, -1).rotate(rotation)
        mine_x = x + back.x * 30
        mine_y = y + back.y * 30
        
        # Give mine a small backward velocity
        mine_velocity = back * 15 + velocity * 0.1
        mine = Mine(mine_x, mine_y, mine_velocity)
        return [mine]
    
    def get_name(self):
        return "Mines"
