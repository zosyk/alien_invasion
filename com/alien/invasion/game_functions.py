import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_play_button(settings, screen, stats, play_button, x, y, ship, aliens, bullets, sb):
    """ Start new game when player clicks Play."""
    if play_button.rect.collidepoint(x, y) and not stats.game_active:
        stats.game_active = True
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game settings
        settings.initialize_dynamic_settings()

        stats.reset_stats()

        aliens.empty()
        bullets.empty()

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        create_fleet(aliens, settings, screen)
        ship.center_ship()


def check_events(settings, stats, screen, ship, aliens, bullets, play_button, sb):
    """Respond on key press and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, play_button, x, y, ship, aliens, bullets, sb)


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


def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw()
    # Make the most recently drawn screen visible.
    # Redrew all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw()

    pygame.display.flip()


def update_bullets(settings, screen, aliens, bullets, stats, sb):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_alien_collision(aliens, bullets, stats, settings, sb)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game and create new fleet:
        bullets.empty()
        settings.increase_speed()
        create_fleet(aliens, settings, screen)

        # Increase level
        stats.level += 1
        sb.prep_level()


def check_bullet_alien_collision(aliens, bullets, stats, settings, sb):
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)

    if collisions:
        stats.score += len(collisions) * settings.alien_points
        sb.prep_score()

        check_high_score(stats, sb)


def ship_hit(settings, stats, screen, ship, aliens, bullets, sb):
    """ Respond to ship being hit by alien """

    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        create_fleet(aliens, settings, screen)
        ship.center_ship()

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets, sb)
            break


def update_aliens(settings, stats, screen, ship, aliens, bullets, sb):
    """ Update the position of all the aliens fleet"""
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Look for aliens are hitting the bottom of the screen.
    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets, sb)

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets, sb)


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
