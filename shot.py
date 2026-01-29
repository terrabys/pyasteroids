import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.glow_surface = self._create_glow_surface()

    def _create_glow_surface(self):
        """Create a pre-rendered glow surface for performance."""
        glow_size = self.radius * 4
        surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        # Outer glow
        for i in range(int(glow_size), 0, -2):
            alpha = int(30 * (1 - i / glow_size))
            pygame.draw.circle(surface, (255, 100, 50, alpha), 
                             (glow_size, glow_size), i)
        return surface

    def draw(self, screen):
        # Draw glow effect
        glow_pos = (int(self.position.x - self.radius * 4), 
                   int(self.position.y - self.radius * 4))
        screen.blit(self.glow_surface, glow_pos, special_flags=pygame.BLEND_ADD)
        # Draw core
        pygame.draw.circle(screen, "white", self.position, self.radius)
        pygame.draw.circle(screen, "red", self.position, self.radius - 1)

    def update(self, dt):
        self.position += self.velocity * dt
        # Despawn when off screen
        if (self.position.x < -self.radius or 
            self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or 
            self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()