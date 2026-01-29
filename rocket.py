import math
import random
import pygame
from circleshape import CircleShape
from constants import (ROCKET_SPEED, ROCKET_TURN_SPEED, ROCKET_LIFETIME, 
                       ROCKET_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT)
from particle import Particle
from particle_effect import ParticleEffect


class RocketTrail(ParticleEffect):
    """Continuous flame trail for rockets."""
    
    TRAIL_COLORS = ['orange', 'yellow', 'red', 'white']
    
    def __init__(self):
        super().__init__()
    
    def emit(self, x, y, direction):
        """Emit flame particles behind the rocket."""
        base_angle = math.atan2(direction.y, direction.x)
        
        for _ in range(2):
            angle = base_angle + random.uniform(-0.3, 0.3)
            speed = random.uniform(60, 120)
            lifetime = random.uniform(0.15, 0.3)
            color = random.choice(self.TRAIL_COLORS)
            size = random.uniform(2, 4)
            
            particle = Particle.create_radial(x, y, color, speed, angle, lifetime, size)
            self._add_particle(particle)


class Rocket(CircleShape):
    """Homing rocket that seeks the nearest asteroid."""
    
    containers = None  # Set by main.py
    asteroids_group = None  # Reference to asteroids for targeting
    player_ref = None  # Reference to player object for targeting
    taken_targets = None  # Set of asteroids already targeted by other rockets
    
    def __init__(self, x, y, rotation, initial_velocity):
        super().__init__(x, y, ROCKET_RADIUS)
        self.rotation = rotation
        self.lifetime = ROCKET_LIFETIME
        self.target = None
        self.trail = RocketTrail()
        
        # Set initial velocity in the direction we're facing + some of player velocity
        forward = pygame.Vector2(0, 1).rotate(rotation)
        self.velocity = forward * ROCKET_SPEED + initial_velocity * 0.3
    
    def _find_target(self):
        """Find the nearest asteroid to the player that isn't already targeted."""
        if not self.asteroids_group:
            return None
        
        # Use player position for targeting, fall back to rocket position
        target_from = Rocket.player_ref.position if Rocket.player_ref else self.position
        taken = Rocket.taken_targets if Rocket.taken_targets else set()
        
        nearest = None
        nearest_dist = float('inf')
        
        for asteroid in self.asteroids_group:
            # Skip asteroids already targeted by other rockets
            if asteroid in taken:
                continue
            dist = target_from.distance_to(asteroid.position)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = asteroid
        
        # If all asteroids are taken, find any nearest
        if nearest is None:
            for asteroid in self.asteroids_group:
                dist = target_from.distance_to(asteroid.position)
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest = asteroid
        
        # Register this target as taken
        if nearest and Rocket.taken_targets is not None:
            Rocket.taken_targets.add(nearest)
        
        return nearest
    
    def _release_target(self):
        """Release the current target so other rockets can use it."""
        if self.target and Rocket.taken_targets is not None:
            Rocket.taken_targets.discard(self.target)
    
    def _steer_towards_target(self, dt):
        """Steer the rocket towards its target."""
        if not self.target or not self.target.alive():
            # Release old target and find new one
            self._release_target()
            self.target = self._find_target()
        
        if not self.target:
            return
        
        # Calculate angle to target
        to_target = self.target.position - self.position
        if to_target.length() == 0:
            return
        
        target_angle = math.degrees(math.atan2(to_target.x, to_target.y))
        
        # Calculate angle difference
        angle_diff = target_angle - self.rotation
        # Normalize to -180 to 180
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360
        
        # Turn towards target
        max_turn = ROCKET_TURN_SPEED * dt
        if abs(angle_diff) < max_turn:
            self.rotation = target_angle
        elif angle_diff > 0:
            self.rotation += max_turn
        else:
            self.rotation -= max_turn
        
        # Update velocity to match new direction
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity = forward * ROCKET_SPEED
    
    def kill(self):
        """Override kill to release target tracking."""
        self._release_target()
        super().kill()
    
    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        
        self._steer_towards_target(dt)
        self.position += self.velocity * dt
        
        # Emit trail
        back_dir = -self.velocity.normalize() if self.velocity.length() > 0 else pygame.Vector2(0, -1)
        trail_pos = self.position + back_dir * self.radius
        self.trail.emit(trail_pos.x, trail_pos.y, back_dir)
        self.trail.update(dt)
        
        # Wrap around screen
        self.wrap_around_screen()
    
    def draw(self, screen):
        # Draw trail first
        self.trail.draw(screen)
        
        # Draw rocket body (small triangle)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 2
        
        # Triangle points
        tip = self.position + forward * self.radius
        back_left = self.position - forward * self.radius * 0.7 - right
        back_right = self.position - forward * self.radius * 0.7 + right
        
        # Draw rocket body
        pygame.draw.polygon(screen, 'orange', [tip, back_left, back_right])
        pygame.draw.polygon(screen, 'yellow', [tip, back_left, back_right], 1)
        
        # Draw fins
        fin_left = self.position - forward * self.radius * 0.5 - right * 1.5
        fin_right = self.position - forward * self.radius * 0.5 + right * 1.5
        pygame.draw.line(screen, 'red', back_left, fin_left, 2)
        pygame.draw.line(screen, 'red', back_right, fin_right, 2)


class RocketExplosion(ParticleEffect):
    """Explosion effect when rocket hits asteroid."""
    
    EXPLOSION_COLORS = ['orange', 'yellow', 'red', 'white']
    
    def __init__(self, x, y):
        super().__init__()
        self._create_burst(x, y)
    
    def _create_burst(self, x, y):
        """Create explosion particles."""
        for _ in range(25):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            lifetime = random.uniform(0.3, 0.6)
            color = random.choice(self.EXPLOSION_COLORS)
            size = random.uniform(2, 5)
            
            particle = Particle.create_radial(x, y, color, speed, angle, lifetime, size)
            self._add_particle(particle)
    
    def update(self, dt):
        super().update(dt)
        if len(self.particles) == 0:
            self.kill()
