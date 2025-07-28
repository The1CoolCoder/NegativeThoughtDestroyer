import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Screen setup![](venv/1bg.jpg)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Negative Thought Destoyer")
icon = pygame.image.load('teddy-bear.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('1bg.jpg')

#Background sound
mixer.music.load('Masha.mp3')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('teddy.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('cloud.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('arrow.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


# Functions
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
    return distance < 27

def show_score(x,y):
    score = font.render("Score: "+ str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(64, 224, 208))
    screen.blit(over_text, (200,250))
    restart_text = font.render("Press R to Restart", True, (64, 224, 208))
    screen.blit(restart_text, (250, 330))
game_over = False

def reset_game():
    global playerX, playerY, playerX_change
    global enemyX, enemyY, enemyX_change, enemyY_change
    global bulletX, bulletY, bullet_state
    global score_value, game_over
    playerX = 370
    playerY = 480
    playerX_change = 0

    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    for i in range(num_of_enemies):
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    bulletX = 0
    bulletY = 480
    bullet_state = "ready"

    score_value = 0
    game_over = False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('Whoosh.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

            else:
                if event.key == pygame.K_r:
                        reset_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if not game_over:
            if enemyY[i] > playerY - 40:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                    game_over_text()
                break


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosion_sound = mixer.Sound('Pop.mp3')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print("Score:", score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Draw player
    player(playerX, playerY)
    # Show Score
    show_score(textX,textY)
    # Update display
    pygame.display.update()

