# Shoot'em up

# Art: Kenny <https://opengameart.org/users/kenney>
# Music: Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3

import random
import sys
from heapq import heappush, heappop

import pygame
from settings import *

# initialise pygame and create window
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    print('no audio device')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shoot\'em up!!')
clock = pygame.time.Clock()


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text(screen, 'Instructions', 40, WIDTH / 2, HEIGHT * 0.15, RED)
        draw_text(screen, '"W" or "<-" to move left', 20,
                  WIDTH / 2, HEIGHT * 0.45 - 50, GREEN)
        draw_text(screen, '"D" or "->" to move left',
                  20, WIDTH / 2, HEIGHT * 0.45, GREEN)
        draw_text(screen, '"Spacebar" to fire ', 20,
                  WIDTH / 2, HEIGHT * 0.45 + 50, GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)


def main_menu():
    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, 'Space shooter', 48, WIDTH / 2, HEIGHT * 0.15, GREEN)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(int(WIDTH / 2) - 100,
                               int(HEIGHT * 0.5) - 40, 200, 50)
        button_2 = pygame.Rect(int(WIDTH / 2) - 100,
                               int(HEIGHT * 0.5) + 40, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        draw_text(screen, 'Play', 20, int(WIDTH / 2), HEIGHT * 0.5 - 25, WHITE)
        draw_text(screen, 'Instructions', 20, int(
            WIDTH / 2), HEIGHT * 0.5 + 55, WHITE)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


def draw_text(surf, text, size, x, y, color=WHITE, font_name=retro):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x), int(y))
    surf.blit(text_surface, text_rect)


def spawn_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def spawn_bullet(x, y):
    bullet = Bullet(x, y)
    all_sprites.add(bullet)
    bullets.add(bullet)


def draw_health_bar(surf, x, y, percentage):
    if percentage <= 0:
        percentage = 0
    bar_length = 100
    bar_height = 10
    filled = int(percentage / 100 * bar_length)
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    filled_rect = pygame.Rect(x, y, filled, bar_height)
    pygame.draw.rect(surf, GREEN, filled_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, image):
    for it in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 30 * it
        img_rect.y = y
        surf.blit(image, img_rect)


def game():
    if pygame.mixer.get_init():
        pygame.mixer.music.play(loops=-1)

    score = 0
    # Game loop
    RUNNING = True
    while RUNNING:
        # keep loop RUNNING at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check closing window
            if event.type == pygame.QUIT:
                RUNNING = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # check bullet mob collision
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += int((70 - hit.radius) / 2)
            if pygame.mixer.get_init():
                random.choice(expl_snds).play()
            explosion = Explosion(
                expln_anim, hit.rect.center, hit.rect.width * 0.9)
            all_sprites.add(explosion)
            if random.random() > 0.9:
                power = Power(hit.rect.center)
                all_sprites.add(power)
                powerups.add(power)
            spawn_mob()
        # check player power collisions
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'pill':
                if pygame.mixer.get_init():
                    pill_power_snd.play()
                player.health += random.randrange(10, 30)
                if player.health > 100:
                    player.health = 100
            elif hit.type == 'gun':
                if pygame.mixer.get_init():
                    gun_power_snd.play()
                player.gun_power()
            elif hit.type == 'shield':
                player.shield_power()

        # check mob player collision
        hits = pygame.sprite.spritecollide(
            player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            if not player.shield_up:
                player.health -= hit.radius * 2
            if player.health <= 0:
                if pygame.mixer.get_init():
                    player_expln_snd.play()
                death_explosion = Explosion(player_expln_anim, player.rect.center,
                                            max(hit.rect.width * 0.5, player.rect.width * 3))
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                # player.health = 100
            else:
                if pygame.mixer.get_init():
                    random.choice(expl_snds).play()
                explosion = Explosion(
                    expln_anim, hit.rect.center, hit.rect.width * 0.5)
                all_sprites.add(explosion)
                spawn_mob()
        if player.lives == 0 and not death_explosion.alive():
            RUNNING = False

        # Draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_health_bar(screen, 5, 5, player.health)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_img_mini)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

    # Game over screen
    GAMEOVER = True
    while GAMEOVER:
        # keep loop RUNNING at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check closing window
            if event.type == pygame.QUIT:
                GAMEOVER = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GAMEOVER = False
        # Draw / render
        screen.fill(BLACK)
        draw_text(screen, 'GAME OVER', 48, WIDTH / 2, HEIGHT * 0.45)
        draw_text(screen, 'score: ' + str(score), 27,
                  WIDTH / 2, HEIGHT * 0.45 + 56, YELLOW)
        # *after* drawing everything, flip the display
        pygame.display.flip()
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 20
        self.health = 100
        # pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        self.rect.centerx = int(WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.hidden_time = 2000
        self.gun = 1
        self.gun_power_time_heap = []
        self.power_timer = 7000
        self.shield_up = False
        self.shield_up_time = pygame.time.get_ticks()

    def update(self):
        # unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > self.hidden_time:
            self.hidden = False
            self.health = 100
            self.rect.centerx = int(WIDTH / 2)
            self.rect.bottom = HEIGHT - 10
        # gun timer
        if len(self.gun_power_time_heap) > 0:
            if pygame.time.get_ticks() - self.gun_power_time_heap[0] > self.power_timer:
                self.gun -= 1
                heappop(self.gun_power_time_heap)
                if self.gun < 1:
                    self.gun = 1
        # shield_up down
        if pygame.time.get_ticks() - self.shield_up_time > self.power_timer and self.shield_up:
            self.image = player_img
            old_rect = player_img.get_rect()
            old_rect.center = self.rect.center
            self.rect = old_rect
            self.radius = 20
            self.shield_up = False
            if pygame.mixer.get_init():
                shield_down_snd.play()
        self.speedx = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.speedx = -7
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.speedx = 7
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.speedx

    def shoot(self):
        if not self.hidden:
            if self.gun % 2 != 0:
                spawn_bullet(self.rect.centerx, self.rect.top)
                if pygame.mixer.get_init():
                    shoot_snd.play()
                for it in range(1, int((self.gun - 1) / 2) + 1):
                    spawn_bullet(self.rect.centerx + it * 15, self.rect.top)
                    spawn_bullet(self.rect.centerx - it * 15, self.rect.top)
            else:
                for it in range(1, int((self.gun / 2) + 1)):
                    spawn_bullet(self.rect.centerx + it *
                                 15 - 7, self.rect.top)
                    spawn_bullet(self.rect.centerx - it *
                                 15 + 7, self.rect.top)

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (int(WIDTH / 2), HEIGHT + 200)

    def gun_power(self):
        self.gun += 1
        heappush(self.gun_power_time_heap, pygame.time.get_ticks())

    def shield_power(self):
        self.shield_up = True
        if pygame.mixer.get_init():
            shield_up_snd.play()
        self.shield_up_time = pygame.time.get_ticks()
        # self.image = shield_img
        # self.image.fill(BLACK)
        new_rect = shielded_player_img.get_rect()
        new_rect.center = self.rect.center
        # self.image.blit(player_img, self.rect.center)
        self.image = shielded_player_img
        self.rect = new_rect
        self.radius = int(new_rect.width / 2.1)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_imgs)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.42)
        # pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -75)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > WIDTH + 3:
            self.speedx = - self.speedx
        if self.rect.left < 0 - 3:
            self.speedx = - self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -16

    def update(self):
        self.rect.y += self.speedy
        # kill at the top
        if self.rect.bottom < 0:
            self.kill()


class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(list(powerup_imgs.keys()))
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill at the top
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, anim, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = int(size)
        self.anim = []
        for expl_img in anim:
            expl_img_resized = pygame.transform.scale(
                expl_img, (self.size, self.size))
            self.anim.append(expl_img_resized)
        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 40

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame += 1
            if self.frame == len(self.anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.anim[self.frame]
                self.rect.center = center


if __name__ == '__main__':

    # Load all game graphics
    background = pygame.image.load(
        path.join(img_dir, 'Space_Shooter_Background.png')).convert()
    background_rect = background.get_rect()
    player_img = pygame.image.load(
        path.join(img_dir, 'playerShip1_orange.png')).convert()
    player_img = pygame.transform.scale(player_img, (50, 38))
    player_img.set_colorkey(BLACK)
    player_img_mini = pygame.transform.scale(player_img, (25, 19)).convert()
    player_img_mini.set_colorkey(BLACK)
    bullet_img = pygame.image.load(
        path.join(img_dir, 'laserRed06.png')).convert()
    bullet_img.set_colorkey(BLACK)
    meteor_imgs = []
    meteor_list = ['meteorBrown_med1.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
                   'meteorBrown_med3.png', 'meteorBrown_tiny1.png',
                   'meteorBrown_tiny2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png']
    for file in meteor_list:
        img = pygame.image.load(path.join(img_dir, file)).convert()
        img.set_colorkey(BLACK)
        meteor_imgs.append(img)
    expln_anim = []
    player_expln_anim = []
    for i in range(9):
        Filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, Filename)).convert()
        img.set_colorkey(BLACK)
        expln_anim.append(img)
        img.set_colorkey(BLACK)
        Filename = 'sonicExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, Filename)).convert()
        img.set_colorkey(BLACK)
        player_expln_anim.append(img)
    powerup_imgs = {'shield': pygame.image.load(path.join(img_dir, 'shield_silver.png')).convert(),
                    'gun': pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert(),
                    'pill': pygame.image.load(path.join(img_dir, 'pill_blue.png')).convert()}
    for key in list(powerup_imgs.keys()):
        powerup_imgs[key].set_colorkey(BLACK)
    shielded_player_img = pygame.image.load(
        path.join(img_dir, 'shielded_player.png')).convert()
    shielded_player_img.set_colorkey(BLACK)

    # Load all game sounds
    if pygame.mixer.get_init():
        shoot_snd = pygame.mixer.Sound(path.join(snd_dir, 'Laser Shot.wav'))
        expl_snds = []
        for expl in ['expl3.wav', 'expl6.wav']:
            expl_snds.append(pygame.mixer.Sound(path.join(snd_dir, expl)))
        for sound in expl_snds:
            sound.set_volume(0.6)
        player_expln_snd = pygame.mixer.Sound(
            path.join(snd_dir, 'rumble1.ogg'))
        gun_power_snd = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
        gun_power_snd.set_volume(0.6)
        pill_power_snd = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
        pill_power_snd.set_volume(0.6)
        lose_snd = pygame.mixer.Sound(path.join(snd_dir, 'sfx_lose.ogg'))
        shield_up_snd = pygame.mixer.Sound(
            path.join(snd_dir, 'sfx_shieldUp.ogg'))
        shield_down_snd = pygame.mixer.Sound(
            path.join(snd_dir, 'sfx_shieldDown.ogg'))
        pygame.mixer.music.load(
            path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.set_volume(0.4)

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        spawn_mob()

    main_menu()
