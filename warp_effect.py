import random
import math
import pygame
from particle import Particle
from particle_effect import ParticleEffect


class WarpEffect(ParticleEffect):
    """Visual effect for player warp teleportation."""
    
    WARP_COLORS = ['cyan', 'blue', 'white']
    
    def __init__(self):
        super().__init__()

    def trigger(self, start_x, start_y, end_x, end_y, direction):
        """Create warp particles at origin and destination."""
        # Particles burst outward at start position (disappearing effect)
        self._create_burst(start_x, start_y, outward=True)
        
        # Particles burst inward at end position (appearing effect)
        self._create_burst(end_x, end_y, outward=False)
        
        # Trail particles along the warp path
        self._create_trail(start_x, start_y, end_x, end_y)

    def _create_burst(self, x, y, outward=True):
        """Create a circular burst of particles."""
        count = 20
        for i in range(count):
            angle = (2 * math.pi * i) / count + random.uniform(-0.2, 0.2)
            speed = random.uniform(100, 200) if outward else random.uniform(50, 100)
            
            # For inward burst, reverse the direction
            if not outward:
                angle += math.pi
            
            lifetime = random.uniform(0.3, 0.5)
            color = random.choice(self.WARP_COLORS)
            size = random.uniform(2, 4)
            particle = Particle.create_radial(x, y, color, speed, angle, lifetime, size)
            self._add_particle(particle)

    def _create_trail(self, start_x, start_y, end_x, end_y):
        """Create particles along the warp trajectory."""
        # Calculate direction and distance
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance == 0:
            return
            
        # Normalize direction
        nx, ny = dx / distance, dy / distance
        
        # Create particles along the path
        num_trail_particles = int(distance / 10)
        for i in range(num_trail_particles):
            t = i / max(1, num_trail_particles - 1)
            px = start_x + dx * t
            py = start_y + dy * t
            
            # Add some perpendicular offset for a wider trail
            perp_offset = random.uniform(-15, 15)
            px += -ny * perp_offset
            py += nx * perp_offset
            
            # Trail particles move perpendicular to warp direction
            angle = math.atan2(ny, nx) + math.pi / 2 + random.uniform(-0.5, 0.5)
            speed = random.uniform(30, 80)
            lifetime = random.uniform(0.2, 0.4)
            color = random.choice(self.WARP_COLORS)
            size = random.uniform(1, 3)
            
            particle = Particle.create_radial(px, py, color, speed, angle, lifetime, size)
            self._add_particle(particle)
