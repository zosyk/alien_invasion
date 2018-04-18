import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


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


def update_bullets(settings, screen, aliens, bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_alien_collision(aliens, bullets)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet:
        bullets.empty()
        create_fleet(aliens, settings, screen)


def check_bullet_alien_collision(aliens, bullets):
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)


def ship_hit(settings, stats, screen, ship, aliens, bullets):
    """ Respond to ship being hit by alien """

    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        create_fleet(aliens, settings, screen)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(settings, stats, screen, ship, aliens, bullets):
    """ Update the position of all the aliens fleet"""
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Look for aliens are hitting the bottom of the screen.
    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets)

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets)


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
