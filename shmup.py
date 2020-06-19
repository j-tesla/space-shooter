# Shoot'em up

# Art: Kenny <https://opengameart.org/users/kenney>
# Music: Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3

import pygame
import random
import os

WIDTH = 400
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set up assets folders
game_dir = os.path.dirname(__file__)
img_dir = os.path.join(game_dir, 'img')
snd_dir = os.path.join(game_dir, 'snd')

# initialise pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shoot\'em up!!')
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_suface = font.render(text, True, color)
    text_rect = text_suface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_suface, text_rect)


def spawn_new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, percentage):
    if percentage <= 0:
        percentage = 0
    bar_length = 100
    bar_height = 10
    filled = percentage / 100 *bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    filled_rect = pygame.Rect(x, y, filled, bar_height)
    pygame.draw.rect(surf, GREEN, filled_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.shield = 100
        # pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speedx = -7
        if key_state[pygame.K_RIGHT]:
            self.speedx = 7
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.speedx

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_snd.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_imgs)
        self.image = self.image_orig
        self.image.set_colorkey(BLACK)
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
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -16

    def update(self):
        self.rect.y += self.speedy
        # kill at the top
        if self.rect.bottom < 0:
            self.kill()


# Load all game graphics
background = pygame.image.load(os.path.join(img_dir, 'Space_Shooter_Background.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir, 'playerShip1_orange.png')).convert()
meteor_img = pygame.image.load(os.path.join(img_dir, 'meteorBrown_med3.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, 'laserRed06.png')).convert()
meteor_imgs = []
meteor_list = ['meteorBrown_med1.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_med3.png', 'meteorBrown_tiny1.png',
               'meteorBrown_tiny2.png', 'meteorBrown_big3.png', 'meteorBrown_big2.png']
for img in meteor_list:
    meteor_imgs.append(pygame.image.load(os.path.join(img_dir, img)).convert())

# Load all game sounds
shoot_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser Shot.wav'))
expl_snds = []
for expl in ['expl3.wav', 'expl6.wav']:
    expl_snds.append(pygame.mixer.Sound(os.path.join(snd_dir, expl)))
pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0
pygame.mixer.music.play(loops=-1)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check closing window
        if event.type == pygame.QUIT:
            running = False
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # check bullet mob collision
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += int((70 - hit.radius) / 2)
        random.choice(expl_snds).play()
        spawn_new_mob()

    # check mob player collision
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        if player.shield <= 0:
            running = False
        else:
            spawn_new_mob()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.mixer.music.stop()

# Game over screen
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check closing window
        if event.type == pygame.QUIT:
            running = False

    # Draw / render
    screen.fill(BLACK)
    draw_text(screen, 'GAME OVER', 48, WIDTH / 2, HEIGHT * 0.45)
    draw_text(screen, 'score: ' + str(score), 27, WIDTH / 2, HEIGHT * 0.45 + 56, YELLOW)

    # *after* drawing everything, flip the display
    pygame.display.flip()
