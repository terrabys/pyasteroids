import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteroid import Asteroid
from starfield import Starfield

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3


class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.menu_asteroids = self._init_menu_asteroids()
        self.menu_starfield = Starfield(ambient_mode=True)

    def _init_menu_asteroids(self):
        menu_asteroids = []
        for _ in range(12):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(20, 60)
            asteroid = Asteroid(x, y, radius)
            asteroid.velocity = pygame.Vector2(
                random.uniform(-50, 50),
                random.uniform(-50, 50)
            )
            menu_asteroids.append(asteroid)
        return menu_asteroids

    def _update_menu_asteroids(self, dt):
        for asteroid in self.menu_asteroids:
            asteroid.update(dt)
            # Wrap asteroids around screen
            if asteroid.position.x < -100:
                asteroid.position.x = SCREEN_WIDTH + 100
            elif asteroid.position.x > SCREEN_WIDTH + 100:
                asteroid.position.x = -100
            if asteroid.position.y < -100:
                asteroid.position.y = SCREEN_HEIGHT + 100
            elif asteroid.position.y > SCREEN_HEIGHT + 100:
                asteroid.position.y = -100

    def _draw_menu_asteroids(self, screen):
        for asteroid in self.menu_asteroids:
            asteroid.draw(screen)

    def _draw_centered_text(self, screen, text, y, color='white', font=None):
        if font is None:
            font = self.font
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(rendered, rect)

    def reset_menu_asteroids(self):
        self.menu_asteroids = self._init_menu_asteroids()

    def draw_menu(self, screen, dt):
        screen.fill('black')
        
        # Draw and update starfield
        self.menu_starfield.update(dt)
        self.menu_starfield.draw(screen)
        
        self._update_menu_asteroids(dt)
        self._draw_menu_asteroids(screen)
        
        self._draw_centered_text(screen, "PYASTEROIDS", SCREEN_HEIGHT // 3, 'white', self.title_font)
        self._draw_centered_text(screen, "Press SPACE to Start", SCREEN_HEIGHT // 2)
        self._draw_centered_text(screen, "WASD to move, SPACE to shoot, SHIFT to warp", SCREEN_HEIGHT // 2 + 50, 'gray')
        self._draw_centered_text(screen, "[1] Rockets  [2] Mines", SCREEN_HEIGHT // 2 + 85, 'gray')
        self._draw_centered_text(screen, "Press ESC to Quit", SCREEN_HEIGHT // 2 + 130, 'gray')

    def draw_paused(self, screen, drawable):
        # Draw the game state dimmed
        screen.fill('black')
        for drawable_sprite in drawable:
            drawable_sprite.draw(screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill('black')
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        self._draw_centered_text(screen, "PAUSED", SCREEN_HEIGHT // 3, 'white', self.title_font)
        self._draw_centered_text(screen, "Press SPACE to Resume", SCREEN_HEIGHT // 2)
        self._draw_centered_text(screen, "Press ESC for Menu", SCREEN_HEIGHT // 2 + 50, 'gray')

    def draw_game_over(self, screen, score, dt):
        screen.fill('black')
        
        # Draw and update starfield
        self.menu_starfield.update(dt)
        self.menu_starfield.draw(screen)
        
        self._update_menu_asteroids(dt)
        self._draw_menu_asteroids(screen)
        
        self._draw_centered_text(screen, "GAME OVER", SCREEN_HEIGHT // 3, 'red', self.title_font)
        self._draw_centered_text(screen, f"Final Score: {score}", SCREEN_HEIGHT // 2)
        self._draw_centered_text(screen, "Press SPACE to Play Again", SCREEN_HEIGHT // 2 + 50)
        self._draw_centered_text(screen, "Press ESC for Menu", SCREEN_HEIGHT // 2 + 100, 'gray')

    def draw_hud(self, screen, score, lives, warp_cooldown=0, warp_charging=False, warp_charge_remaining=0, has_shield=False, speed_boost_remaining=0, rocket_ammo=0, mine_ammo=0):
        score_text = self.font.render(f"Score: {score}", True, 'white')
        screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {lives}", True, 'white')
        screen.blit(lives_text, (10, 45))
        
        # Warp cooldown indicator
        if warp_cooldown > 0:
            warp_text = self.font.render(f"WARP: {warp_cooldown:.1f}s", True, 'gray')
        elif warp_charging:
            warp_text = self.font.render(f"WARP: {warp_charge_remaining:.1f}s", True, 'yellow')
        else:
            warp_text = self.font.render("WARP: READY [SHIFT]", True, 'cyan')
        screen.blit(warp_text, (10, 80))
        
        # Shield indicator
        if has_shield:
            shield_text = self.font.render("SHIELD: ACTIVE", True, 'deepskyblue')
        else:
            shield_text = self.font.render("SHIELD: ---", True, 'gray')
        screen.blit(shield_text, (10, 115))
        
        # Speed boost indicator
        if speed_boost_remaining > 0:
            speed_text = self.font.render(f"SPEED: {speed_boost_remaining:.1f}s", True, 'lime')
        else:
            speed_text = self.font.render("SPEED: ---", True, 'gray')
        screen.blit(speed_text, (10, 150))
        
        # Weapon ammo indicators (right side)
        # Rockets [1]
        if rocket_ammo > 0:
            rocket_text = self.font.render(f"[1] ROCKETS: {rocket_ammo}", True, 'orange')
        else:
            rocket_text = self.font.render("[1] ROCKETS: ---", True, 'gray')
        rocket_rect = rocket_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(rocket_text, rocket_rect)
        
        # Mines [2]
        if mine_ammo > 0:
            mine_text = self.font.render(f"[2] MINES: {mine_ammo}", True, 'red')
        else:
            mine_text = self.font.render("[2] MINES: ---", True, 'gray')
        mine_rect = mine_text.get_rect(topright=(SCREEN_WIDTH - 10, 45))
        screen.blit(mine_text, mine_rect)
