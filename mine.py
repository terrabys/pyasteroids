import math
import random
import pygame
from circleshape import CircleShape
from constants import (MINE_DRIFT_SPEED, MINE_LIFETIME, MINE_RADIUS, 
                       MINE_EXPLOSION_RADIUS, MINE_ARM_TIME)
from particle import Particle
from particle_effect import ParticleEffect


class Mine(CircleShape):
    """Drifting mine that explodes on contact with asteroids."""
    
    containers = None  # Set by main.py
    
    def __init__(self, x, y, initial_velocity):
        super().__init__(x, y, MINE_RADIUS)
        self.lifetime = MINE_LIFETIME
        self.arm_timer = MINE_ARM_TIME  # Time until mine is armed
        self.pulse_timer = 0.0
        self.spike_rotation = 0.0
        
        # Inherit some player velocity + random drift
        drift_angle = random.uniform(0, 360)
        drift = pygame.Vector2(1, 0).rotate(drift_angle) * MINE_DRIFT_SPEED
        self.velocity = initial_velocity * 0.2 + drift
    
    def is_armed(self):
        """Check if mine is armed and ready to explode."""
        return self.arm_timer <= 0
    
    def get_explosion_radius(self):
        """Get the area of effect radius."""
        return MINE_EXPLOSION_RADIUS
    
    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        
        if self.arm_timer > 0:
            self.arm_timer -= dt
        
        # Pulse animation
        self.pulse_timer += dt * 3
        
        # Slow rotation for spikes
        self.spike_rotation += dt * 30
        
        # Apply velocity
        self.position += self.velocity * dt
        
        # Slow down over time
        self.velocity *= 0.99
        
        # Wrap around screen
        self.wrap_around_screen()
    
    def draw(self, screen):
        # Pulse effect
        pulse = 0.8 + 0.2 * math.sin(self.pulse_timer)
        
        # Color based on armed state
        if self.is_armed():
            core_color = 'red'
            spike_color = 'darkred'
            glow_color = (100, 0, 0)
            aoe_color = (255, 50, 50)
        else:
            core_color = 'gray'
            spike_color = 'darkgray'
            glow_color = (50, 50, 50)
            aoe_color = (100, 100, 100)
        
        # Blink warning when about to expire
        if self.lifetime < 3.0 and int(self.lifetime * 4) % 2 == 0:
            core_color = 'white'
            spike_color = 'red'
        
        # Draw AOE indicator (dashed circle)
        if self.is_armed():
            aoe_radius = MINE_EXPLOSION_RADIUS
            num_dashes = 24
            dash_angle = (2 * math.pi) / num_dashes
            for i in range(0, num_dashes, 2):  # Every other segment
                start_angle = i * dash_angle + self.pulse_timer * 0.5
                end_angle = (i + 1) * dash_angle + self.pulse_timer * 0.5
                # Draw arc segment
                start_pos = (
                    self.position.x + math.cos(start_angle) * aoe_radius,
                    self.position.y + math.sin(start_angle) * aoe_radius
                )
                end_pos = (
                    self.position.x + math.cos(end_angle) * aoe_radius,
                    self.position.y + math.sin(end_angle) * aoe_radius
                )
                pygame.draw.line(screen, aoe_color, start_pos, end_pos, 1)
        
        # Draw glow
        glow_radius = int(self.radius * 1.5 * pulse)
        glow_surface = pygame.Surface((glow_radius * 4, glow_radius * 4), pygame.SRCALPHA)
        for i in range(glow_radius, 0, -2):
            alpha = int(40 * (1 - i / glow_radius))
            pygame.draw.circle(glow_surface, (*glow_color, alpha), 
                             (glow_radius * 2, glow_radius * 2), i)
        screen.blit(glow_surface, 
                   (int(self.position.x - glow_radius * 2), 
                    int(self.position.y - glow_radius * 2)), 
                   special_flags=pygame.BLEND_ADD)
        
        # Draw spikes (6 spikes rotating)
        num_spikes = 6
        spike_length = self.radius * 1.8 * pulse
        for i in range(num_spikes):
            angle = math.radians(self.spike_rotation + i * (360 / num_spikes))
            spike_end = (
                self.position.x + math.cos(angle) * spike_length,
                self.position.y + math.sin(angle) * spike_length
            )
            pygame.draw.line(screen, spike_color, self.position, spike_end, 2)
            # Spike tip
            pygame.draw.circle(screen, spike_color, 
                             (int(spike_end[0]), int(spike_end[1])), 3)
        
        # Draw core
        draw_radius = int(self.radius * pulse)
        pygame.draw.circle(screen, core_color, 
                          (int(self.position.x), int(self.position.y)), draw_radius)
        pygame.draw.circle(screen, 'white', 
                          (int(self.position.x), int(self.position.y)), 
                          max(2, draw_radius // 2))


class MineExplosion(ParticleEffect):
    """Large area explosion effect when mine detonates."""
    
    EXPLOSION_COLORS = ['red', 'orange', 'yellow', 'white', 'crimson']
    
    def __init__(self, x, y, radius):
        super().__init__()
        self.center = pygame.Vector2(x, y)
        self.max_radius = radius
        self.expansion_timer = 0.0
        self.expansion_duration = 0.3
        self._create_burst(x, y, radius)
    
    def _create_burst(self, x, y, radius):
        """Create ring of particles expanding outward."""
        # Core burst
        for _ in range(40):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            lifetime = random.uniform(0.4, 0.8)
            color = random.choice(self.EXPLOSION_COLORS)
            size = random.uniform(3, 7)
            
            particle = Particle.create_radial(x, y, color, speed, angle, lifetime, size)
            self._add_particle(particle)
        
        # Ring particles at explosion edge
        ring_particles = 24
        for i in range(ring_particles):
            angle = (2 * math.pi * i) / ring_particles
            px = x + math.cos(angle) * radius * 0.8
            py = y + math.sin(angle) * radius * 0.8
            
            speed = random.uniform(50, 150)
            lifetime = random.uniform(0.3, 0.6)
            color = random.choice(self.EXPLOSION_COLORS)
            size = random.uniform(2, 5)
            
            particle = Particle.create_radial(px, py, color, speed, angle, lifetime, size)
            self._add_particle(particle)
    
    def update(self, dt):
        super().update(dt)
        self.expansion_timer += dt
        if len(self.particles) == 0:
            self.kill()
    
    def draw(self, screen):
        # Draw expanding shockwave ring
        if self.expansion_timer < self.expansion_duration:
            progress = self.expansion_timer / self.expansion_duration
            ring_radius = int(self.max_radius * progress)
            alpha = int(150 * (1 - progress))
            
            # Draw ring
            ring_surface = pygame.Surface((ring_radius * 2 + 4, ring_radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(ring_surface, (255, 100, 100, alpha), 
                             (ring_radius + 2, ring_radius + 2), ring_radius, 3)
            screen.blit(ring_surface, 
                       (int(self.center.x - ring_radius - 2), 
                        int(self.center.y - ring_radius - 2)))
        
        # Draw particles
        super().draw(screen)
