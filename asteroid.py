import random
import math
import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_COUNT
from logger import log_event

class Asteroid(CircleShape):
    asteroids_group = None  # Reference to asteroids sprite group
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Generate random vertices for irregular asteroid shape
        self.num_vertices = random.randint(8, 12)
        self.vertex_offsets = []
        for i in range(self.num_vertices):
            # Random distance from center (70% to 100% of radius)
            offset = random.uniform(0.7, 1.0)
            self.vertex_offsets.append(offset)
        self.rotation = 0
        self.rotation_speed = random.uniform(-50, 50)  # Degrees per second

    def get_vertices(self):
        vertices = []
        angle_step = 360 / self.num_vertices
        for i in range(self.num_vertices):
            angle = math.radians(i * angle_step + self.rotation)
            distance = self.radius * self.vertex_offsets[i]
            x = self.position.x + math.cos(angle) * distance
            y = self.position.y + math.sin(angle) * distance
            vertices.append((x, y))
        return vertices

    def draw(self, screen):
        pygame.draw.polygon(screen, 'white', self.get_vertices(), LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.wrap_around_screen()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # Don't split if at max asteroid count
        if self.asteroids_group and len(self.asteroids_group) >= ASTEROID_MAX_COUNT:
            return
            
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        velocity1 = self.velocity.rotate(angle)
        velocity2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Offset spawn positions so new asteroids don't overlap
        # Use enough distance to prevent immediate re-collision
        offset_distance = new_radius * 2.5
        direction1 = velocity1.normalize() if velocity1.length() > 0 else pygame.Vector2(1, 0)
        direction2 = velocity2.normalize() if velocity2.length() > 0 else pygame.Vector2(-1, 0)
        
        pos1 = self.position + direction1 * offset_distance
        pos2 = self.position + direction2 * offset_distance
        
        asteroid1 = Asteroid(pos1.x, pos1.y, new_radius)
        asteroid1.velocity = velocity1 * 1.2
        asteroid2 = Asteroid(pos2.x, pos2.y, new_radius)
        asteroid2.velocity = velocity2 * 1.2