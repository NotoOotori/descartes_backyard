""" Store constants. """
# Player

## Image

PLAYER_IMAGE_PATH = 'resources/player.png'
PLAYER_IMAGE_ALPHA = 237

## Collision box

PLAYER_COLLISION_BOX_RADIUS = 6
PLAYER_COLLISION_BOX_WIDTH = 3
PLAYER_COLLISION_BOX_COLOR_EDGE = (255, 0, 0)
PLAYER_COLLISION_BOX_COLOR_INSIDE = (255, 255, 255)

## Speed

PLAYER_SPEED = 16

## Bullet

### Image

PLAYER_BULLET_IMAGE_ALPHA = 63
PLAYER_BULLET_IMAGE_PATH = 'resources/bullet1.png'

# TODO: Refactor image loading

### Motion

PLAYER_BULLET_MOTION_KWARGS = {
    'motion_type': 'UniformlyAcceleratedLinearMotion',
    'speed': 20,
    'acceleration': 1,
    'degree': 270}
