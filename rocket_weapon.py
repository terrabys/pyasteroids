import pygame
from weapon import Weapon
from rocket import Rocket
from constants import ROCKET_MAX_AMMO, ROCKET_COUNT_PER_FIRE


class RocketWeapon(Weapon):
    """Homing rocket launcher that fires 3 seeking rockets."""
    
    def __init__(self):
        super().__init__(max_ammo=ROCKET_MAX_AMMO, start_ammo=0)
    
    def fire(self, x, y, rotation, velocity):
        """Fire 3 homing rockets in a spread pattern."""
        if not self.use_ammo(1):
            return []
        
        rockets = []
        # Fire 3 rockets with slight angle spread
        angles = [-15, 0, 15]  # Spread angles
        
        for angle_offset in angles:
            rocket = Rocket(x, y, rotation + angle_offset, velocity)
            rockets.append(rocket)
        
        return rockets
    
    def get_name(self):
        return "Rockets"
