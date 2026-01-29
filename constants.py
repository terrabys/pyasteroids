SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
PLAYER_SPEED = 200
PLAYER_TURN_SPEED = 300
LINE_WIDTH = 2

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_MAX_COUNT = 15

SHOT_RADIUS = 1.5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

SCORE_SMALL_ASTEROID = 100
SCORE_MEDIUM_ASTEROID = 50
SCORE_LARGE_ASTEROID = 20

PLAYER_LIVES = 3
PLAYER_INVINCIBILITY_SECONDS = 2.0
PLAYER_ACCELERATION = 300
PLAYER_MAX_SPEED = 400
PLAYER_DRAG = 0.25
PLAYER_KNOCKBACK = 150
PLAYER_WARP_DISTANCE = 200
PLAYER_WARP_COOLDOWN_SECONDS = 4.0
PLAYER_WARP_MAX_CHARGE_SECONDS = 3.5  # Max time player can hold warp charge
PLAYER_WARP_TIME_SCALE = 0.15  # Time slows to 15% during warp charge

# Power-ups
POWERUP_SPAWN_CHANCE = 0.3  # % chance to spawn on asteroid destroy
POWERUP_LIFETIME = 8.0  # Seconds before powerup disappears
SHIELD_SPAWN_WEIGHT = 1.0  # Relative spawn weight for shield
SPEED_SPAWN_WEIGHT = 1.0  # Relative spawn weight for speed boost

# Speed Boost Power-up
SPEED_BOOST_DURATION = 6.0  # How long the speed boost lasts
SPEED_BOOST_MULTIPLIER = 1.5  # Acceleration and max speed multiplier
SPEED_BOOST_TRAIL_INTENSITY = 1.5  # Engine trail size/particle multiplier

# Normal Engine Trail
TRAIL_PARTICLE_COUNT = 2
TRAIL_SPREAD = 0.3  # Radians spread angle
TRAIL_SPEED_MIN = 80
TRAIL_SPEED_MAX = 150
TRAIL_LIFETIME_MIN = 0.2
TRAIL_LIFETIME_MAX = 0.8
TRAIL_SIZE_MIN = 2
TRAIL_SIZE_MAX = 5
TRAIL_OFFSET = 1.0  # Multiplier of player radius for emission offset

# Speed Boost Trail
BOOST_TRAIL_PARTICLE_COUNT = 3
BOOST_TRAIL_SPREAD = 0.02  # Radians spread angle (tighter)
BOOST_TRAIL_SPEED_MIN = 120
BOOST_TRAIL_SPEED_MAX = 200
BOOST_TRAIL_LIFETIME_MIN = 0.3
BOOST_TRAIL_LIFETIME_MAX = 0.6
BOOST_TRAIL_SIZE_MIN = 2
BOOST_TRAIL_SIZE_MAX = 4
BOOST_TRAIL_LENGTH_MIN = 20
BOOST_TRAIL_LENGTH_MAX = 40
BOOST_TRAIL_OFFSET = 3.0  # Multiplier of player radius for emission offset

# Starfield Background
STAR_COUNT = 150
STAR_LAYERS = 3  # Number of parallax layers (far to near)
STAR_BASE_SPEED = 10  # Base speed for furthest layer

# Screen Shake
SHAKE_DECAY = 4.0  # How fast shake diminishes
SHAKE_HIT_INTENSITY = 8  # Shake on player hit
SHAKE_WARP_INTENSITY = 3  # Shake on warp
SHAKE_EXPLOSION_INTENSITY = 2  # Shake on asteroid explosion

# Weapons
WEAPON_PICKUP_SPAWN_CHANCE = 0.3  # Chance to spawn weapon pickup on asteroid kill
ROCKET_SPAWN_WEIGHT = 1.0
MINE_SPAWN_WEIGHT = 1.0

# Homing Rockets
ROCKET_MAX_AMMO = 3
ROCKET_COUNT_PER_FIRE = 3  # Fires 3 rockets at once
ROCKET_SPEED = 350
ROCKET_TURN_SPEED = 180  # Degrees per second for homing
ROCKET_LIFETIME = 4.0  # Seconds before rocket expires
ROCKET_RADIUS = 6
ROCKET_DAMAGE_RADIUS = 40  # Explosion radius

# Mines
MINE_MAX_AMMO = 5
MINE_DRIFT_SPEED = 20  # Slow drift speed
MINE_LIFETIME = 15.0  # Seconds before mine expires
MINE_RADIUS = 12
MINE_EXPLOSION_RADIUS = 120  # Area of effect radius
MINE_ARM_TIME = 0.5  # Seconds before mine becomes active