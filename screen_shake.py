import random
import pygame
from constants import SHAKE_DECAY


class ScreenShake:
    """Manages screen shake effects for impacts and explosions."""
    
    def __init__(self):
        self.intensity = 0.0
        self.offset = pygame.Vector2(0, 0)
    
    def add_shake(self, intensity):
        """Add shake intensity (stacks with existing shake)."""
        self.intensity = min(self.intensity + intensity, 20)  # Cap max shake
    
    def update(self, dt):
        """Update shake offset and decay intensity."""
        if self.intensity > 0:
            # Random offset based on intensity
            self.offset.x = random.uniform(-self.intensity, self.intensity)
            self.offset.y = random.uniform(-self.intensity, self.intensity)
            # Decay
            self.intensity = max(0, self.intensity - SHAKE_DECAY * dt * self.intensity)
        else:
            self.offset.x = 0
            self.offset.y = 0
    
    def get_offset(self):
        """Get current shake offset as tuple for screen translation."""
        return (int(self.offset.x), int(self.offset.y))
    
    def is_shaking(self):
        """Check if screen is currently shaking."""
        return self.intensity > 0.1
