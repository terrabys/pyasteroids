import random
import math
from particle import Particle, LineParticle
from particle_effect import ParticleEffect
from constants import (TRAIL_PARTICLE_COUNT, TRAIL_SPREAD, TRAIL_SPEED_MIN, TRAIL_SPEED_MAX,
                       TRAIL_LIFETIME_MIN, TRAIL_LIFETIME_MAX, TRAIL_SIZE_MIN, TRAIL_SIZE_MAX,
                       BOOST_TRAIL_PARTICLE_COUNT, BOOST_TRAIL_SPREAD, BOOST_TRAIL_SPEED_MIN,
                       BOOST_TRAIL_SPEED_MAX, BOOST_TRAIL_LIFETIME_MIN, BOOST_TRAIL_LIFETIME_MAX,
                       BOOST_TRAIL_SIZE_MIN, BOOST_TRAIL_SIZE_MAX, BOOST_TRAIL_LENGTH_MIN,
                       BOOST_TRAIL_LENGTH_MAX)


class EngineTrail(ParticleEffect):
    """Continuous particle emitter for ship engine exhaust."""
    
    TRAIL_COLORS = ['orange', 'yellow', 'red']
    BOOST_COLORS = ['cyan', 'white', 'deepskyblue', 'yellow']
    
    def __init__(self):
        super().__init__()

    def emit(self, x, y, direction, intensity=1.0, boosted=False):
        """Emit particles in the given direction."""
        base_angle = math.atan2(direction.y, direction.x)
        colors = self.TRAIL_COLORS
        
        for _ in range(TRAIL_PARTICLE_COUNT):
            angle = base_angle + random.uniform(-TRAIL_SPREAD, TRAIL_SPREAD)
            speed = random.uniform(TRAIL_SPEED_MIN, TRAIL_SPEED_MAX) * intensity
            lifetime = random.uniform(TRAIL_LIFETIME_MIN, TRAIL_LIFETIME_MAX)
            color = random.choice(colors)
            size = random.uniform(TRAIL_SIZE_MIN, TRAIL_SIZE_MAX) * intensity
            
            particle = Particle.create_radial(x, y, color, speed, angle, lifetime, size)
            self._add_particle(particle)

    def emit_directed(self, x, y, direction, intensity=1.0):
        """Emit line particles in a specific direction with minimal spread (for speed boost)."""
        base_angle = math.atan2(direction.y, direction.x)
        colors = self.BOOST_COLORS
        
        for _ in range(BOOST_TRAIL_PARTICLE_COUNT):
            angle = base_angle + random.uniform(-BOOST_TRAIL_SPREAD, BOOST_TRAIL_SPREAD)
            speed = random.uniform(BOOST_TRAIL_SPEED_MIN, BOOST_TRAIL_SPEED_MAX) * intensity
            lifetime = random.uniform(BOOST_TRAIL_LIFETIME_MIN, BOOST_TRAIL_LIFETIME_MAX)
            color = random.choice(colors)
            size = random.uniform(BOOST_TRAIL_SIZE_MIN, BOOST_TRAIL_SIZE_MAX)
            length = random.uniform(BOOST_TRAIL_LENGTH_MIN, BOOST_TRAIL_LENGTH_MAX) * intensity
            
            particle = LineParticle.create_radial(x, y, color, speed, angle, lifetime, size, length)
            self._add_particle(particle)
