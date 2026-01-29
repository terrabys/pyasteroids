import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STAR_COUNT, STAR_LAYERS, STAR_BASE_SPEED


class Star:
    """A single star in the background."""
    __slots__ = ('x', 'y', 'layer', 'size', 'brightness')
    
    def __init__(self, x, y, layer):
        self.x = x
        self.y = y
        self.layer = layer  # 0 = far (slow, dim), higher = near (fast, bright)
        # Size increases with layer
        self.size = 1 if layer == 0 else (2 if layer < STAR_LAYERS - 1 else random.choice([2, 3]))
        # Brightness increases with layer
        base_brightness = 40 + layer * 50
        self.brightness = min(255, base_brightness + random.randint(-20, 20))


class Starfield:
    """Parallax scrolling starfield background."""
    
    def __init__(self, ambient_mode=False):
        self.stars = []
        self._init_stars()
        self.velocity = pygame.Vector2(0, 0)  # Will be influenced by player movement
        self.ambient_mode = ambient_mode
        # For ambient mode: slow random drift
        if ambient_mode:
            self._randomize_drift()
            self.drift_timer = 0.0
    
    def _randomize_drift(self):
        """Set a new random drift direction for ambient mode."""
        angle = random.uniform(0, 360)
        speed = random.uniform(15, 35)  # Slow, gentle drift
        self.velocity = pygame.Vector2(1, 0).rotate(angle) * speed
    
    def _init_stars(self):
        """Create initial stars distributed across screen."""
        stars_per_layer = STAR_COUNT // STAR_LAYERS
        for layer in range(STAR_LAYERS):
            for _ in range(stars_per_layer):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                self.stars.append(Star(x, y, layer))
    
    def update(self, dt, player_velocity=None):
        """Update star positions with parallax effect."""
        if self.ambient_mode:
            # Slowly change drift direction over time
            self.drift_timer += dt
            if self.drift_timer > 8.0:  # Change direction every 8 seconds
                self.drift_timer = 0.0
                self._randomize_drift()
        else:
            # Drift based on player movement (opposite direction for parallax feel)
            if player_velocity and player_velocity.length() > 0:
                self.velocity = self.velocity.lerp(-player_velocity * 0.1, dt * 2)
            else:
                self.velocity = self.velocity.lerp(pygame.Vector2(0, 0), dt * 2)
        
        for star in self.stars:
            # Layer speed multiplier (far = slow, near = fast)
            speed_mult = (star.layer + 1) * 0.5
            
            # Move based on velocity and layer
            star.x += self.velocity.x * speed_mult * dt
            star.y += self.velocity.y * speed_mult * dt
            
            # Gentle drift
            star.y += STAR_BASE_SPEED * speed_mult * dt * 0.2
            
            # Wrap around screen
            if star.x < 0:
                star.x = SCREEN_WIDTH
            elif star.x > SCREEN_WIDTH:
                star.x = 0
            if star.y < 0:
                star.y = SCREEN_HEIGHT
            elif star.y > SCREEN_HEIGHT:
                star.y = 0
    
    def draw(self, screen):
        """Draw all stars."""
        for star in self.stars:
            color = (star.brightness, star.brightness, star.brightness)
            if star.size == 1:
                screen.set_at((int(star.x), int(star.y)), color)
            else:
                pygame.draw.circle(screen, color, (int(star.x), int(star.y)), star.size)
