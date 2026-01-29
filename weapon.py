from abc import ABC, abstractmethod


class Weapon(ABC):
    """Base class for all weapons. Handles ammo management."""
    
    def __init__(self, max_ammo, start_ammo=0):
        self.max_ammo = max_ammo
        self.ammo = start_ammo
    
    def add_ammo(self, amount=1):
        """Add ammo, capped at max."""
        self.ammo = min(self.max_ammo, self.ammo + amount)
    
    def get_ammo(self):
        """Get current ammo count."""
        return self.ammo
    
    def has_ammo(self):
        """Check if weapon has ammo."""
        return self.ammo > 0
    
    def use_ammo(self, amount=1):
        """Use ammo if available. Returns True if successful."""
        if self.ammo >= amount:
            self.ammo -= amount
            return True
        return False
    
    @abstractmethod
    def fire(self, x, y, rotation, velocity):
        """Fire the weapon from position (x, y) with given rotation and player velocity.
        Returns list of projectile sprites created, or empty list if no ammo."""
        pass
    
    @abstractmethod
    def get_name(self):
        """Return weapon name for UI display."""
        pass
