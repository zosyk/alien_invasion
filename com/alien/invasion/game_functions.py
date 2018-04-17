import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_events(settings, screen, ship, bullets):
    """Respond on key press and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def fire_bullet(settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_event(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    # Make the most recently drawn screen visible.
    # Redrew all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw()

    pygame.display.flip()


def update_bullets(bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def update_aliens(settings, aliens):
    """ Update the position of all the aliens fleet"""
    check_fleet_edges(settings, aliens)
    aliens.update()


def check_fleet_edges(settings, aliens):
    """ Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """ Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def create_fleet(aliens, settings, screen):
    number_aliens_x = int(settings.screen_width / (2 * settings.alien_width))
    number_aliens_y = int(
        (settings.screen_height - 3 * settings.alien_height - settings.ship_height) / (settings.alien_height * 2))

    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            aliens.add(create_alien(settings, screen, alien_number, row_number))


def create_alien(settings, screen, alien_number, row_number):
    alien = Alien(settings, screen)
    alien.x = settings.alien_width + 2 * settings.alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = settings.alien_height + 2 * settings.alien_height * row_number
    alien.rect.y = alien.y

    return alien
