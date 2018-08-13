""" All functions used in the game"""
import sys

import pygame
from pygame.sprite import collide_rect


def check_events(player, keys):
    """ Respond to key events and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, player, keys)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player, keys)

def check_keydown_events(event, player, keys):
    """ Respond to key presses."""
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_UP:
        keys.k_up.press()
        player.moving_up = True
        player.moving_down = False
    elif event.key == pygame.K_DOWN:
        keys.k_down.press()
        player.moving_down = True
        player.moving_up = False
    elif event.key == pygame.K_LEFT:
        keys.k_left.press()
        player.moving_left = True
        player.moving_right = False
    elif event.key == pygame.K_RIGHT:
        keys.k_right.press()
        player.moving_right = True
        player.moving_left = False
    elif event.key == pygame.K_z:
        keys.k_z.press()
        player.shooting = True

def check_keyup_events(event, player, keys):
    """ Respond to key releases."""
    if event.key == pygame.K_UP:
        keys.k_up.release()
        player.moving_up = False
        if keys.k_down.hold:
            player.moving_down = True
    elif event.key == pygame.K_DOWN:
        keys.k_down.release()
        player.moving_down = False
        if keys.k_up.hold:
            player.moving_up = True
    elif event.key == pygame.K_LEFT:
        keys.k_left.release()
        player.moving_left = False
        if keys.k_right.hold:
            player.moving_right = True
    elif event.key == pygame.K_RIGHT:
        keys.k_right.release()
        player.moving_right = False
        if keys.k_left.hold:
            player.moving_left = True
    elif event.key == pygame.K_z:
        keys.k_z.release()
        player.shooting = False

def update_bullets(screen, bullets):
    """Update the bullets' position and speed,
       and remove bullets outside the screen."""
    bullets.update()
    for bullet in bullets.copy():
        if not collide_rect(bullet, screen):
            bullets.remove(bullet)

def update_screen(screen, settings, player, bullets):
    """ Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(settings.bg_color)
    for bullet in bullets:
        bullet.blitme()
    player.blitme()
    player.collision_box.blitme(screen, player.rect.center)

    # Make the most recently drawn screen visible.
    pygame.display.flip()

    # Control the frames per second
    pygame.time.Clock().tick(settings.fps)
