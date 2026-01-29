import random
import math
from particle import Particle
from particle_effect import ParticleEffect


class Explosion(ParticleEffect):
    """One-time burst explosion effect that auto-destroys when complete."""
    
    def __init__(self, x, y, colors, particle_count, speed_range, lifetime):
        super().__init__()
        self._create_burst(x, y, colors, particle_count, speed_range, lifetime)

    def _create_burst(self, x, y, colors, count, speed_range, lifetime):
        """Create the initial burst of particles."""
        if isinstance(colors, str):
            colors = [colors]
        lifetime_range = (lifetime * 0.5, lifetime)
        for _ in range(count):
            color = random.choice(colors)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(speed_range[0], speed_range[1])
            life = random.uniform(lifetime_range[0], lifetime_range[1])
            particle = Particle.create_radial(x, y, color, speed, angle, life)
            self._add_particle(particle)

    def update(self, dt):
        super().update(dt)
        if len(self.particles) == 0:
            self.kill()


class AsteroidExplosion(Explosion):
    """Explosion effect for destroyed asteroids, scales with asteroid size."""
    
    def __init__(self, x, y, radius):
        particle_count = int(radius * 1.5)
        speed_range = (radius * 2, radius * 5)
        super().__init__(x, y, colors='white', particle_count=particle_count,
                        speed_range=speed_range, lifetime=0.6)


class ShipExplosion(Explosion):
    """Fiery explosion effect for when the player ship is hit."""
    
    def __init__(self, x, y):
        super().__init__(x, y, colors=['orange', 'yellow', 'red'], 
                        particle_count=45, speed_range=(50, 250), lifetime=0.8)


class ShieldExplosion(Explosion):
    """Blue explosion effect for when the player's shield breaks."""
    
    def __init__(self, x, y):
        super().__init__(x, y, colors=['deepskyblue', 'cyan', 'white'], 
                        particle_count=35, speed_range=(80, 200), lifetime=0.5)
