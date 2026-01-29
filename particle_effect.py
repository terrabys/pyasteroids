import random
import math
import pygame
from particle import Particle


class ParticleEffect(pygame.sprite.Sprite):
    """Base class for all particle-based visual effects."""
    
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.particles = []

    def _add_particle(self, particle):
        self.particles.append(particle)

    def _create_radial_particles(self, x, y, color, count, speed_range, lifetime_range, size_range=None):
        """Helper to create particles radiating outward from a point."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(speed_range[0], speed_range[1])
            lifetime = random.uniform(lifetime_range[0], lifetime_range[1])
            size = random.uniform(size_range[0], size_range[1]) if size_range else None
            particle = Particle.create_radial(x, y, color, speed, angle, lifetime, size)
            self._add_particle(particle)

    def _cleanup_particles(self):
        """Remove dead particles from the list."""
        self.particles = [p for p in self.particles if p.is_alive()]

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self._cleanup_particles()

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
