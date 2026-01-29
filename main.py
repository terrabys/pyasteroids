import random
import pygame
from player import Player
from logger import log_event, log_state
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS, 
                       SCORE_SMALL_ASTEROID, SCORE_MEDIUM_ASTEROID, SCORE_LARGE_ASTEROID, 
                       PLAYER_LIVES, PLAYER_WARP_TIME_SCALE, POWERUP_SPAWN_CHANCE, 
                       SHIELD_SPAWN_WEIGHT, SPEED_SPAWN_WEIGHT,
                       SHAKE_HIT_INTENSITY, SHAKE_WARP_INTENSITY, SHAKE_EXPLOSION_INTENSITY,
                       WEAPON_PICKUP_SPAWN_CHANCE, ROCKET_SPAWN_WEIGHT, MINE_SPAWN_WEIGHT)
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import AsteroidExplosion, ShipExplosion, ShieldExplosion
from ui import UI, STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER
from shield_powerup import ShieldPowerUp
from speed_powerup import SpeedPowerUp
from starfield import Starfield
from screen_shake import ScreenShake
from rocket import Rocket, RocketExplosion
from mine import Mine, MineExplosion
from rocket_pickup import RocketPickup
from mine_pickup import MinePickup


def init_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    rockets = pygame.sprite.Group()
    mines = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    Asteroid.asteroids_group = asteroids
    AsteroidField.containers = (updatable,)
    AsteroidField.asteroids_group = asteroids
    AsteroidField()
    Shot.containers = (shots, updatable, drawable)
    AsteroidExplosion.containers = (updatable, drawable)
    ShipExplosion.containers = (updatable, drawable)
    ShieldExplosion.containers = (updatable, drawable)
    RocketExplosion.containers = (updatable, drawable)
    MineExplosion.containers = (updatable, drawable)
    ShieldPowerUp.containers = (powerups, updatable, drawable)
    SpeedPowerUp.containers = (powerups, updatable, drawable)
    RocketPickup.containers = (powerups, updatable, drawable)
    MinePickup.containers = (powerups, updatable, drawable)
    Rocket.containers = (rockets, updatable, drawable)
    Rocket.asteroids_group = asteroids
    Rocket.taken_targets = set()  # Track which asteroids are already targeted
    Mine.containers = (mines, updatable, drawable)
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    # Note: player.position is a Vector2, which is mutable and shared by reference
    Rocket.player_ref = player  # Rockets target asteroids nearest to player
    
    starfield = Starfield()
    screen_shake = ScreenShake()
    
    return updatable, drawable, asteroids, shots, powerups, rockets, mines, player, starfield, screen_shake


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pyasteroids")
    clock = pygame.time.Clock()
    
    ui = UI()
    game_state = STATE_MENU
    score = 0
    lives = PLAYER_LIVES
    updatable, drawable, asteroids, shots, powerups, rockets, mines, player = None, None, None, None, None, None, None, None
    starfield, screen_shake = None, None
    dt = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        game_state = STATE_PLAYING
                        score = 0
                        lives = PLAYER_LIVES
                        updatable, drawable, asteroids, shots, powerups, rockets, mines, player, starfield, screen_shake = init_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif game_state == STATE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        game_state = STATE_PAUSED
                    elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        player.start_warp_charge()
                elif game_state == STATE_PAUSED:
                    if event.key == pygame.K_SPACE:
                        game_state = STATE_PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        game_state = STATE_MENU
                        ui.reset_menu_asteroids()
                elif game_state == STATE_GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        game_state = STATE_PLAYING
                        score = 0
                        lives = PLAYER_LIVES
                        updatable, drawable, asteroids, shots, powerups, rockets, mines, player, starfield, screen_shake = init_game()
                    elif event.key == pygame.K_ESCAPE:
                        game_state = STATE_MENU
                        ui.reset_menu_asteroids()
            if event.type == pygame.KEYUP:
                if game_state == STATE_PLAYING and player:
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        player.release_warp()

        if game_state == STATE_MENU:
            ui.draw_menu(screen, dt)
        
        elif game_state == STATE_PAUSED:
            ui.draw_paused(screen, drawable)
        
        elif game_state == STATE_GAME_OVER:
            ui.draw_game_over(screen, score, dt)
        
        elif game_state == STATE_PLAYING:
            # Apply time slowdown when charging warp
            game_dt = dt
            if player.is_warp_charging():
                game_dt = dt * PLAYER_WARP_TIME_SCALE
            
            # Update warp charge timer (uses real time, not slowed time)
            warp_executed = player.update_warp_charge(dt)
            if warp_executed:
                screen_shake.add_shake(SHAKE_WARP_INTENSITY)
            
            # Update screen shake
            screen_shake.update(dt)
            
            # Update starfield with player velocity for parallax
            starfield.update(dt, player.velocity)
            
            screen.fill('black')
            
            # Draw starfield first (background)
            starfield.draw(screen)
            
            # Apply screen shake offset
            shake_offset = screen_shake.get_offset()
            if screen_shake.is_shaking():
                shake_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                shake_surface.fill('black')
                starfield.draw(shake_surface)
                for drawable_sprite in drawable:
                    drawable_sprite.draw(shake_surface)
                screen.blit(shake_surface, shake_offset)
            else:
                for drawable_sprite in drawable:
                    drawable_sprite.draw(screen)
            
            # HUD always drawn without shake
            ui.draw_hud(screen, score, lives, player.get_warp_cooldown(), 
                       player.is_warp_charging(), player.get_warp_charge_remaining(),
                       player.has_active_shield(), player.get_speed_boost_remaining(),
                       player.get_rocket_ammo(), player.get_mine_ammo())

            log_state()  # Log the current state of the game
            
            updatable.update(game_dt)
            
            # Clear fired projectiles list (they auto-add via containers)
            player.get_fired_projectiles()
            
            # Check asteroid-asteroid collisions
            asteroid_list = list(asteroids)
            collided = set()  # Track asteroids that already collided this frame
            for i, asteroid1 in enumerate(asteroid_list):
                if asteroid1 in collided:
                    continue
                for asteroid2 in asteroid_list[i + 1:]:
                    if asteroid2 in collided:
                        continue
                    if asteroid1.collides_with(asteroid2):
                        log_event("asteroid_collision")
                        AsteroidExplosion(asteroid1.position.x, asteroid1.position.y, asteroid1.radius)
                        AsteroidExplosion(asteroid2.position.x, asteroid2.position.y, asteroid2.radius)
                        screen_shake.add_shake(SHAKE_EXPLOSION_INTENSITY)
                        collided.add(asteroid1)
                        collided.add(asteroid2)
                        asteroid1.split()
                        asteroid2.split()
                        break
            
            for asteroid in asteroids:
                if player.collides_with_circle(asteroid) and not player.is_invincible():
                    log_event("player_hit")
                    # Check if player has shield
                    if player.break_shield():
                        # Shield absorbs the hit
                        log_event("shield_break")
                        ShieldExplosion(player.position.x, player.position.y)
                        screen_shake.add_shake(SHAKE_HIT_INTENSITY)
                        # Still push player away
                        knockback_dir = (player.position - asteroid.position).normalize()
                        player.take_hit(knockback_dir)
                    else:
                        # No shield - take damage
                        ShipExplosion(player.position.x, player.position.y)
                        screen_shake.add_shake(SHAKE_HIT_INTENSITY * 2)
                        lives -= 1
                        if lives <= 0:
                            game_state = STATE_GAME_OVER
                        else:
                            # Push player away from asteroid
                            knockback_dir = (player.position - asteroid.position).normalize()
                            player.take_hit(knockback_dir)
                    break
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        AsteroidExplosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        screen_shake.add_shake(SHAKE_EXPLOSION_INTENSITY * (asteroid.radius / ASTEROID_MIN_RADIUS) * 0.5)
                        # Award points based on asteroid size
                        if asteroid.radius <= ASTEROID_MIN_RADIUS:
                            score += SCORE_SMALL_ASTEROID
                        elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                            score += SCORE_MEDIUM_ASTEROID
                        else:
                            score += SCORE_LARGE_ASTEROID
                        
                        # Chance to spawn power-up (only on player kills)
                        if random.random() < POWERUP_SPAWN_CHANCE:
                            # Weighted random selection for power-up type
                            powerup_classes = [ShieldPowerUp, SpeedPowerUp]
                            weights = [SHIELD_SPAWN_WEIGHT, SPEED_SPAWN_WEIGHT]
                            PowerUpClass = random.choices(powerup_classes, weights=weights)[0]
                            PowerUpClass(asteroid.position.x, asteroid.position.y)
                            log_event("powerup_spawn")
                        
                        # Chance to spawn weapon pickup
                        if random.random() < WEAPON_PICKUP_SPAWN_CHANCE:
                            weapon_classes = [RocketPickup, MinePickup]
                            weights = [ROCKET_SPAWN_WEIGHT, MINE_SPAWN_WEIGHT]
                            WeaponClass = random.choices(weapon_classes, weights=weights)[0]
                            WeaponClass(asteroid.position.x, asteroid.position.y)
                            log_event("weapon_pickup_spawn")
                        
                        shot.kill()
                        asteroid.split()
            
            # Check rocket collisions with asteroids
            for rocket in list(rockets):
                for asteroid in list(asteroids):
                    if rocket.collides_with(asteroid):
                        log_event("rocket_hit")
                        RocketExplosion(rocket.position.x, rocket.position.y)
                        screen_shake.add_shake(SHAKE_EXPLOSION_INTENSITY * 2)
                        
                        # Destroy hit asteroid
                        AsteroidExplosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        score += SCORE_MEDIUM_ASTEROID
                        asteroid.split()
                        rocket.kill()
                        break
            
            # Check mine collisions with asteroids
            for mine in list(mines):
                if not mine.is_armed():
                    continue
                for asteroid in list(asteroids):
                    if mine.collides_with(asteroid):
                        log_event("mine_explode")
                        explosion_radius = mine.get_explosion_radius()
                        MineExplosion(mine.position.x, mine.position.y, explosion_radius)
                        screen_shake.add_shake(SHAKE_EXPLOSION_INTENSITY * 4)
                        
                        # Destroy all asteroids in explosion radius
                        for other_asteroid in list(asteroids):
                            if mine.position.distance_to(other_asteroid.position) < explosion_radius + other_asteroid.radius:
                                AsteroidExplosion(other_asteroid.position.x, other_asteroid.position.y, other_asteroid.radius)
                                score += SCORE_MEDIUM_ASTEROID
                                other_asteroid.split()
                        
                        mine.kill()
                        break
            
            # Check power-up collection
            for powerup in powerups:
                if player.collides_with(powerup):
                    log_event("powerup_collect", type=powerup.get_name())
                    powerup.apply(player)
                    powerup.kill()

        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Limit to 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
