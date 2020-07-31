import pygame
import math
import random
from pygame import mixer

# initialize py_game
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('planet.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption(" Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
PlayerImg = pygame.image.load('player.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    if i % 2 == 0:
        EnemyImg.append(pygame.image.load('enemy_1.png'))
    else:
        EnemyImg.append(pygame.image.load('fear.png'))

    EnemyX.append(random.randint(0, 780))
    EnemyY.append(random.randint(40, 150))
    EnemyX_change.append(4)
    EnemyY_change.append(40)

# bullet
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480  # PlayerY = 480
BulletY_change = 10  # speed of the bullet
Bullet_state = "ready"  # stationary

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 27)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text(x, y):
    over_text = over_font.render(" GAME OVER ", True, (255, 120, 190))
    screen.blit(over_text, (x, y))


# Display score
def show_score(x, y):
    score = font.render(f" Score : {str(score_value)}", True, (255, 150, 150))
    screen.blit(score, (x, y))


# def collision
def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX, 2) + math.pow(EnemyY - BulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# def player
def player(x, y):
    screen.blit(PlayerImg, (x, y))
    # blit means draws players in window


# def enemy
def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


# def bullet firing
def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


# game loop
running = True

while running:
    # BulletX = PlayerX
    screen.fill((50, 0, 50))
    screen.blit(background, (0, 0))
    # PlayerY -= 0.1
    # PlayerX += 0.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key stroke left or right controls
        if event.type == pygame.KEYDOWN:  # enable key
            if event.key == pygame.K_LEFT:
                # print(" left activated ")
                PlayerX_change = -1.5

            if event.key == pygame.K_RIGHT:
                # print(" right activated")
                PlayerX_change = 1.5

            if event.key == pygame.K_SPACE:
                if Bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)

        if event.type == pygame.KEYUP:  # disable key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0

    PlayerX += PlayerX_change
    # adding boundaries to territory of space ship
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736  # 800 - 64 = 736

    # BULLET Movement
    if Bullet_state is "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    if BulletY <= 0:
        BulletY = 480  # back to original position
        Bullet_state = "ready"  # next new bullet to shoot

    # Enemy Movement
    for i in range(no_of_enemies):
        if EnemyY[i] > 450:
            for j in range(no_of_enemies):
                EnemyY[j] = 2000
                PlayerY = 2000
                game_over_text(200, 250)
                break

        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 2
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -2
            EnemyY[i] += EnemyY_change[i]
        # collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            explode_sound = mixer.Sound('explosion.wav')
            explode_sound.play()
            BulletY = 480
            Bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 780)
            EnemyY[i] = random.randint(30, 70)

        enemy(EnemyX[i], EnemyY[i], i)

        # RGB Color
    show_score(textX, textY)
    player(PlayerX, PlayerY)
    pygame.display.update()
