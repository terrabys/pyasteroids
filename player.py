import pygame
import random
from circleshape import CircleShape 
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_INVINCIBILITY_SECONDS, PLAYER_ACCELERATION, PLAYER_MAX_SPEED, PLAYER_DRAG, PLAYER_KNOCKBACK, PLAYER_WARP_DISTANCE, PLAYER_WARP_COOLDOWN_SECONDS, PLAYER_WARP_MAX_CHARGE_SECONDS, SPEED_BOOST_DURATION, SPEED_BOOST_MULTIPLIER, SPEED_BOOST_TRAIL_INTENSITY, TRAIL_OFFSET, BOOST_TRAIL_OFFSET
from shot import Shot
from engine_trail import EngineTrail
from warp_effect import WarpEffect
from rocket_weapon import RocketWeapon
from mine_weapon import MineWeapon

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.warp_timer = 0
        self.warp_charging = False
        self.warp_charge_timer = 0
        self.invincibility_timer = PLAYER_INVINCIBILITY_SECONDS
        self.has_shield = False
        self.shield_offset = pygame.Vector2(0, 0)  # Parallax offset for shield
        self.speed_boost_timer = 0
        self.engine_trail = EngineTrail()
        self.warp_effect = WarpEffect()
        # Weapons
        self.rocket_weapon = RocketWeapon()
        self.mine_weapon = MineWeapon()
        self.fired_projectiles = []  # Store projectiles to be added to sprite groups
        self.rocket_cooldown = 0
        self.mine_cooldown = 0

    def is_invincible(self):
        return self.invincibility_timer > 0

    def has_active_shield(self):
        return self.has_shield

    def activate_shield(self):
        self.has_shield = True

    def break_shield(self):
        """Break the shield, returns True if shield was active."""
        if self.has_shield:
            self.has_shield = False
            return True
        return False

    def activate_speed_boost(self):
        """Activate speed boost power-up."""
        self.speed_boost_timer = SPEED_BOOST_DURATION

    def has_speed_boost(self):
        """Check if speed boost is active."""
        return self.speed_boost_timer > 0

    def get_speed_boost_remaining(self):
        """Get remaining speed boost time."""
        return max(0, self.speed_boost_timer)

    def take_hit(self, knockback_direction=None):
        self.invincibility_timer = PLAYER_INVINCIBILITY_SECONDS
        if knockback_direction is not None:
            self.velocity = knockback_direction * PLAYER_KNOCKBACK

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def _point_in_triangle(self, p, a, b, c):
        """Check if point p is inside triangle abc using barycentric coordinates."""
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
        
        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
    
    def _closest_point_on_segment(self, p, a, b):
        """Find the closest point on line segment ab to point p."""
        ab = b - a
        ap = p - a
        ab_len_sq = ab.length_squared()
        if ab_len_sq == 0:
            return a
        t = max(0, min(1, ap.dot(ab) / ab_len_sq))
        return a + ab * t
    
    def collides_with_circle(self, circle):
        """Check if this triangle collides with a circle (asteroid)."""
        tri = self.triangle()
        a, b, c = tri[0], tri[1], tri[2]
        
        # Check if circle center is inside triangle
        if self._point_in_triangle(circle.position, a, b, c):
            return True
        
        # Check if circle intersects any edge of the triangle
        edges = [(a, b), (b, c), (c, a)]
        for edge_start, edge_end in edges:
            closest = self._closest_point_on_segment(circle.position, edge_start, edge_end)
            if circle.position.distance_to(closest) < circle.radius:
                return True
        
        return False
    
    def draw(self, screen):
        # Draw engine trail first (behind ship)
        self.engine_trail.draw(screen)
        # Draw warp effect
        self.warp_effect.draw(screen)
        
        # Draw warp ghost preview when charging
        if self.warp_charging and self.can_warp():
            ghost_pos, ghost_tri = self._get_warp_destination()
            # Draw dashed line from current position to warp destination
            self._draw_warp_line(screen, self.position, ghost_pos)
            # Draw ghost ship outline with dashed lines
            self._draw_dashed_polygon(screen, ghost_tri, 'cyan')
        
        # Blink when invincible
        if self.is_invincible() and int(self.invincibility_timer * 10) % 2 == 0:
            return
        
        # Draw shield outline if active (slightly larger blue triangle)
        if self.has_shield:
            shield_tri = self._get_shield_triangle()
            pygame.draw.polygon(screen, 'deepskyblue', shield_tri, 2)
        
        pygame.draw.polygon(screen, 'white', self.triangle(), LINE_WIDTH)
    
    def _get_shield_triangle(self):
        """Get a larger triangle for the shield outline with parallax offset."""
        # Uniform gap between ship and shield on all sides
        shield_gap = 10
        
        # Apply parallax offset to shield position
        shield_center = self.position + self.shield_offset
        
        # Calculate shield vertices with uniform gap
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        
        # Front tip - offset forward
        a = shield_center + forward * (self.radius + shield_gap)
        
        # Back corners - offset backward and outward
        back_offset = shield_gap
        side_offset = shield_gap
        b = shield_center - forward * (self.radius + back_offset) - right * (self.radius / 1.5 + side_offset)
        c = shield_center - forward * (self.radius + back_offset) + right * (self.radius / 1.5 + side_offset)
        
        return [a, b, c]
    
    def rotate(self, direction, dt):
        self.rotation += direction * PLAYER_TURN_SPEED * dt
        
        # Update shield parallax offset based on rotation
        if self.has_shield:
            # Calculate perpendicular offset (shield lags behind rotation)
            right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
            target_offset = right * direction * 6  # Offset in direction of turn
            # Smooth interpolation towards target
            self.shield_offset = self.shield_offset.lerp(target_offset, dt * 8)
    
    def _get_warp_destination(self):
        """Calculate where the ship will warp to and return ghost triangle."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        ghost_pos = self.position + forward * PLAYER_WARP_DISTANCE
        
        # Wrap ghost position around screen
        if ghost_pos.x < -self.radius:
            ghost_pos.x = SCREEN_WIDTH + self.radius
        elif ghost_pos.x > SCREEN_WIDTH + self.radius:
            ghost_pos.x = -self.radius
        if ghost_pos.y < -self.radius:
            ghost_pos.y = SCREEN_HEIGHT + self.radius
        elif ghost_pos.y > SCREEN_HEIGHT + self.radius:
            ghost_pos.y = -self.radius
        
        # Calculate ghost triangle vertices
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = ghost_pos + forward * self.radius
        b = ghost_pos - forward * self.radius - right
        c = ghost_pos - forward * self.radius + right
        
        return ghost_pos, [a, b, c]
    
    def _draw_warp_line(self, screen, start, end):
        """Draw a dashed line between start and end positions."""
        diff = end - start
        distance = diff.length()
        if distance == 0:
            return
        dx, dy = diff.x, diff.y
        
        dash_length = 10
        gap_length = 8
        num_dashes = int(distance / (dash_length + gap_length))
        
        for i in range(num_dashes):
            t1 = i * (dash_length + gap_length) / distance
            t2 = (i * (dash_length + gap_length) + dash_length) / distance
            t2 = min(t2, 1.0)
            
            p1 = (start.x + dx * t1, start.y + dy * t1)
            p2 = (start.x + dx * t2, start.y + dy * t2)
            pygame.draw.line(screen, 'cyan', p1, p2, 1)
    
    def _draw_dashed_polygon(self, screen, vertices, color):
        """Draw a polygon with dashed lines."""
        dash_length = 6
        gap_length = 4
        
        for i in range(len(vertices)):
            start = vertices[i]
            end = vertices[(i + 1) % len(vertices)]
            
            # Convert to Vector2 if needed
            if not isinstance(start, pygame.Vector2):
                start = pygame.Vector2(start)
            if not isinstance(end, pygame.Vector2):
                end = pygame.Vector2(end)
            
            diff = end - start
            distance = diff.length()
            if distance == 0:
                continue
            dx, dy = diff.x, diff.y
            
            num_dashes = int(distance / (dash_length + gap_length))
            for j in range(num_dashes + 1):
                t1 = j * (dash_length + gap_length) / distance
                t2 = (j * (dash_length + gap_length) + dash_length) / distance
                t1 = min(t1, 1.0)
                t2 = min(t2, 1.0)
                
                p1 = (start.x + dx * t1, start.y + dy * t1)
                p2 = (start.x + dx * t2, start.y + dy * t2)
                pygame.draw.line(screen, color, p1, p2, 1)
    
    def accelerate(self, dt, direction=1):
        """Apply thrust in the direction the ship is facing."""
        thrust_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Apply speed boost multiplier
        accel = PLAYER_ACCELERATION
        max_speed = PLAYER_MAX_SPEED
        if self.has_speed_boost():
            accel *= SPEED_BOOST_MULTIPLIER
            max_speed *= SPEED_BOOST_MULTIPLIER
        
        self.velocity += thrust_vector * accel * dt * direction
        
        # Clamp to max speed
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed
        
        # Update shield parallax for acceleration/deceleration
        if self.has_shield:
            # Shield lags behind when accelerating, pushes forward when braking
            accel_offset = -thrust_vector * direction * 8
            self.shield_offset = self.shield_offset.lerp(accel_offset, dt * 10)
        
        # Emit engine trail when thrusting forward
        if direction > 0:
            if self.has_speed_boost():
                # For speed boost: emit from random points along the back edge of the triangle
                forward = pygame.Vector2(0, 1).rotate(self.rotation)
                right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
                
                # Back edge endpoints (offset by BOOST_TRAIL_OFFSET)
                back_left = self.position - forward * self.radius * BOOST_TRAIL_OFFSET - right
                back_right = self.position - forward * self.radius * BOOST_TRAIL_OFFSET + right
                
                # Emit from random point along back edge
                t = random.random()
                emit_pos = back_left.lerp(back_right, t)
                
                intensity = SPEED_BOOST_TRAIL_INTENSITY
                self.engine_trail.emit_directed(emit_pos.x, emit_pos.y, -forward, 
                                                intensity=intensity)
            else:
                # Normal trail: single emission from back center
                back_direction = -thrust_vector
                trail_pos = self.position + back_direction * self.radius * TRAIL_OFFSET
                self.engine_trail.emit(trail_pos.x, trail_pos.y, back_direction, 
                                       intensity=1.0, boosted=False)
        
    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def fire_rockets(self):
        """Fire homing rockets if ammo available."""
        if self.rocket_cooldown > 0:
            return False
        projectiles = self.rocket_weapon.fire(
            self.position.x, self.position.y, 
            self.rotation, self.velocity
        )
        if projectiles:
            self.rocket_cooldown = 0.5  # Half second cooldown
        self.fired_projectiles.extend(projectiles)
        return len(projectiles) > 0

    def deploy_mine(self):
        """Deploy a mine if ammo available."""
        if self.mine_cooldown > 0:
            return False
        projectiles = self.mine_weapon.fire(
            self.position.x, self.position.y,
            self.rotation, self.velocity
        )
        if projectiles:
            self.mine_cooldown = 0.3  # Short cooldown
        self.fired_projectiles.extend(projectiles)
        return len(projectiles) > 0

    def get_fired_projectiles(self):
        """Get and clear the list of newly fired projectiles."""
        projectiles = self.fired_projectiles
        self.fired_projectiles = []
        return projectiles

    def get_rocket_ammo(self):
        """Get current rocket ammo count."""
        return self.rocket_weapon.get_ammo()

    def get_mine_ammo(self):
        """Get current mine ammo count."""
        return self.mine_weapon.get_ammo()

    def start_warp_charge(self):
        """Begin charging the warp - call when shift is pressed."""
        if self.can_warp():
            self.warp_charging = True
            self.warp_charge_timer = PLAYER_WARP_MAX_CHARGE_SECONDS
    
    def release_warp(self):
        """Execute the warp - call when shift is released."""
        if self.warp_charging and self.can_warp():
            self.warp_charging = False
            self._execute_warp()
        else:
            self.warp_charging = False
    
    def is_warp_charging(self):
        """Check if player is currently charging warp."""
        return self.warp_charging and self.can_warp()

    def get_warp_charge_remaining(self):
        """Get remaining charge time."""
        return max(0, self.warp_charge_timer)

    def update_warp_charge(self, dt):
        """Update warp charge timer - returns True if warp should auto-execute."""
        if self.warp_charging and self.can_warp():
            self.warp_charge_timer -= dt
            if self.warp_charge_timer <= 0:
                self.warp_charging = False
                self._execute_warp()
                return True
        return False

    def _execute_warp(self):
        """Perform the actual warp teleportation."""
        self.warp_timer = PLAYER_WARP_COOLDOWN_SECONDS
        
        # Store start position for effect
        start_pos = pygame.Vector2(self.position.x, self.position.y)
        
        # Get destination
        ghost_pos, _ = self._get_warp_destination()
        
        # Get forward direction
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Teleport to destination
        self.position = ghost_pos
        
        # Translate velocity to warp direction while preserving speed
        speed = self.velocity.length()
        if speed > 0:
            self.velocity = forward * speed
        
        # Trigger warp particle effect
        self.warp_effect.trigger(start_pos.x, start_pos.y, 
                                  self.position.x, self.position.y, forward)

    def can_warp(self):
        return self.warp_timer <= 0

    def get_warp_cooldown(self):
        return max(0, self.warp_timer)

    def update(self, dt):
        self.shoot_timer -= dt
        if self.warp_timer > 0:
            self.warp_timer -= dt
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
        if self.rocket_cooldown > 0:
            self.rocket_cooldown -= dt
        if self.mine_cooldown > 0:
            self.mine_cooldown -= dt
        self.engine_trail.update(dt)
        self.warp_effect.update(dt)
        
        # Update shield parallax - drift back to center when not rotating
        # and also react to velocity/acceleration
        if self.has_shield:
            # Add velocity-based offset (shield lags behind movement)
            if self.velocity.length() > 10:
                velocity_offset = -self.velocity.normalize() * 3
                target = self.shield_offset + velocity_offset * dt * 2
                self.shield_offset = self.shield_offset.lerp(target, dt * 3)
            
            # Gradually return to center
            self.shield_offset = self.shield_offset.lerp(pygame.Vector2(0, 0), dt * 4)
        
        # Apply drag to slow down over time (0 = no drag, 1 = max drag)
        # Framerate-independent: drag value = percentage of speed lost per second
        self.velocity *= pow(1 - PLAYER_DRAG, dt)
        
        # Update position based on velocity (momentum)
        self.position += self.velocity * dt
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.accelerate(dt, 1)
        if keys[pygame.K_s]:
            self.accelerate(dt, -0.5)  # Reverse thrust is weaker
        if keys[pygame.K_a]:
            self.rotate(-1, dt)
        if keys[pygame.K_d]:
            self.rotate(1, dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_1]:
            self.fire_rockets()
        if keys[pygame.K_2]:
            self.deploy_mine()
        
        self.wrap_around_screen()