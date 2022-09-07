import pygame
from pygame.locals import *
import random
import math
from pygame import mixer
import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize the pygame module
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
# Display the title
pygame.display.set_caption('Space Invaders')
# Display the icon
icon = pygame.image.load('spaceship_icon.png')
pygame.display.set_icon(icon)
# Adding background to the game window
background = pygame.image.load('background.png')

# Background sound of the game
mixer.music.load('background.wav')
# add -1 to play the music on loop
mixer.music.play(-1)


# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
# print(type(playerX))-int

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
# ready state - We can't see the bullet on the screen
# Fire state - We can see the bullet currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
white = (255, 255, 255)

gameover_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, white)
    screen.blit(score, (x, y))


def game_over_text():
    over_text = gameover_font.render("GAME OVER", True, white)
    screen.blit(over_text, (200, 250))


"""
# Adding Score to the screen
font = pygame.font.Font('freesansbold.ttf', 32)
# create a text surface object on which text is drawn on
white = (255, 255, 255)
green = (0, 255, 0)
text = font.render('Score- ', score, True, white)
# create a rectangular object for the text surface object
textRect = text.get_rect()
# set the center of the rectangular object.
textRect.center = (380, 50)
"""


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop, so game is running always & the game window doesn't close unless x is pressed
running = True
while running:
    # rgb background
    screen.fill((0, 0, 100))
    screen.blit(background, (0, 0))
    # playerX -= 0.2
    for event in pygame.event.get():
        # For closing the game window
        if event.type == QUIT:
            running = False
        # if keystroke is pressed check if its left or right
        if event.type == pygame.KEYDOWN:
            # print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke has been released")
                playerX_change = 0

    # print(playerX)
    # print(type(playerX))-float

    # Checking for boundaries of the spaceship, so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # and (534 >= enemyY >= 0)
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] -= 4
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # screen.blit(text, textRect)
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

# text format: CTRL + ALT + L
